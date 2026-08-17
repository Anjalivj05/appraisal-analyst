"""Streamlit interface for The Appraisal Analyst."""

import streamlit as st

from appraisal_analyst.llm import analyze_with_llm, is_llm_configured
from appraisal_analyst.review import analyze_appraisal
from appraisal_analyst.rules import SUPPORTED_RATINGS


# -------------------------------------------------------------------
# Page setup
# -------------------------------------------------------------------

st.set_page_config(
    page_title="The Appraisal Analyst",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# -------------------------------------------------------------------
# Styling
# -------------------------------------------------------------------

st.html(
    """
    <style>
        .block-container {
            max-width: 1180px;
            padding-top: 1.5rem;
            padding-bottom: 3.5rem;
        }

        .hero {
            background:
                radial-gradient(
                    circle at 90% 10%,
                    rgba(45, 212, 191, 0.30),
                    transparent 30%
                ),
                linear-gradient(
                    135deg,
                    #0f172a 0%,
                    #1e3a8a 55%,
                    #0f766e 100%
                );
            border-radius: 26px;
            padding: 42px 46px 38px 46px;
            margin-bottom: 28px;
            box-shadow: 0 18px 45px rgba(15, 23, 42, 0.18);
        }

        .hero-eyebrow {
            color: #67e8f9;
            font-size: 0.78rem;
            font-weight: 750;
            letter-spacing: 0.14em;
            text-transform: uppercase;
            margin-bottom: 13px;
        }

        .hero-title {
            color: #ffffff;
            font-size: 3rem;
            font-weight: 780;
            line-height: 1.05;
            letter-spacing: -0.03em;
            margin-bottom: 18px;
        }

        .hero-description {
            color: #e2e8f0;
            font-size: 1.08rem;
            line-height: 1.7;
            max-width: 900px;
            margin: 0;
        }

        .hero-pills {
            display: flex;
            flex-wrap: wrap;
            gap: 9px;
            margin-top: 24px;
        }

        .hero-pill {
            color: #f8fafc;
            background: rgba(255, 255, 255, 0.10);
            border: 1px solid rgba(255, 255, 255, 0.20);
            border-radius: 999px;
            padding: 7px 13px;
            font-size: 0.82rem;
            font-weight: 500;
        }

        .section-label {
            color: #475569;
            font-size: 0.76rem;
            font-weight: 750;
            letter-spacing: 0.11em;
            text-transform: uppercase;
            margin-bottom: 3px;
        }

        .workflow-card {
            min-height: 125px;
            border: 1px solid #e2e8f0;
            border-radius: 18px;
            padding: 19px 20px;
            background: #ffffff;
            box-shadow: 0 5px 18px rgba(15, 23, 42, 0.04);
        }

        .workflow-number {
            color: #0f766e;
            font-size: 0.76rem;
            font-weight: 800;
            letter-spacing: 0.09em;
            text-transform: uppercase;
            margin-bottom: 7px;
        }

        .workflow-title {
            color: #0f172a;
            font-size: 1rem;
            font-weight: 700;
            margin-bottom: 5px;
        }

        .workflow-text {
            color: #64748b;
            font-size: 0.88rem;
            line-height: 1.5;
        }

        .reviewed-card {
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 16px;
            padding: 16px 19px;
            margin: 7px 0 18px 0;
        }

        .reviewed-label {
            color: #64748b;
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin-bottom: 5px;
        }

        .reviewed-value {
            color: #0f172a;
            font-size: 1rem;
            margin: 0;
        }

        .app-footer {
            text-align: center;
            color: #94a3b8;
            font-size: 0.80rem;
            padding-top: 30px;
        }

        div[data-testid="stFormSubmitButton"] button {
            min-height: 46px;
            border-radius: 10px;
            font-weight: 650;
        }
    </style>
    """
)


# -------------------------------------------------------------------
# Display names
# -------------------------------------------------------------------

CHECK_TITLES = {
    "minimum_word_count": "Comment Detail",
    "vague_phrases": "Vague Language",
    "personality_language": "Personality-Focused Language",
    "supporting_evidence": "Supporting Evidence",
    "rating_alignment": "Rating Alignment",
}


CATEGORY_TITLES = {
    "vagueness": "Vagueness",
    "missing_evidence": "Missing Evidence",
    "potential_bias": "Potentially Biased Language",
    "rating_mismatch": "Rating Alignment",
}


# -------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------

@st.cache_data(show_spinner=False, ttl=3600)
def cached_llm_analysis(
    comment: str,
    rating: str,
) -> dict[str, object]:
    """Cache identical LLM requests for one hour."""
    return analyze_with_llm(comment, rating)


def get_rule_category_flags(
    rule_result: dict[str, object],
) -> dict[str, bool]:
    """Convert detailed rule checks into the four comparison categories."""

    checks = {
        str(check["rule_id"]): bool(check["flagged"])
        for check in rule_result["checks"]
    }

    return {
        "vagueness": (
            checks.get("minimum_word_count", False)
            or checks.get("vague_phrases", False)
        ),
        "missing_evidence": checks.get(
            "supporting_evidence",
            False,
        ),
        "potential_bias": checks.get(
            "personality_language",
            False,
        ),
        "rating_mismatch": checks.get(
            "rating_alignment",
            False,
        ),
    }


def show_status(flagged: bool) -> None:
    """Display a simple status indicator."""

    if flagged:
        st.warning("⚠️ Review")
    else:
        st.success("✓ No concern")


def render_comparison_card(
    title: str,
    rule_flagged: bool,
    ai_flagged: bool,
) -> None:
    """Display one rule-vs-LLM comparison."""

    with st.container(border=True):
        st.markdown(f"#### {title}")

        rule_col, ai_col = st.columns(2)

        with rule_col:
            st.caption("RULE-BASED")
            show_status(rule_flagged)

        with ai_col:
            st.caption("CONTEXTUAL AI")
            show_status(ai_flagged)

        if rule_flagged == ai_flagged:
            st.caption("✓ Both approaches agree")
        else:
            st.caption(
                "↔ The two approaches interpret this differently"
            )


# -------------------------------------------------------------------
# Hero
# -------------------------------------------------------------------

st.html(
    """
    <div class="hero">

        <div class="hero-eyebrow">
            HR Analytics • NLP • Applied AI
        </div>

        <div class="hero-title">
            The Appraisal Analyst
        </div>

        <p class="hero-description">
            Review employee performance-feedback comments using two
            different approaches: a transparent rule-based baseline and
            a context-aware large language model (LLM).
            Compare what each approach finds and where their judgments differ.
        </p>

        <div class="hero-pills">
            <span class="hero-pill">Rule-Based NLP</span>
            <span class="hero-pill">Llama 3.3 70B</span>
            <span class="hero-pill">Side-by-Side Comparison</span>
            <span class="hero-pill">Synthetic-Data Evaluation</span>
        </div>

    </div>
    """
)


# -------------------------------------------------------------------
# Quick explanation
# -------------------------------------------------------------------

st.html(
    """
    <div class="section-label">
        How it works
    </div>
    """
)

st.subheader("Two approaches. One appraisal comment.")

workflow_1, workflow_2, workflow_3 = st.columns(
    3,
    gap="medium",
)

with workflow_1:
    st.html(
        """
        <div class="workflow-card">
            <div class="workflow-number">Step 01</div>
            <div class="workflow-title">Enter the feedback</div>
            <div class="workflow-text">
                Select a performance rating and enter a draft
                appraisal comment.
            </div>
        </div>
        """
    )

with workflow_2:
    st.html(
        """
        <div class="workflow-card">
            <div class="workflow-number">Step 02</div>
            <div class="workflow-title">Run both analyses</div>
            <div class="workflow-text">
                Python rules check known patterns while the
                large language model evaluates the full context.
            </div>
        </div>
        """
    )

with workflow_3:
    st.html(
        """
        <div class="workflow-card">
            <div class="workflow-number">Step 03</div>
            <div class="workflow-title">Compare the results</div>
            <div class="workflow-text">
                See where the two approaches agree, disagree,
                and what could improve the written feedback.
            </div>
        </div>
        """
    )

st.write("")

st.info(
    "The app reviews four areas: **vagueness, supporting evidence, "
    "potentially biased language, and rating alignment.**"
)


# -------------------------------------------------------------------
# Input
# -------------------------------------------------------------------

st.divider()

st.html(
    """
    <div class="section-label">
        Try the application
    </div>
    """
)

st.subheader("Review an appraisal comment")

st.caption(
    "Use synthetic or non-sensitive text in this public portfolio prototype."
)

with st.form(
    "appraisal_form",
    border=True,
):

    input_left, input_right = st.columns(
        [1, 2.3],
        gap="large",
    )

    with input_left:

        rating = st.selectbox(
            "Performance rating",
            options=SUPPORTED_RATINGS,
            help=(
                "The rating is used only to check whether "
                "the written feedback appears to support it."
            ),
        )

        st.caption(
            "The application reviews the written feedback. "
            "It does not determine the employee's rating."
        )

    with input_right:

        comment = st.text_area(
            "Appraisal comment",
            height=170,
            max_chars=2500,
            placeholder=(
                "Example: Sarah exceeded her annual target by 18%, "
                "reduced reporting time, and mentored two new team members."
            ),
        )

    submitted = st.form_submit_button(
        "Analyze Comment",
        type="primary",
        use_container_width=True,
    )


# -------------------------------------------------------------------
# Run analysis
# -------------------------------------------------------------------

if submitted:

    cleaned_comment = comment.strip()

    if not cleaned_comment:

        st.warning(
            "Please enter an appraisal comment before analyzing."
        )

    else:

        try:

            rule_result = analyze_appraisal(
                cleaned_comment,
                rating,
            )

        except ValueError as error:

            st.error(str(error))

        else:

            st.session_state["rule_result"] = rule_result
            st.session_state["reviewed_comment"] = cleaned_comment
            st.session_state["reviewed_rating"] = rating

            # Scroll only after a newly submitted analysis.
            st.session_state["scroll_to_results"] = True

            if is_llm_configured():

                try:

                    with st.spinner(
                        "Analyzing the comment..."
                    ):

                        llm_result = cached_llm_analysis(
                            cleaned_comment,
                            rating,
                        )

                    st.session_state["llm_result"] = llm_result
                    st.session_state["llm_error"] = None

                except RuntimeError as error:

                    st.session_state["llm_result"] = None
                    st.session_state["llm_error"] = str(error)

            else:

                st.session_state["llm_result"] = None
                st.session_state["llm_error"] = (
                    "Contextual AI is not currently configured."
                )


# -------------------------------------------------------------------
# Results
# -------------------------------------------------------------------

if "rule_result" in st.session_state:

    # Invisible target used by the smooth-scroll script.
    st.html('<div id="analysis-results-anchor"></div>')

    rule_result = st.session_state["rule_result"]
    reviewed_comment = st.session_state["reviewed_comment"]
    reviewed_rating = st.session_state["reviewed_rating"]

    llm_result = st.session_state.get("llm_result")
    llm_error = st.session_state.get("llm_error")

    rule_flags = get_rule_category_flags(rule_result)
    rule_concern_count = sum(rule_flags.values())

    if llm_result:

        llm_flags = {
            category: bool(llm_result[category])
            for category in CATEGORY_TITLES
        }

        llm_concern_count = sum(llm_flags.values())

        agreement_count = sum(
            rule_flags[category] == llm_flags[category]
            for category in CATEGORY_TITLES
        )

    else:

        llm_flags = {}
        llm_concern_count = None
        agreement_count = None


    st.divider()

    st.html(
        """
        <div class="section-label">
            Analysis complete
        </div>
        """
    )

    st.header("Review Results")


    # Overall result

    if llm_result:

        if (
            rule_concern_count == 0
            and llm_concern_count == 0
        ):

            st.success(
                "✓ No quality concerns were identified by either approach."
            )

        else:

            st.warning(
                "⚠️ The written feedback contains areas worth reviewing."
            )

    else:

        if rule_concern_count == 0:

            st.success(
                "✓ No rule-based quality concerns were identified."
            )

        else:

            st.warning(
                "⚠️ The rule-based baseline found areas worth reviewing."
            )


    st.html(
        f"""
        <div class="reviewed-card">
            <div class="reviewed-label">
                Rating reviewed
            </div>
            <p class="reviewed-value">
                <strong>{reviewed_rating}</strong>
            </p>
        </div>
        """
    )


    with st.expander(
        "View submitted comment",
        expanded=False,
    ):

        st.write(reviewed_comment)


    # Metrics

    metric_1, metric_2, metric_3 = st.columns(3)

    with metric_1:

        st.metric(
            "Rule-Based Flags",
            f"{rule_concern_count} / 4",
        )

    with metric_2:

        if llm_concern_count is not None:

            st.metric(
                "Contextual AI Flags",
                f"{llm_concern_count} / 4",
            )

        else:

            st.metric(
                "Contextual AI Flags",
                "Unavailable",
            )

    with metric_3:

        if agreement_count is not None:

            st.metric(
                "Approach Agreement",
                f"{agreement_count} / 4",
            )

        else:

            st.metric(
                "Approach Agreement",
                "N/A",
            )


    # Tabs

    comparison_tab, rules_tab, ai_tab = st.tabs(
        [
            "🔎 Compare",
            "🧩 Rule-Based",
            "✨ Contextual AI",
        ]
    )


    # ---------------------------------------------------------------
    # Comparison tab
    # ---------------------------------------------------------------

    with comparison_tab:

        st.subheader("Rule-Based vs Contextual AI")

        st.write(
            "Both approaches review the same four quality areas, "
            "but they reach their results differently."
        )

        if llm_result:

            categories = list(CATEGORY_TITLES.items())

            row_1_left, row_1_right = st.columns(
                2,
                gap="medium",
            )

            with row_1_left:

                category, title = categories[0]

                render_comparison_card(
                    title,
                    rule_flags[category],
                    llm_flags[category],
                )

            with row_1_right:

                category, title = categories[1]

                render_comparison_card(
                    title,
                    rule_flags[category],
                    llm_flags[category],
                )


            row_2_left, row_2_right = st.columns(
                2,
                gap="medium",
            )

            with row_2_left:

                category, title = categories[2]

                render_comparison_card(
                    title,
                    rule_flags[category],
                    llm_flags[category],
                )

            with row_2_right:

                category, title = categories[3]

                render_comparison_card(
                    title,
                    rule_flags[category],
                    llm_flags[category],
                )


            disagreement_count = 4 - agreement_count

            if disagreement_count == 0:

                st.success(
                    "The two approaches agree across all four "
                    "quality checks."
                )

            else:

                st.info(
                    f"The approaches disagree on "
                    f"{disagreement_count} of 4 checks. "
                    "That difference is useful: the rule-based system "
                    "is deterministic, while the language model can "
                    "interpret wording and context."
                )

        else:

            st.warning(
                "Contextual AI is temporarily unavailable. "
                "The rule-based results are still available."
            )


    # ---------------------------------------------------------------
    # Rule-based tab
    # ---------------------------------------------------------------

    with rules_tab:

        st.subheader("Transparent Rule-Based Baseline")

        st.write(
            "The baseline uses predefined phrases, word-count checks, "
            "evidence terms, and rating-alignment rules."
        )

        for check in rule_result["checks"]:

            rule_id = str(check["rule_id"])

            title = CHECK_TITLES.get(
                rule_id,
                rule_id.replace("_", " ").title(),
            )

            with st.container(border=True):

                title_col, status_col = st.columns(
                    [4, 1],
                    vertical_alignment="center",
                )

                with title_col:

                    st.markdown(f"#### {title}")

                with status_col:

                    show_status(
                        bool(check["flagged"])
                    )

                st.write(
                    check["message"]
                )


        with st.expander(
            "Why keep a rule-based baseline?"
        ):

            st.write(
                "Rules are predictable, transparent, and easy to audit. "
                "Their limitation is that they can miss an issue when "
                "the same idea is expressed using unfamiliar wording."
            )


    # ---------------------------------------------------------------
    # Contextual AI tab
    # ---------------------------------------------------------------

    with ai_tab:

        st.subheader(
            "Context-Aware Large Language Model (LLM)"
        )

        if llm_result:

            st.write(
                "This analysis uses **Llama 3.3 70B** through "
                "Cloudflare Workers AI. Unlike the baseline, it evaluates "
                "the meaning of the full comment rather than relying only "
                "on predefined keywords."
            )


            ai_columns = st.columns(4)

            for column, (category, title) in zip(
                ai_columns,
                CATEGORY_TITLES.items(),
            ):

                with column:

                    with st.container(border=True):

                        st.markdown(
                            f"**{title}**"
                        )

                        show_status(
                            llm_flags[category]
                        )


            st.markdown("### AI Review")

            summary_col, suggestion_col = st.columns(
                2,
                gap="large",
            )

            with summary_col:

                with st.container(border=True):

                    st.markdown(
                        "#### What the model noticed"
                    )

                    st.write(
                        llm_result["summary"]
                    )


            with suggestion_col:

                with st.container(border=True):

                    st.markdown(
                        "#### How the feedback could improve"
                    )

                    st.write(
                        llm_result["suggestion"]
                    )


            with st.expander(
                "Model details"
            ):

                st.write(
                    f"**Provider:** {llm_result['provider']}"
                )

                st.write(
                    f"**Model:** {llm_result['model']}"
                )

                st.caption(
                    "Contextual model output can vary on borderline "
                    "or ambiguous comments."
                )


        elif llm_error:

            st.warning(
                "The contextual AI analysis could not be completed."
            )

            st.caption(
                llm_error
            )


    # ---------------------------------------------------------------
    # Use boundary
    # ---------------------------------------------------------------

    st.divider()

    with st.expander(
        "What this application does — and does not do",
        expanded=False,
    ):

        st.write(
            "The Appraisal Analyst reviews the **quality of written "
            "performance feedback**."
        )

        st.write(
            "It does not determine employee ratings, promotions, "
            "compensation, discipline, hiring, or termination."
        )

        st.write(
            "Flags identify comments that may deserve closer review. "
            "They are not conclusions about an employee or manager."
        )


    # ---------------------------------------------------------------
    # Automatic smooth scroll
    # ---------------------------------------------------------------

    if st.session_state.pop(
        "scroll_to_results",
        False,
    ):

        st.html(
            """
            <script>
                setTimeout(() => {

                    const target =
                        document.getElementById(
                            "analysis-results-anchor"
                        );

                    if (target) {

                        target.scrollIntoView({
                            behavior: "smooth",
                            block: "start"
                        });

                    }

                }, 250);
            </script>
            """,
            unsafe_allow_javascript=True,
        )


# -------------------------------------------------------------------
# Footer
# -------------------------------------------------------------------

st.html(
    """
    <div class="app-footer">
        The Appraisal Analyst • Python • Streamlit •
        Rule-Based NLP • Contextual Large Language Model
    </div>
    """
)