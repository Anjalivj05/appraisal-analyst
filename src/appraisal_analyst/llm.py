"""Optional LLM-assisted analysis for appraisal comments."""

import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


SYSTEM_INSTRUCTIONS = """
You are assisting with the quality review of a draft employee
performance-appraisal comment.

Evaluate only the quality of the written feedback.

Consider:
1. Vagueness or generic wording
2. Missing supporting evidence or examples
3. Whether the written feedback appears to support the selected rating
4. Personality-focused or potentially inappropriate language
5. Whether the feedback could be made clearer or more actionable

Important boundaries:
- Do not decide whether the employee deserves the rating.
- Do not recommend promotion, compensation, discipline, hiring,
  or termination decisions.
- Do not infer protected characteristics.
- Treat possible bias as a review concern, not as a conclusion.
- Explain concerns using the wording contained in the comment.
- Keep the response concise and professional.
"""


def is_llm_configured() -> bool:
    """Return whether an OpenAI API key is available."""
    return bool(os.getenv("OPENAI_API_KEY"))


def analyze_with_llm(
    comment: str,
    rating: str,
) -> dict[str, str]:
    """Analyze an appraisal comment using the optional OpenAI LLM."""

    cleaned_comment = comment.strip()

    if not cleaned_comment:
        raise ValueError("Appraisal comment cannot be empty.")

    if not is_llm_configured():
        raise RuntimeError(
            "OpenAI API key is not configured. "
            "Add OPENAI_API_KEY to your local .env file."
        )

    model = os.getenv("OPENAI_MODEL", "gpt-5.5")

    client = OpenAI()

    user_input = f"""
Performance rating: {rating}

Appraisal comment:
{cleaned_comment}

Review the appraisal comment and provide:

- Overall comment-quality assessment
- Concerns identified
- Explanation of each concern
- Suggested improvements to the written feedback

Do not rewrite the employee's rating or make any employment decision.
"""

    response = client.responses.create(
        model=model,
        instructions=SYSTEM_INSTRUCTIONS,
        input=user_input,
    )

    return {
        "model": model,
        "analysis": response.output_text,
    }