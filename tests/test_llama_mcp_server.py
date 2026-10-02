"""Unit tests for the fail-fast local llama.cpp MCP server."""

import json
import time
from unittest.mock import MagicMock, patch

import pytest

from scripts.llama_mcp_server import (
    check_local_agent_status,
    format_unavailable_message,
    probe_llama_server,
    query_local_model,
)


def test_probe_llama_server_connection_refused():
    """Verify that a closed port immediately fails fast with False."""
    start = time.monotonic()
    is_online, reason, metadata = probe_llama_server("http://127.0.0.1:59998", timeout=1.0)
    elapsed = time.monotonic() - start

    assert is_online is False
    assert "refused" in reason.lower() or "error" in reason.lower() or "timed out" in reason.lower()
    assert elapsed < 1.0
    assert metadata == {}


def test_probe_llama_server_timeout_fails_fast():
    """Verify that an unreachable blackhole address respects timeout and fails fast."""
    start = time.monotonic()
    is_online, reason, _ = probe_llama_server("http://10.255.255.1:8080", timeout=0.5)
    elapsed = time.monotonic() - start

    assert is_online is False
    assert "timed out" in reason.lower() or "network error" in reason.lower()
    assert elapsed < 1.0


def test_format_unavailable_message_structure():
    """Verify that the unavailable message contains clear Antigravity directives."""
    msg = format_unavailable_message("Connection refused")
    assert "[LOCAL_AGENT_UNAVAILABLE]" in msg
    assert "DO NOT retry" in msg
    assert "standard Antigravity models" in msg


def test_check_local_agent_status_offline():
    """Verify check_local_agent_status fails fast with unavailable banner when offline."""
    with patch("scripts.llama_mcp_server.LLAMA_CPP_URL", "http://127.0.0.1:59998"):
        status = check_local_agent_status()
        assert "[LOCAL_AGENT_UNAVAILABLE]" in status
        assert "DO NOT retry" in status


def test_query_local_model_offline_fails_fast():
    """Verify query_local_model returns unavailable banner without throwing exceptions."""
    with patch("scripts.llama_mcp_server.LLAMA_CPP_URL", "http://127.0.0.1:59998"):
        res = query_local_model("Summarize this file", context="sample code")
        assert "[LOCAL_AGENT_UNAVAILABLE]" in res
        assert "offline or unreachable" in res


def test_check_local_agent_status_online_mock():
    """Verify check_local_agent_status formats online metadata correctly when reachable."""
    mock_meta = {
        "default_generation_settings": {
            "n_ctx": 131072
        }
    }
    with patch("scripts.llama_mcp_server.probe_llama_server", return_value=(True, "OK", mock_meta)):
        status = check_local_agent_status()
        assert "[LOCAL_AGENT_ONLINE]" in status
        assert "128k tokens" in status
        assert "Fail-Fast enabled" in status


def test_query_local_model_success_mock():
    """Verify query_local_model parses chat completion choices and injects 128k footer."""
    mock_response_json = {
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": "Here is the refactored code."
                }
            }
        ],
        "usage": {
            "prompt_tokens": 1500,
            "completion_tokens": 120,
            "total_tokens": 1620
        }
    }

    mock_resp = MagicMock()
    mock_resp.read.return_value = json.dumps(mock_response_json).encode("utf-8")
    mock_resp.__enter__.return_value = mock_resp

    with patch("scripts.llama_mcp_server.probe_llama_server", return_value=(True, "OK", {})), \
         patch("urllib.request.urlopen", return_value=mock_resp):
        result = query_local_model(prompt="Refactor this function", context="def foo(): pass")
        assert "Here is the refactored code." in result
        assert "[Local Agent: llama.cpp | Tokens: 1500 prompt + 120 completion = 1620 total | Window: ~128k]" in result
