# The Appraisal Analyst

The Appraisal Analyst is a Python and Streamlit application that reviews employee performance-appraisal comments for common quality issues.

It checks whether feedback is vague, lacks supporting evidence, does not align with the selected rating, or focuses too much on personality instead of job performance.

### Live Demo

**Try the application:** [appraisal-analyst.streamlit.app](https://appraisal-analyst.streamlit.app)

The project compares two different approaches:

* a transparent **rule-based baseline**
* a **contextual LLM analysis** using Llama 3.3 70B through Cloudflare Workers AI

The goal is not to let AI make HR decisions. The goal is to see whether written feedback is clear, specific, and well supported before an appraisal is finalized.

---

## Why I Built This

Performance reviews can influence promotions, compensation, development plans, and other important career decisions.

But the quality of the written feedback can vary a lot between managers.

A comment such as:

> “John is a great employee with a positive attitude. Everyone likes working with him.”

sounds positive, but it does not explain what John actually achieved or why the comment supports an **Outstanding** rating.

Reviewing hundreds of comments manually can also take a lot of HR time.

The Appraisal Analyst explores how simple rules and contextual AI can help identify comments that may need a closer look.

---

## What the App Checks

Each appraisal comment is reviewed for four areas:

### Vagueness

Is the feedback too general or unclear?

### Missing Evidence

Does the comment include actual examples, results, achievements, errors, deadlines, or measurable outcomes?

### Potential Bias

Does the wording focus on personality, likability, temperament, or similar traits instead of observable work performance?

### Rating Alignment

Does the written feedback provide enough support for the selected performance rating?

---

## How It Works

A user enters:

* a performance rating
* an appraisal comment

The application runs the same input through two approaches.

### 1. Rule-Based Analysis

The baseline uses Python rules such as:

* word-count checks
* predefined vague phrases
* personality-related terms
* evidence keywords
* simple rating-alignment logic

This approach is easy to understand and audit, but it has trouble when the same idea is written in an unfamiliar way.

### 2. Contextual LLM Analysis

The second approach sends the comment to **Llama 3.3 70B**, hosted through Cloudflare Workers AI.

Instead of looking only for predefined words, the model evaluates the meaning of the full comment.

The Streamlit interface then shows both results side by side so their differences are easy to see.

---

## Evaluation

The project uses synthetic appraisal comments so no real employee data is required.

Two datasets are included:

* **20-record development set** for building and validating the rule-based baseline
* **12-record challenge set** with harder and less familiar wording

On the challenge set:

| Check            | Rule-Based Accuracy | Contextual LLM Accuracy |
| ---------------- | ------------------: | ----------------------: |
| Vagueness        |            **0.83** |                    0.75 |
| Missing Evidence |                0.50 |                **0.92** |
| Potential Bias   |                0.75 |                **1.00** |
| Rating Mismatch  |                0.75 |                **0.92** |
| Overall Revision |                0.67 |                **1.00** |

The results show why both approaches are useful.

The rule-based system is predictable and explainable, while the LLM handles unfamiliar and contextual language much better in several categories.

The LLM is not treated as automatically correct. It also disagreed with some reference labels, especially on borderline cases.

See [`docs/evaluation.md`](docs/evaluation.md) for the evaluation details.

---

## Tech Stack

* Python 3.11
* Streamlit
* pandas
* scikit-learn
* pytest
* Cloudflare Workers AI
* Llama 3.3 70B

---

## Project Structure

```text
appraisal-analyst/
├── data/                  # Synthetic development and challenge datasets
├── docs/                  # Evaluation and governance documentation
├── src/
│   └── appraisal_analyst/
│       ├── rules.py       # Rule-based checks
│       ├── review.py      # Review workflow
│       ├── llm.py         # Contextual LLM analysis
│       ├── evaluation.py  # Rule-based evaluation
│       └── llm_evaluation.py
├── tests/                 # Automated tests
├── course-project-docs/   # Original graduate capstone materials
├── app.py                 # Streamlit application
├── requirements.txt
└── README.md
```

---

## Run Locally

Clone the repository and install the dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file using `.env.example` and add your Cloudflare Workers AI credentials.

Then run:

```bash
streamlit run app.py
```

---

## Responsible Use

This project reviews the **quality of written appraisal comments**.

It does not decide:

* employee ratings
* promotions
* compensation
* discipline
* hiring
* termination

Flags are review signals, not conclusions about an employee or manager.

The public project uses synthetic data only.

See [`docs/governance.md`](docs/governance.md) for more details.

---

## Project Background

The Appraisal Analyst began as a graduate capstone project focused on improving the quality of written employee performance reviews.

I later rebuilt and expanded the idea as an individual portfolio project using Python, Streamlit, a rule-based baseline, contextual LLM analysis, synthetic-data evaluation, automated testing, and responsible-AI documentation.
