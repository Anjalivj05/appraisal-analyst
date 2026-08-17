# The Appraisal Analyst

**An HR analytics application that helps review employee performance-feedback comments before they are finalized.**

The Appraisal Analyst checks whether a manager's written feedback is vague, lacks supporting evidence, focuses too much on personality, or does not support the selected performance rating.

### [Try the Live Application](https://appraisal-analyst.streamlit.app)

---

## Why I Built This

Performance-review comments can influence how an employee's work is understood and may later affect development, promotion, compensation, or other career decisions.

A manager might select **Outstanding** but write:

> "John is a great employee with a positive attitude. Everyone likes working with him."

The comment sounds positive, but it does not explain what John accomplished or why the rating is justified.

The idea behind this project is simple:

**Manager writes feedback → Appraisal Analyst reviews it → HR checks the flags → unclear comments can be returned to the manager for revision before the appraisal is finalized.**

The application does not make employment decisions. It helps HR identify feedback that may need a closer look, supporting a more consistent and better-documented appraisal process.

---

## What the App Checks

| Check | Purpose |
|---|---|
| **Vagueness** | Finds feedback that is too general or unclear |
| **Supporting Evidence** | Looks for examples, actions, outcomes, or measurable evidence |
| **Potentially Biased Language** | Flags personality, likability, temperament, or similar wording for review |
| **Rating Alignment** | Checks whether the comment appears to support the selected rating |

---

## How It Works

The same comment is analyzed in two different ways.

### Rule-Based NLP
A transparent Python rule engine checks predefined phrases, evidence terms, word count, numbers, performance language, and rating alignment.

**Strength:** predictable and easy to explain.  
**Limitation:** can miss issues written in unfamiliar ways.

### Context-Aware LLM
The application also uses **Llama 3.3 70B through Cloudflare Workers AI**.

Instead of relying only on keywords, the large language model (LLM) evaluates the meaning and context of the full comment.

The interface shows both results side by side so users can see where the approaches agree or disagree.

---

## Try It Yourself

Open the **[live app](https://appraisal-analyst.streamlit.app)** and:

1. Select a performance rating, such as `Outstanding`.
2. Enter:
   > John is a great employee with a positive attitude. Everyone likes working with him.
3. Click **Analyze Comment**.
4. Review the **Compare**, **Rule-Based**, and **Contextual AI** tabs.

Then try a stronger comment:

> John exceeded his quarterly target by 18%, reduced reporting delays, and mentored two new team members who completed onboarding ahead of schedule.

The difference between the results helps demonstrate what the application is looking for.

---

## Evaluation

The project uses only synthetic appraisal data.

- **20-record development set** for building and validating the rule-based baseline
- **12-record challenge set** for testing both approaches on less familiar wording

| Challenge-Set Accuracy | Rule-Based | Contextual LLM |
|---|---:|---:|
| Vagueness | **0.83** | 0.75 |
| Missing Evidence | 0.50 | **0.92** |
| Potential Bias | 0.75 | **1.00** |
| Rating Mismatch | 0.75 | **0.92** |
| Overall Revision | 0.67 | **1.00** |

These results are based on a small synthetic dataset and are meant for comparison, not as production-level accuracy claims.

More details: [`docs/evaluation.md`](docs/evaluation.md)

---

## How the Project Evolved

The Appraisal Analyst started as a **graduate group capstone project**.

The original prototype was built as a Custom GPT that reviewed appraisal comments for vague feedback, missing evidence, rating mismatch, and potentially problematic language.

**[View the original Custom GPT prototype](https://chatgpt.com/g/g-6a59640718688191b7a45764d3e3cc18-the-appraisal-analyst-hr-review-quality-assistant)**

I later expanded the idea independently into a complete portfolio application by adding:

- Python-based rule engine
- contextual LLM integration
- synthetic development and challenge datasets
- evaluation metrics
- automated tests
- side-by-side model comparison
- custom Streamlit interface
- public cloud deployment
- responsible-use documentation

The original capstone materials are preserved in [`course-project-docs`](course-project-docs/).

---

## Tech Stack

**Python 3.11 · Streamlit · pandas · scikit-learn · pytest · Cloudflare Workers AI · Llama 3.3 70B · Git/GitHub**

---

## Project Structure

```text
app.py                         Streamlit application

src/appraisal_analyst/
├── rules.py                   Rule-based checks
├── review.py                  Review logic
├── llm.py                     Llama / Cloudflare integration
├── evaluation.py              Rule evaluation
└── llm_evaluation.py          LLM evaluation

data/                          Synthetic datasets
tests/                         Automated tests
docs/                          Evaluation and governance notes
course-project-docs/           Original graduate capstone materials
```

---

## Responsible Use

The Appraisal Analyst reviews the **quality of written feedback**. It does not decide employee ratings, promotions, compensation, hiring, discipline, or termination.

Flags are signals for closer review, not final judgments.

The public application should only be tested with synthetic or non-sensitive text.

More details: [`docs/governance.md`](docs/governance.md)

---

**Live Demo:** [appraisal-analyst.streamlit.app](https://appraisal-analyst.streamlit.app)
