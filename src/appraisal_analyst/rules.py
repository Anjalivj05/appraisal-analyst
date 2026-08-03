"""Rule-based checks for employee appraisal comments."""

import re
MINIMUM_WORD_COUNT = 10

VAGUE_PHRASES = [
    "good performer",
    "great employee",
    "does a good job",
    "meets expectations",
    "needs improvement",
    "works hard",
]

PERSONALITY_TERMS = [
    "attitude",
    "personality",
    "likeable",
    "unlikeable",
    "emotional",
    "fit",
]

EVIDENCE_TERMS = [
    "for example",
    "such as",
    "resulted in",
    "increased",
    "decreased",
    "reduced",
    "improved",
    "completed",
    "delivered",
    "achieved",
    "automated",
    "mentored",
    "resolved",
]

def count_words(comment: str) -> int:
    """Return the number of words in an appraisal comment."""
    return len(comment.strip().split())


def check_minimum_length(comment: str) -> dict[str, object]:
    """Check whether an appraisal comment contains enough detail."""
    word_count = count_words(comment)
    flagged = word_count < MINIMUM_WORD_COUNT

    if flagged:
        message = (
            f"Comment contains only {word_count} words. "
            f"Add specific examples or results to provide stronger evidence."
        )
    else:
        message = "Comment meets the minimum length requirement."

    return {
        "rule_id": "minimum_word_count",
        "category": "vagueness",
        "flagged": flagged,
        "message": message,
        "word_count": word_count,
        "minimum_word_count": MINIMUM_WORD_COUNT,
    }


def check_vague_phrases(comment: str) -> dict[str, object]:
    """Check whether an appraisal comment contains vague phrases."""
    normalized_comment = comment.lower()

    matched_phrases = [
        phrase
        for phrase in VAGUE_PHRASES
        if phrase in normalized_comment
    ]

    flagged = len(matched_phrases) > 0

    if flagged:
        message = (
            "Potentially vague wording found: "
            + ", ".join(matched_phrases)
            + ". Add specific actions, examples, or measurable results."
        )
    else:
        message = "No predefined vague phrases were found."

    return {
        "rule_id": "vague_phrases",
        "category": "vagueness",
        "flagged": flagged,
        "message": message,
        "matched_phrases": matched_phrases,
    }


def check_personality_language(comment: str) -> dict[str, object]:
    """Check for personality-focused terms in an appraisal comment."""
    normalized_comment = comment.lower()

    matched_terms = [
        term
        for term in PERSONALITY_TERMS
        if re.search(rf"\b{re.escape(term)}\b", normalized_comment)
    ]

    flagged = len(matched_terms) > 0

    if flagged:
        message = (
            "Potentially personality-focused language found: "
            + ", ".join(matched_terms)
            + ". Focus the feedback on observable work behavior and results."
        )
    else:
        message = "No predefined personality-focused terms were found."

    return {
        "rule_id": "personality_language",
        "category": "potential_bias",
        "flagged": flagged,
        "message": message,
        "matched_terms": matched_terms,
    }

def check_supporting_evidence(comment: str) -> dict[str, object]:
    """Check whether an appraisal comment includes supporting evidence."""
    normalized_comment = comment.lower()

    matched_terms = [
        term
        for term in EVIDENCE_TERMS
        if term in normalized_comment
    ]

    has_number = bool(
        re.search(r"\b\d+(?:\.\d+)?%?\b", normalized_comment)
    )

    flagged = not matched_terms and not has_number

    if flagged:
        message = (
            "No clear supporting evidence was found. "
            "Add a specific action, example, outcome, or measurable result."
        )
    else:
        message = "The comment contains possible supporting evidence."

    return {
        "rule_id": "supporting_evidence",
        "category": "missing_evidence",
        "flagged": flagged,
        "message": message,
        "matched_terms": matched_terms,
        "has_number": has_number,
    }


def run_rule_checks(comment: str) -> list[dict[str, object]]:
    """Run all rule-based quality checks on an appraisal comment."""
    return [
        check_minimum_length(comment),
        check_vague_phrases(comment),
        check_personality_language(comment),
        check_supporting_evidence(comment),
    ]
