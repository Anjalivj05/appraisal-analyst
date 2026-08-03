"""Tests for the rule-based appraisal checks."""

from appraisal_analyst.rules import (
    check_minimum_length,
    check_personality_language,
    check_rating_alignment,
    check_supporting_evidence,
    check_vague_phrases,
    run_rule_checks,
)


def test_short_comment_is_flagged() -> None:
    """A very short appraisal comment should be flagged."""
    result = check_minimum_length("Good performer")

    assert result["flagged"] is True
    assert result["word_count"] == 2


def test_vague_phrase_is_detected() -> None:
    """A predefined vague phrase should be detected."""
    result = check_vague_phrases(
        "John is a great employee and works hard."
    )

    assert result["flagged"] is True
    assert "great employee" in result["matched_phrases"]
    assert "works hard" in result["matched_phrases"]


def test_personality_language_is_detected() -> None:
    """Personality-focused language should be detected."""
    result = check_personality_language(
        "John has a positive attitude and is a good fit for the team."
    )

    assert result["flagged"] is True
    assert "attitude" in result["matched_terms"]
    assert "fit" in result["matched_terms"]


def test_fit_does_not_match_inside_another_word() -> None:
    """The word fit should not match inside a word such as benefit."""
    result = check_personality_language(
        "Her work created a significant benefit for the department."
    )

    assert "fit" not in result["matched_terms"]


def test_supporting_evidence_is_detected() -> None:
    """A measurable work result should count as possible evidence."""
    result = check_supporting_evidence(
        "Sarah reduced reporting time by 25%."
    )

    assert result["flagged"] is False
    assert result["has_number"] is True
    assert "reduced" in result["matched_terms"]


def test_combined_engine_returns_four_results() -> None:
    """The combined engine should execute all four current rules."""
    results = run_rule_checks("John is a good performer.")

    assert len(results) == 4

def test_unsupported_outstanding_comment_is_flagged() -> None:
    """An Outstanding rating without supporting language should be flagged."""
    result = check_rating_alignment(
        "John is a great employee with a positive attitude.",
        "Outstanding",
    )

    assert result["flagged"] is True
    assert result["rating"] == "Outstanding"


def test_evidence_based_high_rating_is_not_flagged() -> None:
    """Strong performance evidence should support a high rating."""
    result = check_rating_alignment(
        "Sarah exceeded her targets, improved reporting accuracy, "
        "and mentored two new employees.",
        "Exceeds Expectations",
    )

    assert result["flagged"] is False
    assert "exceeded" in result["matched_positive_terms"]
    assert "improved" in result["matched_positive_terms"]
    assert "mentored" in result["matched_positive_terms"]