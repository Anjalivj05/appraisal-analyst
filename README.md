\# The Appraisal Analyst



The Appraisal Analyst is a human-in-the-loop decision-support application designed to improve the quality, consistency, and fairness of written employee performance reviews.



Performance-appraisal comments can influence important outcomes such as promotions, compensation, and employee development. However, review quality often varies between managers. Some comments include specific achievements and measurable evidence, while others are vague, unsupported, inconsistent with the selected rating, or focused on personality rather than job performance.



HR teams must often identify these issues manually before appraisals are finalized. The Appraisal Analyst is being developed to make that review process more structured, explainable, and efficient.



\## Business Problem



Managers do not always write performance feedback using the same level of detail or objectivity.



Examples of common review-quality problems include:



\- Vague statements such as “good performer” or “needs improvement”

\- Ratings that are not adequately supported by the written comment

\- Feedback that lacks examples, outcomes, or measurable evidence

\- Personality-focused language that may be unrelated to job performance

\- Inconsistent review standards across managers or departments



Weak appraisal documentation can make it difficult for HR to evaluate whether employees are receiving clear, fair, and evidence-based feedback.



\## Proposed Solution



The application reviews a draft appraisal comment together with its selected performance rating.



It evaluates the comment for:



\- Vagueness and generic wording

\- Missing supporting evidence

\- Possible rating-comment mismatch

\- Personality-focused or potentially biased language

\- Missing actionable development guidance



The application then produces a structured review explaining which concerns were identified and what additional information may be needed.



\## How the Project Works



The project combines multiple approaches:



1\. \*\*Rule-based checks\*\* identify clear issues such as very short comments, unsupported wording, and selected personality-related terms.

2\. \*\*Optional LLM analysis\*\* evaluates contextual issues that simple keyword rules may miss.

3\. \*\*A Streamlit interface\*\* allows users to enter appraisal information and review the results.

4\. \*\*Synthetic data\*\* supports development and testing without exposing real employee information.

5\. \*\*Evaluation metrics\*\* compare system outputs with reference labels and measure false positives, false negatives, precision, recall, and agreement.

6\. \*\*Governance documentation\*\* defines privacy, fairness, human-review, and responsible-use controls.



\## Why Both Rules and an LLM?



Rule-based checks are transparent and useful for detecting obvious problems. However, they may miss comments that are long enough but still lack meaningful information.



For example:



> “Consistently meets expectations across all areas.”



This comment may pass a basic word-count check, but it does not explain what the employee accomplished or provide evidence supporting the assessment.



An optional LLM layer can evaluate the meaning and context of a comment, while the rule-based system remains available as an explainable baseline.



\## Important Boundary



The Appraisal Analyst does not determine:



\- Employee performance ratings

\- Promotions

\- Compensation

\- Discipline

\- Hiring

\- Termination



The application only supports appraisal-comment quality review. HR professionals and managers remain responsible for all final decisions and wording.



\## Technology Stack



\- Python 3.11

\- Streamlit

\- pandas

\- scikit-learn

\- pytest

\- python-dotenv

\- Optional OpenAI API integration



\## Repository Structure



```text

appraisal-analyst/

├── course-project-docs/   # Original academic capstone materials

├── data/                  # Synthetic datasets

├── docs/                  # Governance and project documentation

├── screenshots/           # Application screenshots

├── src/                   # Application source code

├── tests/                 # Automated tests

├── requirements.txt       # Python dependencies

└── README.md

