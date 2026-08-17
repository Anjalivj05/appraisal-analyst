"""Contextual appraisal analysis using Cloudflare Workers AI."""

import json
import os
import time

import requests
from dotenv import load_dotenv


load_dotenv()


DEFAULT_MODEL = "@cf/meta/llama-3.3-70b-instruct-fp8-fast"


SYSTEM_INSTRUCTIONS = """
You review the quality of draft employee performance-appraisal comments.

Evaluate only the written feedback. Do not make employment decisions.

Use these definitions:

Vagueness:
Flag when feedback is generic, subjective, or does not clearly describe
what the employee actually did.

Missing evidence:
Flag when the comment lacks concrete examples, observable work behavior,
outcomes, achievements, errors, deadlines, metrics, or other supporting
performance evidence.

Potential bias:
Flag personality-, popularity-, likability-, temperament-, culture-fit-,
or identity-focused wording that is not clearly tied to observable job
behavior. A flag is only a review concern and does not mean discrimination
occurred.

Rating mismatch:
Flag when the written evidence does not appear sufficient to support the
selected rating, or when the overall meaning of the comment appears
inconsistent with the rating.

Important boundaries:
- Do not decide whether the employee deserves the rating.
- Do not recommend promotion, compensation, discipline, hiring,
  or termination.
- Do not infer protected characteristics.
- Do not invent facts not present in the comment.
- Base every conclusion on the supplied text.
- Keep explanations concise and professional.
"""


RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "vagueness": {"type": "boolean"},
        "missing_evidence": {"type": "boolean"},
        "potential_bias": {"type": "boolean"},
        "rating_mismatch": {"type": "boolean"},
        "summary": {"type": "string"},
        "suggestion": {"type": "string"},
    },
    "required": [
        "vagueness",
        "missing_evidence",
        "potential_bias",
        "rating_mismatch",
        "summary",
        "suggestion",
    ],
}


def is_llm_configured() -> bool:
    """Return whether Cloudflare Workers AI credentials are configured."""
    return bool(
        os.getenv("CLOUDFLARE_ACCOUNT_ID")
        and os.getenv("CLOUDFLARE_API_TOKEN")
    )


def _parse_model_response(
    response_data: dict,
) -> dict[str, object]:
    """Extract and validate structured output from Workers AI."""

    try:
        result = response_data["result"]
        raw_response = result["response"]
    except (KeyError, TypeError) as error:
        raise RuntimeError(
            "Cloudflare Workers AI returned an unexpected response format."
        ) from error

    if isinstance(raw_response, dict):
        analysis = raw_response

    elif isinstance(raw_response, str):
        try:
            analysis = json.loads(raw_response)
        except json.JSONDecodeError as error:
            raise RuntimeError(
                "Cloudflare Workers AI returned invalid JSON."
            ) from error

    else:
        raise RuntimeError(
            "Cloudflare Workers AI returned an unsupported response format."
        )

    required_fields = {
        "vagueness",
        "missing_evidence",
        "potential_bias",
        "rating_mismatch",
        "summary",
        "suggestion",
    }

    if not required_fields.issubset(analysis):
        raise RuntimeError(
            "Cloudflare Workers AI response is missing required fields."
        )

    boolean_fields = {
        "vagueness",
        "missing_evidence",
        "potential_bias",
        "rating_mismatch",
    }

    if any(
        not isinstance(analysis[field], bool)
        for field in boolean_fields
    ):
        raise RuntimeError(
            "Cloudflare Workers AI returned invalid category values."
        )

    if not isinstance(analysis["summary"], str):
        raise RuntimeError(
            "Cloudflare Workers AI returned an invalid summary."
        )

    if not isinstance(analysis["suggestion"], str):
        raise RuntimeError(
            "Cloudflare Workers AI returned an invalid suggestion."
        )

    return analysis


def analyze_with_llm(
    comment: str,
    rating: str,
) -> dict[str, object]:
    """Analyze an appraisal comment using Cloudflare Workers AI."""

    cleaned_comment = comment.strip()

    if not cleaned_comment:
        raise ValueError("Appraisal comment cannot be empty.")

    account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID")
    api_token = os.getenv("CLOUDFLARE_API_TOKEN")
    model = os.getenv("CLOUDFLARE_MODEL", DEFAULT_MODEL)

    if not account_id or not api_token:
        raise RuntimeError(
            "Cloudflare Workers AI is not configured."
        )

    url = (
        "https://api.cloudflare.com/client/v4/accounts/"
        f"{account_id}/ai/run/{model}"
    )

    user_input = (
        f"Performance rating: {rating}\n\n"
        f"Appraisal comment:\n{cleaned_comment}\n\n"
        "Evaluate this comment using the four review-quality categories."
    )

    payload = {
        "messages": [
            {
                "role": "system",
                "content": SYSTEM_INSTRUCTIONS,
            },
            {
                "role": "user",
                "content": user_input,
            },
        ],
        "response_format": {
            "type": "json_schema",
            "json_schema": RESPONSE_SCHEMA,
        },
        "max_tokens": 500,
        "temperature": 0.2,
    }

    response = None
    last_error = None

    for attempt in range(2):
        try:
            response = requests.post(
                url,
                headers={
                    "Authorization": f"Bearer {api_token}",
                },
                json=payload,
                timeout=(10, 90),
            )

            if response.status_code in {
                429,
                500,
                502,
                503,
                504,
            }:
                if attempt == 0:
                    time.sleep(2)
                    continue

            break

        except (
            requests.Timeout,
            requests.ConnectionError,
        ) as error:
            last_error = error

            if attempt == 0:
                time.sleep(2)
                continue

        except requests.RequestException as error:
            raise RuntimeError(
                "Unable to reach Cloudflare Workers AI."
            ) from error

    if response is None:
        raise RuntimeError(
            "Cloudflare Workers AI temporarily timed out. "
            "Please try the analysis again."
        ) from last_error

    if response.status_code != 200:
        raise RuntimeError(
            "Cloudflare Workers AI request failed "
            f"with status {response.status_code}."
        )

    try:
        response_data = response.json()
    except ValueError as error:
        raise RuntimeError(
            "Cloudflare Workers AI returned an invalid API response."
        ) from error

    if response_data.get("success") is not True:
        errors = response_data.get("errors", [])

        if errors:
            error_message = str(
                errors[0].get(
                    "message",
                    "Unknown error",
                )
            )
        else:
            error_message = "Unknown error"

        raise RuntimeError(
            f"Cloudflare Workers AI request failed: {error_message}"
        )

    analysis = _parse_model_response(response_data)

    usage = response_data.get(
        "result",
        {},
    ).get(
        "usage",
        {},
    )

    return {
        "provider": "Cloudflare Workers AI",
        "model": model,
        "vagueness": analysis["vagueness"],
        "missing_evidence": analysis["missing_evidence"],
        "potential_bias": analysis["potential_bias"],
        "rating_mismatch": analysis["rating_mismatch"],
        "summary": analysis["summary"],
        "suggestion": analysis["suggestion"],
        "usage": {
            "prompt_tokens": usage.get("prompt_tokens"),
            "completion_tokens": usage.get("completion_tokens"),
            "total_tokens": usage.get("total_tokens"),
            "neurons": usage.get("neurons"),
        },
    }