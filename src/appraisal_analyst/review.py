"""Appraisal review service for combining rule-based results."""

from appraisal_analyst.rules import run_rule_checks


def analyze_appraisal(
    comment: str,
    rating: str | None = None,
) -> dict[str, object]:
    """Analyze an appraisal comment and summarize the rule results."""
    cleaned_comment = comment.strip()

    if not cleaned_comment:
        raise ValueError("Appraisal comment cannot be empty.")

    checks = run_rule_checks(cleaned_comment, rating)
    flagged_checks = [
        check for check in checks if check["flagged"] is True
    ]

    if flagged_checks:
        review_status = "Revision recommended"
    else:
        review_status = "No rule-based concerns detected"

    return {
        "comment": cleaned_comment,
        "rating": rating,
        "review_status": review_status,
        "total_checks": len(checks),
        "flagged_count": len(flagged_checks),
        "flagged_categories": sorted(
            {
                str(check["category"])
                for check in flagged_checks
            }
        ),
        "checks": checks,
    }