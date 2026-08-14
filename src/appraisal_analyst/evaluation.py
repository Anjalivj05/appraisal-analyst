"""Evaluate the rule-based appraisal review system."""

from pathlib import Path

import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)

from appraisal_analyst.review import analyze_appraisal


DATA_PATH = Path("data/synthetic_appraisals.csv")


def get_prediction_flags(
    comment: str,
    rating: str,
) -> dict[str, bool]:
    """Return predicted issue labels from the rule-based review."""

    result = analyze_appraisal(comment, rating)

    checks = {
        str(check["rule_id"]): bool(check["flagged"])
        for check in result["checks"]
    }

    predicted_vagueness = (
        checks.get("minimum_word_count", False)
        or checks.get("vague_phrases", False)
    )

    return {
        "predicted_vagueness": predicted_vagueness,
        "predicted_missing_evidence": checks.get(
            "supporting_evidence",
            False,
        ),
        "predicted_potential_bias": checks.get(
            "personality_language",
            False,
        ),
        "predicted_rating_mismatch": checks.get(
            "rating_alignment",
            False,
        ),
        "predicted_revision": result["flagged_count"] > 0,
    }


def evaluate_label(
    actual: pd.Series,
    predicted: pd.Series,
    label_name: str,
) -> dict[str, object]:
    """Calculate classification metrics for one appraisal-quality label."""

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


def run_evaluation(
    data_path: Path = DATA_PATH,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Run the rule engine against the labeled synthetic dataset."""

    dataset = pd.read_csv(data_path)

    prediction_records = []

    for _, row in dataset.iterrows():
        predictions = get_prediction_flags(
            comment=str(row["comment"]),
            rating=str(row["rating"]),
        )

        prediction_records.append(
            {
                "appraisal_id": row["appraisal_id"],
                **predictions,
            }
        )

    predictions_df = pd.DataFrame(prediction_records)

    evaluated_data = dataset.merge(
        predictions_df,
        on="appraisal_id",
        how="left",
    )

    label_pairs = [
        (
            "expected_vagueness",
            "predicted_vagueness",
            "Vagueness",
        ),
        (
            "expected_missing_evidence",
            "predicted_missing_evidence",
            "Missing Evidence",
        ),
        (
            "expected_potential_bias",
            "predicted_potential_bias",
            "Potential Bias",
        ),
        (
            "expected_rating_mismatch",
            "predicted_rating_mismatch",
            "Rating Mismatch",
        ),
        (
            "expected_revision",
            "predicted_revision",
            "Overall Revision",
        ),
    ]

    metric_records = []

    for expected_column, predicted_column, label_name in label_pairs:
        metrics = evaluate_label(
            evaluated_data[expected_column].astype(bool),
            evaluated_data[predicted_column].astype(bool),
            label_name,
        )

        metric_records.append(metrics)

    metrics_df = pd.DataFrame(metric_records)

    return evaluated_data, metrics_df


if __name__ == "__main__":
    evaluated_data, metrics = run_evaluation()

    print("\nRule-Based Evaluation Metrics\n")
    print(
        metrics.to_string(
            index=False,
            float_format=lambda value: f"{value:.2f}",
        )
    )

    print("\nExamples evaluated:", len(evaluated_data))