"""Tests for the optional LLM integration."""

import pytest

from appraisal_analyst import llm


def test_llm_not_configured_without_api_key(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """LLM should report unavailable when no API key is configured."""
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    assert llm.is_llm_configured() is False


def test_llm_requires_api_key(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """LLM analysis should fail safely when no API key is configured."""
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    with pytest.raises(
        RuntimeError,
        match="OpenAI API key is not configured",
    ):
        llm.analyze_with_llm(
            "John is a great employee.",
            "Outstanding",
        )


def test_empty_comment_is_rejected(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Empty comments should be rejected before any API request."""
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")

    with pytest.raises(
        ValueError,
        match="Appraisal comment cannot be empty",
    ):
        llm.analyze_with_llm(
            "   ",
            "Meets Expectations",
        )