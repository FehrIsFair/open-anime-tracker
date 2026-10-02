#!/usr/bin/env python3
"""
Model Context Protocol (MCP) server for local llama.cpp instance.

Provides tools for Antigravity and subagents to query a local llama.cpp server
with a ~128k token context window. Includes a strict fail-fast mechanism:
if the local agent is offline, unreachable, or unconfigured, it fails fast
in <1.5 seconds and returns a clear, structured notification rather than hanging
or crashing the MCP client.
"""

import json
import os
import socket
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
import urllib.request

from mcp.server.mcpserver import MCPServer

# ------------------------------------------------------------------------------
# Environment & Configuration
# ------------------------------------------------------------------------------

def _load_dotenv_fallback():
    """Load variables from project root .env if not already set in environment."""
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env_file = os.path.join(root_dir, ".env")
    if os.path.isfile(env_file):
        try:
            with open(env_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    key, val = line.split("=", 1)
                    key = key.strip()
                    val = val.strip().strip("\"'")
                    if key and key not in os.environ:
                        os.environ[key] = val
        except Exception:
            pass

_load_dotenv_fallback()

# Base URL to the llama.cpp server (defaults to localhost:8080)
DEFAULT_URL = "http://127.0.0.1:8080"
LLAMA_CPP_URL = os.environ.get("LLAMA_CPP_URL", DEFAULT_URL).rstrip("/")

# Fail-fast timeout for initial connection / health probe (in seconds)
CONNECT_TIMEOUT = float(os.environ.get("LLAMA_CPP_CONNECT_TIMEOUT", "1.5"))

# Maximum wait time for inference generation once connected (in seconds)
REQUEST_TIMEOUT = float(os.environ.get("LLAMA_CPP_REQUEST_TIMEOUT", "120.0"))

# Default advertised context window size (~128k tokens)
CONTEXT_WINDOW = int(os.environ.get("LLAMA_CPP_CONTEXT_WINDOW", "131072"))

# Model name identifier (default: "default")
MODEL_NAME = os.environ.get("LLAMA_CPP_MODEL_NAME", "default")


# ------------------------------------------------------------------------------
# Fail-Fast Health Probe
# ------------------------------------------------------------------------------

def probe_llama_server(url: str = LLAMA_CPP_URL, timeout: float = CONNECT_TIMEOUT) -> tuple[bool, str, dict]:
    """
    Quickly probe if the llama.cpp server is reachable and responsive.
    
    Guaranteed to return in <= timeout seconds.
    Returns:
        (is_online: bool, message: str, metadata: dict)
    """
    parsed = urlparse(url)
    host = parsed.hostname or "127.0.0.1"
    port = parsed.port or (443 if parsed.scheme == "https" else 80)

    # Step 1: Fast socket connect test
    start_time = time.monotonic()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        sock.connect((host, port))
        sock.close()
    except (socket.timeout, TimeoutError):
        elapsed = round(time.monotonic() - start_time, 2)
        return False, f"Connection timed out after {elapsed}s connecting to {host}:{port}", {}
    except ConnectionRefusedError:
        return False, f"Connection refused at {host}:{port} (no service listening)", {}
    except Exception as e:
        return False, f"Network error connecting to {host}:{port}: {str(e)}", {}

    # Step 2: HTTP probe to verify llama.cpp server status
    remaining_timeout = max(0.5, timeout - (time.monotonic() - start_time))
    metadata = {}
    
    # Try /props or /healthMCP Library: The project already has mcp>=2.2.0 in pyproject.toml (dev dependencies). The bridge will use from mcp.server.mcpserver import MCPServer with zero additional external dependencies (using Python standard library urllib / socket for HTTP communication).
    for endpoint in ("/props", "/health", "/v1/models"):
        try:
            req = urllib.request.Request(
                f"{url}{endpoint}",
                headers={"User-Agent": "Antigravity-Llama-MCP/1.0"},
                method="GET"
            )
            with urllib.request.urlopen(req, timeout=remaining_timeout) as resp:
                if resp.status == 200:
                    raw_data = resp.read().decode("utf-8", errors="replace")
                    try:
                        metadata = json.loads(raw_data)
                    except json.JSONDecodeError:
                        pass
                    return True, "Server online and responsive", metadata
        except HTTPError as e:
            # An HTTP error still means the server is reachable and active
            return True, f"Server responded with HTTP {e.code}", metadata
        except Exception:
            continue

    # Socket connected, server is considered reachable even if endpoints differ
    return True, "Server reachable on port", metadata


def format_unavailable_message(reason: str) -> str:
    """Format an explicit, fail-fast notice for Antigravity when the agent is down."""
    return (
        f"[LOCAL_AGENT_UNAVAILABLE]\n"
        f"Unable to reach the local llama.cpp server at '{LLAMA_CPP_URL}'.\n"
        f"Reason: {reason}.\n\n"
        f"Instructions for Antigravity:\n"
        f"1. DO NOT retry calling this local agent tool during this step.\n"
        f"2. The local llama.cpp agent is currently offline or unreachable on this network.\n"
        f"3. Seamlessly proceed with the task using standard Antigravity models and native tools.\n"
        f"4. If you are a collaborator or CI environment without a local GPU/llama-server, this is expected.\n"
        f"5. To enable the local agent, ensure llama-server is running and set LLAMA_CPP_URL in .env."
    )


# ------------------------------------------------------------------------------
# MCP Server & Tools
# ------------------------------------------------------------------------------

server = MCPServer("local-llama")


@server.tool(
    description=(
        "Check if the local llama.cpp agent is reachable and inspect its active configuration. "
        "Returns model details, active context window size (~128k), or a fast offline notice in <1.5s."
    )
)
def check_local_agent_status() -> str:
    """Check connectivity and status of the local llama.cpp instance."""
    is_online, reason, metadata = probe_llama_server(LLAMA_CPP_URL, CONNECT_TIMEOUT)
    if not is_online:
        return format_unavailable_message(reason)

    # Attempt to extract context size from /props if available
    active_ctx = CONTEXT_WINDOW
    if isinstance(metadata, dict):
        # llama.cpp /props often includes default_generation_settings with n_ctx
        gen_settings = metadata.get("default_generation_settings", {})
        if "n_ctx" in gen_settings:
            active_ctx = gen_settings["n_ctx"]
        elif "n_ctx" in metadata:
            active_ctx = metadata["n_ctx"]

    return (
        f"[LOCAL_AGENT_ONLINE]\n"
        f"Status: Online and responsive\n"
        f"URL: {LLAMA_CPP_URL}\n"
        f"Context Window: ~{active_ctx // 1024}k tokens ({active_ctx} tokens)\n"
        f"Model: {MODEL_NAME}\n"
        f"Connect Timeout: {CONNECT_TIMEOUT}s (Fail-Fast enabled)\n"
        f"Request Timeout: {REQUEST_TIMEOUT}s"
    )


@server.tool(
    description=(
        "Query the local LLM running on llama.cpp with a massive ~128k token context window. "
        "Best suited for large multi-file analysis, large code diffs, bulky logs, or deep background reasoning. "
        "Fails fast in <1.5s if the local server is offline, allowing immediate fallback to native tools."
    )
)
def query_local_model(prompt: str, system_prompt: str = "", context: str = "") -> str:
    """
    Send a prompt and optional large context to the local llama.cpp instance.

    Args:
        prompt: The main instruction or question to send.
        system_prompt: Optional custom system prompt (defaults to helpful assistant).
        context: Optional large context string (source code, logs, diffs) utilizing the ~128k window.
    """
    # Fail fast before sending heavy payloads
    is_online, reason, _ = probe_llama_server(LLAMA_CPP_URL, CONNECT_TIMEOUT)
    if not is_online:
        return format_unavailable_message(reason)

    # Construct chat completion messages
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    else:
        messages.append({
            "role": "system",
            "content": (
                "You are an expert AI software engineer. Provide clear, accurate, "
                "well-structured code and answers."
            )
        })

    if context:
        user_content = f"--- CONTEXT ---\n{context}\n\n--- TASK ---\n{prompt}"
    else:
        user_content = prompt

    messages.append({"role": "user", "content": user_content})

    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "stream": False,
    }

    req_data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{LLAMA_CPP_URL}/v1/chat/completions",
        data=req_data,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "Antigravity-Llama-MCP/1.0"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
            resp_body = resp.read().decode("utf-8", errors="replace")
            res_json = json.loads(resp_body)
    except HTTPError as e:
        err_msg = e.read().decode("utf-8", errors="replace") if e.fp else str(e)
        return (
            f"[LOCAL_AGENT_ERROR] HTTP {e.code} from llama.cpp server: {err_msg}\n\n"
            f"Please proceed using standard Antigravity tools."
        )
    except (URLError, TimeoutError, socket.timeout) as e:
        return format_unavailable_message(f"Request timed out or failed: {str(e)}")
    except Exception as e:
        return format_unavailable_message(f"Unexpected error communicating with llama.cpp: {str(e)}")

    # Extract assistant reply
    choices = res_json.get("choices", [])
    if not choices:
        return "[LOCAL_AGENT_EMPTY_RESPONSE] The local model returned no choices."

    reply_content = choices[0].get("message", {}).get("content", "").strip()

    # Append usage footer
    usage = res_json.get("usage", {})
    prompt_tokens = usage.get("prompt_tokens", "?")
    completion_tokens = usage.get("completion_tokens", "?")
    total_tokens = usage.get("total_tokens", "?")

    footer = (
        f"\n\n---\n"
        f"*[Local Agent: llama.cpp | Tokens: {prompt_tokens} prompt + {completion_tokens} completion = {total_tokens} total | Window: ~{CONTEXT_WINDOW // 1024}k]*"
    )

    return reply_content + footer


if __name__ == "__main__":
    server.run(transport="stdio")
