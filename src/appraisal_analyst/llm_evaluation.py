"""Evaluate contextual LLM analysis on the synthetic challenge set."""

from pathlib import Path
import time

import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)

from appraisal_analyst.llm import analyze_with_llm


DATA_PATH = Path("data/holdout_appraisals.csv")


def evaluate_label(
    actual: pd.Series,
    predicted: pd.Series,
    label_name: str,
) -> dict[str, object]:
    """Calculate classification metrics for one quality category."""

    true_negative, false_positive, false_negative, true_positive = (
        confusion_matrix(
            actual,
            predicted,
            labels=[False, True],
        ).ravel()
    )

    return {
        "label": label_name,
        "accuracy": accuracy_score(actual, predicted),
        "precision": precision_score(
            actual,
            predicted,
            zero_division=0,
        ),
        "recall": recall_score(
            actual,
            predicted,
            zero_division=0,
        ),
        "f1_score": f1_score(
            actual,
            predicted,
            zero_division=0,
        ),
        "true_positives": int(true_positive),
        "true_negatives": int(true_negative),
        "false_positives": int(false_positive),
        "false_negatives": int(false_negative),
    }


def run_llm_evaluation(
    data_path: Path = DATA_PATH,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Evaluate the contextual LLM on the challenge dataset."""

    dataset = pd.read_csv(data_path)
    prediction_records = []

    total_records = len(dataset)

    for index, row in dataset.iterrows():
        appraisal_id = str(row["appraisal_id"])

        print(
            f"Analyzing {index + 1}/{total_records}: "
            f"{appraisal_id}"
        )

        result = analyze_with_llm(
            comment=str(row["comment"]),
            rating=str(row["rating"]),
        )

        prediction_records.append(
            {
                "appraisal_id": appraisal_id,
                "llm_vagueness": result["vagueness"],
                "llm_missing_evidence": result["missing_evidence"],
                "llm_potential_bias": result["potential_bias"],
                "llm_rating_mismatch": result["rating_mismatch"],
                "llm_summary": result["summary"],
            }
        )

        # Small pause between requests to avoid unnecessary bursts.
        time.sleep(1)

    predictions = pd.DataFrame(prediction_records)

    evaluated_data = dataset.merge(
        predictions,
        on="appraisal_id",
        how="left",
    )

    evaluated_data["llm_revision"] = evaluated_data[
        [
            "llm_vagueness",
            "llm_missing_evidence",
            "llm_potential_bias",
            "llm_rating_mismatch",
        ]
    ].any(axis=1)

    label_pairs = [
        (
            "expected_vagueness",
            "llm_vagueness",
            "Vagueness",
        ),
        (
            "expected_missing_evidence",
            "llm_missing_evidence",
            "Missing Evidence",
        ),
        (
            "expected_potential_bias",
            "llm_potential_bias",
            "Potential Bias",
        ),
        (
            "expected_rating_mismatch",
            "llm_rating_mismatch",
            "Rating Mismatch",
        ),
        (
            "expected_revision",
            "llm_revision",
            "Overall Revision",
        ),
    ]

    metrics = []

    for expected_column, predicted_column, label_name in label_pairs:
        metrics.append(
            evaluate_label(
                evaluated_data[expected_column].astype(bool),
                evaluated_data[predicted_column].astype(bool),
                label_name,
            )
        )

    return evaluated_data, pd.DataFrame(metrics)


if __name__ == "__main__":
    evaluated_data, metrics = run_llm_evaluation()

    print("\nContextual LLM Evaluation Metrics\n")

    print(
        metrics.to_string(
            index=False,
            float_format=lambda value: f"{value:.2f}",
        )
    )

    print("\nExamples evaluated:", len(evaluated_data))