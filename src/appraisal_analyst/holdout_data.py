"""Generate a holdout synthetic dataset for rule-engine evaluation."""

from pathlib import Path

import pandas as pd


OUTPUT_PATH = Path("data/holdout_appraisals.csv")


def build_holdout_dataset() -> pd.DataFrame:
    """Create harder synthetic appraisal examples for holdout evaluation."""

    records = [
        {
            "appraisal_id": "H001",
            "department": "Engineering",
            "job_level": "Individual Contributor",
            "rating": "Meets Expectations",
            "comment": (
                "Provides dependable support to colleagues and consistently "
                "contributes across assigned responsibilities throughout the year."
            ),
            "expected_vagueness": True,
            "expected_missing_evidence": True,
            "expected_potential_bias": False,
            "expected_rating_mismatch": False,
            "expected_revision": True,
        },
        {
            "appraisal_id": "H002",
            "department": "Operations",
            "job_level": "Individual Contributor",
            "rating": "Exceeds Expectations",
            "comment": (
                "Built a reconciliation workflow that removed duplicate manual "
                "steps and gave analysts same-day results."
            ),
            "expected_vagueness": False,
            "expected_missing_evidence": False,
            "expected_potential_bias": False,
            "expected_rating_mismatch": False,
            "expected_revision": False,
        },
        {
            "appraisal_id": "H003",
            "department": "Marketing",
            "job_level": "Manager",
            "rating": "Meets Expectations",
            "comment": (
                "Her communication style can be abrasive in meetings even though "
                "her project work is consistently reliable."
            ),
            "expected_vagueness": False,
            "expected_missing_evidence": True,
            "expected_potential_bias": True,
            "expected_rating_mismatch": False,
            "expected_revision": True,
        },
        {
            "appraisal_id": "H004",
            "department": "Finance",
            "job_level": "Individual Contributor",
            "rating": "Meets Expectations",
            "comment": (
                "Work is often late and requires repeated correction before "
                "monthly reporting can be finalized."
            ),
            "expected_vagueness": False,
            "expected_missing_evidence": False,
            "expected_potential_bias": False,
            "expected_rating_mismatch": True,
            "expected_revision": True,
        },
        {
            "appraisal_id": "H005",
            "department": "Sales",
            "job_level": "Individual Contributor",
            "rating": "Outstanding",
            "comment": (
                "Closed complex enterprise opportunities, expanded strategic "
                "accounts, and became the primary resource for difficult client "
                "negotiations."
            ),
            "expected_vagueness": False,
            "expected_missing_evidence": False,
            "expected_potential_bias": False,
            "expected_rating_mismatch": False,
            "expected_revision": False,
        },
        {
            "appraisal_id": "H006",
            "department": "Human Resources",
            "job_level": "Manager",
            "rating": "Exceeds Expectations",
            "comment": (
                "She is not leadership material and can be difficult to work "
                "with despite completing her assigned responsibilities."
            ),
            "expected_vagueness": False,
            "expected_missing_evidence": True,
            "expected_potential_bias": True,
            "expected_rating_mismatch": True,
            "expected_revision": True,
        },
        {
            "appraisal_id": "H007",
            "department": "Engineering",
            "job_level": "Senior Individual Contributor",
            "rating": "Outstanding",
            "comment": (
                "Improved API response time by 34%, resolved two recurring "
                "production failures, and mentored three junior engineers."
            ),
            "expected_vagueness": False,
            "expected_missing_evidence": False,
            "expected_potential_bias": False,
            "expected_rating_mismatch": False,
            "expected_revision": False,
        },
        {
            "appraisal_id": "H008",
            "department": "Finance",
            "job_level": "Manager",
            "rating": "Needs Improvement",
            "comment": (
                "Produces accurate forecasts, supports executive planning, and "
                "is trusted with high-priority financial analysis."
            ),
            "expected_vagueness": False,
            "expected_missing_evidence": False,
            "expected_potential_bias": False,
            "expected_rating_mismatch": True,
            "expected_revision": True,
        },
        {
            "appraisal_id": "H009",
            "department": "Operations",
            "job_level": "Manager",
            "rating": "Meets Expectations",
            "comment": (
                "Coordinated the warehouse transition across three teams and "
                "maintained service continuity during the change."
            ),
            "expected_vagueness": False,
            "expected_missing_evidence": False,
            "expected_potential_bias": False,
            "expected_rating_mismatch": False,
            "expected_revision": False,
        },
        {
            "appraisal_id": "H010",
            "department": "Marketing",
            "job_level": "Individual Contributor",
            "rating": "Exceeds Expectations",
            "comment": (
                "Always brings great energy to the team and everyone enjoys "
                "working with her on campaigns."
            ),
            "expected_vagueness": True,
            "expected_missing_evidence": True,
            "expected_potential_bias": True,
            "expected_rating_mismatch": True,
            "expected_revision": True,
        },
        {
            "appraisal_id": "H011",
            "department": "Sales",
            "job_level": "Manager",
            "rating": "Unsatisfactory",
            "comment": (
                "Failed to submit required forecasts, missed client follow-ups, "
                "and had repeated errors in account documentation."
            ),
            "expected_vagueness": False,
            "expected_missing_evidence": False,
            "expected_potential_bias": False,
            "expected_rating_mismatch": False,
            "expected_revision": False,
        },
        {
            "appraisal_id": "H012",
            "department": "Human Resources",
            "job_level": "Individual Contributor",
            "rating": "Meets Expectations",
            "comment": (
                "Handled employee onboarding questions, coordinated orientation "
                "activities, and maintained accurate new-hire documentation."
            ),
            "expected_vagueness": False,
            "expected_missing_evidence": False,
            "expected_potential_bias": False,
            "expected_rating_mismatch": False,
            "expected_revision": False,
        },
    ]

    return pd.DataFrame(records)


def save_holdout_dataset() -> Path:
    """Build and save the holdout appraisal dataset."""
    dataset = build_holdout_dataset()

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    dataset.to_csv(OUTPUT_PATH, index=False)

    return OUTPUT_PATH


if __name__ == "__main__":
    saved_path = save_holdout_dataset()
    print(f"Holdout dataset saved to: {saved_path}")