"""Tests for the appraisal review service."""

import pytest

from appraisal_analyst.review import analyze_appraisal


def test_weak_appraisal_recommends_revision() -> None:
    """A weak appraisal should produce a revision recommendation."""
    result = analyze_appraisal(
        "John is a great employee with a positive attitude. "
        "Everyone likes working with him.",
        "Outstanding",
    )

    assert result["review_status"] == "Revision recommended"
    assert result["total_checks"] == 5
    assert result["flagged_count"] == 4
    assert "vagueness" in result["flagged_categories"]
    assert "missing_evidence" in result["flagged_categories"]
    assert "potential_bias" in result["flagged_categories"]
    assert "rating_mismatch" in result["flagged_categories"]


def test_strong_appraisal_has_no_detected_concerns() -> None:
    """A specific, evidence-based appraisal should pass current rules."""
    result = analyze_appraisal(
        "Sarah exceeded her annual target by 18%, reduced reporting "
        "time, and mentored two new team members.",
        "Exceeds Expectations",
    )

    assert result["review_status"] == "No rule-based concerns detected"
    assert result["flagged_count"] == 0


def test_empty_comment_raises_error() -> None:
    """An empty appraisal comment should not be accepted."""
    with pytest.raises(
        ValueError,
        match="Appraisal comment cannot be empty",
    ):
        analyze_appraisal("   ", "Meets Expectations")