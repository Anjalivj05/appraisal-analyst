"""Streamlit interface for The Appraisal Analyst."""

import streamlit as st

from appraisal_analyst.review import analyze_appraisal
from appraisal_analyst.rules import SUPPORTED_RATINGS


st.set_page_config(
    page_title="The Appraisal Analyst",
    page_icon="📋",
    layout="wide",
)

CHECK_TITLES = {
    "minimum_word_count": "Comment Detail",
    "vague_phrases": "Vague Language",
    "personality_language": "Personality-Focused Language",
    "supporting_evidence": "Supporting Evidence",
    "rating_alignment": "Rating Alignment",
}


st.title("The Appraisal Analyst")

st.write(
    "Review employee performance-appraisal comments for clarity, "
    "supporting evidence, rating alignment, and potentially "
    "personality-focused language."
)

with st.container(border=True):
    st.subheader("Review an appraisal comment")

    rating = st.selectbox(
        "Performance rating",
        options=SUPPORTED_RATINGS,
    )

    comment = st.text_area(
        "Appraisal comment",
        height=180,
        placeholder=(
            "Example: Sarah exceeded her annual target by 18%, "
            "reduced reporting time, and mentored two new team members."
        ),
    )

    analyze_button = st.button(
        "Analyze comment",
        type="primary",
        use_container_width=True,
    )

if analyze_button:
    try:
        result = analyze_appraisal(comment, rating)
    except ValueError as error:
        st.warning(str(error))
    else:
        st.divider()
        st.subheader("Review result")

        if result["flagged_count"] > 0:
            st.error("Revision recommended")
        else:
            st.success("No rule-based concerns detected")

        metric_column_1, metric_column_2, metric_column_3 = st.columns(3)

        metric_column_1.metric(
            "Checks completed",
            result["total_checks"],
        )
        metric_column_2.metric(
            "Concerns identified",
            result["flagged_count"],
        )
        metric_column_3.metric(
            "Rating reviewed",
            result["rating"],
        )

        st.subheader("Quality checks")

        for check in result["checks"]:
            rule_id = str(check["rule_id"])
            title = CHECK_TITLES.get(rule_id, rule_id.replace("_", " ").title())

            with st.container(border=True):
                heading_column, status_column = st.columns([4, 1])

                heading_column.markdown(f"#### {title}")

                if check["flagged"]:
                    status_column.error("Review")
                else:
                    status_column.success("Passed")

                st.write(check["message"])

        with st.expander("Important use boundary"):
            st.write(
                "This application evaluates the quality of written appraisal "
                "comments. It does not determine employee ratings, promotions, "
                "compensation, discipline, hiring, or termination. Final review "
                "and decisions remain the responsibility of qualified HR "
                "professionals and managers."
            )