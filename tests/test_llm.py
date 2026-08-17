"""Tests for the Cloudflare Workers AI integration."""

import pytest

from appraisal_analyst import llm


def test_llm_not_configured_without_credentials(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """LLM should be unavailable when Cloudflare credentials are missing."""
    monkeypatch.delenv("CLOUDFLARE_ACCOUNT_ID", raising=False)
    monkeypatch.delenv("CLOUDFLARE_API_TOKEN", raising=False)

    assert llm.is_llm_configured() is False


def test_llm_configured_with_credentials(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """LLM should be available when both credentials exist."""
    monkeypatch.setenv("CLOUDFLARE_ACCOUNT_ID", "test-account")
    monkeypatch.setenv("CLOUDFLARE_API_TOKEN", "test-token")

    assert llm.is_llm_configured() is True


def test_empty_comment_is_rejected(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Empty comments should be rejected before any API request."""
    monkeypatch.setenv("CLOUDFLARE_ACCOUNT_ID", "test-account")
    monkeypatch.setenv("CLOUDFLARE_API_TOKEN", "test-token")

    with pytest.raises(
        ValueError,
        match="Appraisal comment cannot be empty",
    ):
        llm.analyze_with_llm(
            "   ",
            "Meets Expectations",
        )


def test_missing_credentials_raise_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Analysis should fail safely when credentials are unavailable."""
    monkeypatch.delenv("CLOUDFLARE_ACCOUNT_ID", raising=False)
    monkeypatch.delenv("CLOUDFLARE_API_TOKEN", raising=False)

    with pytest.raises(
        RuntimeError,
        match="Cloudflare Workers AI is not configured",
    ):
        llm.analyze_with_llm(
            "Completed assigned work on time.",
            "Meets Expectations",
        )


def test_structured_response_parser() -> None:
    """Valid Cloudflare structured output should be parsed correctly."""
    response_data = {
        "result": {
            "response": {
                "vagueness": True,
                "missing_evidence": True,
                "potential_bias": False,
                "rating_mismatch": True,
                "summary": "The feedback is too general.",
                "suggestion": "Add specific performance examples.",
            }
        }
    }

    result = llm._parse_model_response(response_data)

    assert result["vagueness"] is True
    assert result["missing_evidence"] is True
    assert result["potential_bias"] is False
    assert result["rating_mismatch"] is True


def test_invalid_structured_response_is_rejected() -> None:
    """Incomplete LLM output should fail validation."""
    response_data = {
        "result": {
            "response": {
                "vagueness": True,
            }
        }
    }

    with pytest.raises(
        RuntimeError,
        match="missing required fields",
    ):
        llm._parse_model_response(response_data)