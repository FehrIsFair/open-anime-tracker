# Local LLM Agent Integration (llama.cpp)

## Overview
A local `llama.cpp` inference engine can be reached on the local network via the `local-llama` MCP server (`scripts/llama_mcp_server.py`).

- **Context Window**: ~128k tokens (`131072` tokens).
- **Endpoint**: Configurable via `LLAMA_CPP_URL` in `.env` (defaults to `http://127.0.0.1:8080`).
- **Tools**:
  - `query_local_model(prompt, system_prompt, context)`: Dispatches prompts and large context to the local model.
  - `check_local_agent_status()`: Quick connectivity and context limit health probe.

---

## When to Delegate to Local Agent
- **Large Context Ingestion**: Analyzing entire code modules, large test run outputs, database dump excerpts, or multi-commit git diffs that benefit from the 128k context window.
- **Background Tasks**: Offloading long-running analysis or auxiliary drafting tasks while Antigravity continues pair-programming with the user.

---

## Fail-Fast Fallback Protocol (Critical)
The local agent integration implements a **strict 1.5-second fail-fast policy**:
1. If the tool returns a response beginning with `[LOCAL_AGENT_UNAVAILABLE]`, the local server is offline, down, or not present on the current developer's network.
2. **DO NOT retry** calling `query_local_model` or `check_local_agent_status` during the current turn.
3. Immediately proceed to execute the task using standard Antigravity capabilities and built-in tools.
4. When collaborating on this project without a local GPU/llama-server instance, this unavailable state is normal and expected.
