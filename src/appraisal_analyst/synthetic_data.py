"""Generate synthetic employee appraisal data for development and evaluation."""

from pathlib import Path

import pandas as pd


OUTPUT_PATH = Path("data/synthetic_appraisals.csv")


def build_synthetic_dataset() -> pd.DataFrame:
    """Create synthetic appraisal examples with reference quality labels."""

    records = [
        {
            "appraisal_id": "A001",
            "department": "Engineering",
            "job_level": "Individual Contributor",
            "rating": "Outstanding",
            "comment": (
                "John is a great employee with a positive attitude. "
                "Everyone likes working with him."
            ),
            "expected_vagueness": True,
            "expected_missing_evidence": True,
            "expected_potential_bias": True,
            "expected_rating_mismatch": True,
            "expected_revision": True,
        },
        {
            "appraisal_id": "A002",
            "department": "Finance",
            "job_level": "Individual Contributor",
            "rating": "Exceeds Expectations",
            "comment": (
                "Sarah exceeded her annual target by 18%, reduced reporting "
                "time, and mentored two new team members."
            ),
            "expected_vagueness": False,
            "expected_missing_evidence": False,
            "expected_potential_bias": False,
            "expected_rating_mismatch": False,
            "expected_revision": False,
        },
        {
            "appraisal_id": "A003",
            "department": "Marketing",
            "job_level": "Individual Contributor",
            "rating": "Meets Expectations",
            "comment": "Good performer.",
            "expected_vagueness": True,
            "expected_missing_evidence": True,
            "expected_potential_bias": False,
            "expected_rating_mismatch": False,
            "expected_revision": True,
        },
        {
            "appraisal_id": "A004",
            "department": "Operations",
            "job_level": "Manager",
            "rating": "Needs Improvement",
            "comment": (
                "Delivered all assigned reports on time and improved "
                "processing accuracy by 12%."
            ),
            "expected_vagueness": False,
            "expected_missing_evidence": False,
            "expected_potential_bias": False,
            "expected_rating_mismatch": True,
            "expected_revision": True,
        },
        {
            "appraisal_id": "A005",
            "department": "Sales",
            "job_level": "Individual Contributor",
            "rating": "Exceeds Expectations",
            "comment": (
                "Exceeded quarterly sales targets by 15% and increased "
                "renewal revenue across key accounts."
            ),
            "expected_vagueness": False,
            "expected_missing_evidence": False,
            "expected_potential_bias": False,
            "expected_rating_mismatch": False,
            "expected_revision": False,
        },
        {
            "appraisal_id": "A006",
            "department": "Human Resources",
            "job_level": "Manager",
            "rating": "Meets Expectations",
            "comment": (
                "Works hard and does a good job supporting the team."
            ),
            "expected_vagueness": True,
            "expected_missing_evidence": True,
            "expected_potential_bias": False,
            "expected_rating_mismatch": False,
            "expected_revision": True,
        },
        {
            "appraisal_id": "A007",
            "department": "Engineering",
            "job_level": "Senior Individual Contributor",
            "rating": "Outstanding",
            "comment": (
                "Led the migration of three reporting pipelines, reduced "
                "processing time by 32%, and mentored four engineers."
            ),
            "expected_vagueness": False,
            "expected_missing_evidence": False,
            "expected_potential_bias": False,
            "expected_rating_mismatch": False,
            "expected_revision": False,
        },
        {
            "appraisal_id": "A008",
            "department": "Finance",
            "job_level": "Individual Contributor",
            "rating": "Meets Expectations",
            "comment": (
                "Reliable employee with a likeable personality and a good "
                "fit for the finance team."
            ),
            "expected_vagueness": False,
            "expected_missing_evidence": True,
            "expected_potential_bias": True,
            "expected_rating_mismatch": False,
            "expected_revision": True,
        },
        {
            "appraisal_id": "A009",
            "department": "Marketing",
            "job_level": "Manager",
            "rating": "Exceeds Expectations",
            "comment": (
                "Improved campaign conversion by 21% and delivered the "
                "annual product launch two weeks ahead of schedule."
            ),
            "expected_vagueness": False,
            "expected_missing_evidence": False,
            "expected_potential_bias": False,
            "expected_rating_mismatch": False,
            "expected_revision": False,
        },
        {
            "appraisal_id": "A010",
            "department": "Sales",
            "job_level": "Individual Contributor",
            "rating": "Needs Improvement",
            "comment": (
                "Exceeded quota in every quarter and increased revenue "
                "from strategic accounts by 17%."
            ),
            "expected_vagueness": False,
            "expected_missing_evidence": False,
            "expected_potential_bias": False,
            "expected_rating_mismatch": True,
            "expected_revision": True,
        },
        {
            "appraisal_id": "A011",
            "department": "Operations",
            "job_level": "Individual Contributor",
            "rating": "Needs Improvement",
            "comment": (
                "Missed three monthly reporting deadlines and had repeated "
                "errors that required additional review."
            ),
            "expected_vagueness": False,
            "expected_missing_evidence": False,
            "expected_potential_bias": False,
            "expected_rating_mismatch": False,
            "expected_revision": False,
        },
        {
            "appraisal_id": "A012",
            "department": "Human Resources",
            "job_level": "Individual Contributor",
            "rating": "Unsatisfactory",
            "comment": (
                "Needs improvement."
            ),
            "expected_vagueness": True,
            "expected_missing_evidence": True,
            "expected_potential_bias": False,
            "expected_rating_mismatch": False,
            "expected_revision": True,
        },
        {
            "appraisal_id": "A013",
            "department": "Engineering",
            "job_level": "Manager",
            "rating": "Outstanding",
            "comment": (
                "Strong technical leader who delivered the platform upgrade "
                "and reduced production incidents by 28%."
            ),
            "expected_vagueness": False,
            "expected_missing_evidence": False,
            "expected_potential_bias": False,
            "expected_rating_mismatch": False,
            "expected_revision": False,
        },
        {
            "appraisal_id": "A014",
            "department": "Finance",
            "job_level": "Manager",
            "rating": "Exceeds Expectations",
            "comment": (
                "Has a difficult personality but produced accurate monthly "
                "financial reports."
            ),
            "expected_vagueness": False,
            "expected_missing_evidence": True,
            "expected_potential_bias": True,
            "expected_rating_mismatch": True,
            "expected_revision": True,
        },
        {
            "appraisal_id": "A015",
            "department": "Marketing",
            "job_level": "Individual Contributor",
            "rating": "Meets Expectations",
            "comment": (
                "Completed all scheduled campaign reports and delivered "
                "weekly performance updates to stakeholders."
            ),
            "expected_vagueness": False,
            "expected_missing_evidence": False,
            "expected_potential_bias": False,
            "expected_rating_mismatch": False,
            "expected_revision": False,
        },
        {
            "appraisal_id": "A016",
            "department": "Sales",
            "job_level": "Manager",
            "rating": "Outstanding",
            "comment": (
                "Great employee who works hard and has the right attitude."
            ),
            "expected_vagueness": True,
            "expected_missing_evidence": True,
            "expected_potential_bias": True,
            "expected_rating_mismatch": True,
            "expected_revision": True,
        },
        {
            "appraisal_id": "A017",
            "department": "Operations",
            "job_level": "Manager",
            "rating": "Unsatisfactory",
            "comment": (
                "Missed five critical deadlines, failed to complete required "
                "quality checks, and created repeated processing errors."
            ),
            "expected_vagueness": False,
            "expected_missing_evidence": False,
            "expected_potential_bias": False,
            "expected_rating_mismatch": False,
            "expected_revision": False,
        },
        {
            "appraisal_id": "A018",
            "department": "Human Resources",
            "job_level": "Manager",
            "rating": "Exceeds Expectations",
            "comment": (
                "Reduced onboarding processing time by 24%, automated two "
                "manual reporting activities, and improved completion rates."
            ),
            "expected_vagueness": False,
            "expected_missing_evidence": False,
            "expected_potential_bias": False,
            "expected_rating_mismatch": False,
            "expected_revision": False,
        },
        {
            "appraisal_id": "A019",
            "department": "Engineering",
            "job_level": "Individual Contributor",
            "rating": "Meets Expectations",
            "comment": (
                "Consistently meets expectations across all areas."
            ),
            "expected_vagueness": True,
            "expected_missing_evidence": True,
            "expected_potential_bias": False,
            "expected_rating_mismatch": False,
            "expected_revision": True,
        },
        {
            "appraisal_id": "A020",
            "department": "Finance",
            "job_level": "Senior Individual Contributor",
            "rating": "Outstanding",
            "comment": (
                "Improved forecasting accuracy by 19%, delivered the annual "
                "budget ahead of schedule, and led automation of monthly "
                "variance reporting."
            ),
            "expected_vagueness": False,
            "expected_missing_evidence": False,
            "expected_potential_bias": False,
            "expected_rating_mismatch": False,
            "expected_revision": False,
        },
    ]

    return pd.DataFrame(records)


def save_synthetic_dataset() -> Path:
    """Build and save the synthetic appraisal dataset as a CSV file."""
    dataset = build_synthetic_dataset()

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    dataset.to_csv(OUTPUT_PATH, index=False)

    return OUTPUT_PATH


if __name__ == "__main__":
    saved_path = save_synthetic_dataset()
    print(f"Synthetic dataset saved to: {saved_path}")