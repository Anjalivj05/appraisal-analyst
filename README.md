# The Appraisal Analyst

A Python and Streamlit application that reviews the quality of written employee performance feedback using two different approaches:

- a transparent **rule-based NLP baseline**
- a context-aware **large language model (LLM)**

The application compares both approaches side by side to show where they agree, where they differ, and what could improve the written feedback.

### Live Demo

**[Try The Appraisal Analyst](https://appraisal-analyst.streamlit.app)**

---

## Why I Built This

Performance-review comments are often subjective.

A rating such as **Outstanding** may be paired with a comment like:

> "John is a great employee with a positive attitude. Everyone likes working with him."

The comment sounds positive, but it does not explain what John actually accomplished or why the rating is justified.

The Appraisal Analyst was built to identify these kinds of quality issues before written feedback is finalized.

---

## What the App Reviews

The application checks four areas:

| Check | What it looks for |
|---|---|
| **Vagueness** | Feedback that is too general or unclear |
| **Supporting Evidence** | Whether the comment includes examples, outcomes, actions, or measurable evidence |
| **Potentially Biased Language** | Personality, likability, temperament, or similar wording that may deserve closer review |
| **Rating Alignment** | Whether the written feedback appears to support the selected performance rating |

A flag means the comment may deserve another look. It is not a conclusion about the employee or manager.

---

## How It Works

### 1. Rule-Based Analysis

The baseline uses transparent Python rules such as:

- minimum comment length
- known vague phrases
- personality-focused terms
- evidence-related words and numbers
- positive and negative performance language
- rating-alignment heuristics

This approach is predictable and easy to audit, but it can miss issues when unfamiliar wording is used.

### 2. Contextual LLM Analysis

The second approach uses **Llama 3.3 70B** through **Cloudflare Workers AI**.

Instead of relying only on predefined keywords, the model evaluates the meaning of the full comment.

It reviews the same four quality areas as the rule-based system so the results can be compared directly.

### 3. Side-by-Side Comparison

The Streamlit interface shows:

- Rule-Based Flags
- Contextual AI Flags
- Agreement between the two approaches
- Detailed rule explanations
- LLM observations
- Suggested improvements to the written feedback

---

## Evaluation

The project uses two synthetic datasets:

- **20-record development set** for building and validating the rule-based baseline
- **12-record challenge set** containing less familiar and more context-dependent wording

The challenge set was not used to shape the original rules, making it more useful for comparing how the two approaches generalize.

| Challenge-Set Metric | Rule-Based | Contextual LLM |
|---|---:|---:|
| Vagueness Accuracy | **0.83** | 0.75 |
| Missing Evidence Accuracy | 0.50 | **0.92** |
| Potential Bias Accuracy | 0.75 | **1.00** |
| Rating Mismatch Accuracy | 0.75 | **0.92** |
| Overall Revision Accuracy | 0.67 | **1.00** |

The LLM handled unfamiliar wording particularly well for supporting evidence, personality-focused language, and rating alignment.

The rule-based approach performed slightly better on vagueness in this small challenge set.

Neither approach should be treated as automatically correct.

See the full evaluation notes in [`docs/evaluation.md`](docs/evaluation.md).

---

## Tech Stack

- **Python 3.11**
- **Streamlit**
- **pandas**
- **scikit-learn**
- **pytest**
- **Cloudflare Workers AI**
- **Llama 3.3 70B**
- **Git / GitHub**

---

## Project Structure

```text
appraisal-analyst/
│
├── app.py
│
├── data/
│   ├── synthetic_appraisals.csv
│   └── holdout_appraisals.csv
│
├── docs/
│   ├── evaluation.md
│   └── governance.md
│
├── src/
│   └── appraisal_analyst/
│       ├── rules.py
│       ├── review.py
│       ├── evaluation.py
│       ├── llm.py
│       ├── llm_evaluation.py
│       ├── synthetic_data.py
│       └── holdout_data.py
│
├── tests/
│
├── course-project-docs/
│
├── pyproject.toml
├── requirements.txt
└── README.md
