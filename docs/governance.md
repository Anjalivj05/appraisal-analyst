\# Responsible AI and Governance



\## Purpose



The Appraisal Analyst is designed to support the review of written employee performance-appraisal comments before they are finalized.



The application analyzes comment quality and identifies potential concerns such as:



\- Vague or generic feedback

\- Missing supporting evidence

\- Possible rating-comment mismatch

\- Personality-focused or potentially biased language



The application is a review-support tool and is not intended to make employment decisions.



\## Scope Boundary



The Appraisal Analyst must not independently determine or recommend:



\- Promotions

\- Compensation

\- Hiring

\- Termination

\- Discipline

\- Employee performance ratings



Its purpose is limited to evaluating the quality of written appraisal documentation.



\## Data Privacy



Performance-review information may contain sensitive employee information.



The public portfolio version therefore uses only synthetic data.



If the application were evaluated in an organizational environment, appropriate controls would include:



\- De-identification where possible

\- Role-based access

\- Secure storage

\- Defined retention periods

\- Access and activity logging

\- Approved data-processing environments

\- Review of vendor data-use and model-training terms



Real employee appraisal data should not be placed in the public repository.



\## Bias and Fairness



Performance-review language can contain subjective or personality-focused wording.



The application therefore includes checks intended to identify potentially problematic language, but these checks have important limitations.



A keyword or language model flag does not prove that a comment is biased.



Likewise, the absence of a flag does not prove that a comment is fair.



Outputs should be treated as signals for further review rather than conclusions about an employee or manager.



\## False Positives and False Negatives



Two important error types are monitored.



\### False Positive



A comment is flagged even though it is acceptable.



This may create unnecessary review work or incorrectly suggest that valid feedback contains a problem.



\### False Negative



A problematic comment passes without being flagged.



This may allow vague, unsupported, inconsistent, or inappropriate feedback to remain unnoticed.



The evaluation pipeline therefore measures both types of errors rather than relying only on overall accuracy.



\## Evaluation Controls



The project uses:



\- Curated synthetic development examples

\- A separate synthetic challenge set

\- Accuracy, precision, recall, and F1 score

\- Confusion-matrix counts

\- Error analysis

\- Automated regression tests



The challenge-set results demonstrate that the transparent rule-based baseline does not generalize perfectly to unfamiliar wording.



This limitation is documented rather than hidden.



\## Rule-Based Baseline Limitations



The baseline relies on:



\- Keyword dictionaries

\- Phrase matching

\- Word-count thresholds

\- Simple rating-alignment heuristics



These rules are explainable and easy to audit, but they do not fully understand language or context.



They may miss:



\- Indirect personality judgments

\- Unfamiliar descriptions of supporting evidence

\- Context-dependent vagueness

\- Complex relationships between written feedback and ratings



The rule dictionaries should not be continuously expanded simply to memorize evaluation examples.



\## Optional LLM Layer



A later project stage may use an LLM to analyze contextual issues that deterministic rules cannot easily capture.



The LLM will remain optional so that:



\- The rule-based baseline can be evaluated independently

\- Users can compare deterministic and contextual analysis

\- The system still works without an external model

\- LLM output can be evaluated against the same reference data



LLM-generated analysis should also be treated as advisory rather than authoritative.



\## Human Review



A qualified reviewer should evaluate flagged concerns before any action is taken.



The application should explain why a concern was identified and provide enough information for the reviewer to agree, disagree, or investigate further.



Human review is therefore a governance control, not the primary feature or identity of the project.



\## Logging and Auditability



A production implementation should maintain an audit trail containing information such as:



\- Review timestamp

\- Appraisal identifier

\- Analysis method used

\- Checks triggered

\- Model or rule version

\- Reviewer decision

\- Override information



Sensitive appraisal text should only be retained when permitted by organizational privacy and retention policies.



\## Deployment Considerations



Before use with real employee data, an organization would need to validate:



\- Accuracy on organization-specific review language

\- Fairness across relevant employee groups

\- Privacy and security controls

\- Data residency requirements

\- Model-provider contractual terms

\- Access permissions

\- Retention policies

\- Monitoring and incident-response procedures



Performance on this portfolio project's synthetic datasets should not be interpreted as evidence that the system is ready for production deployment.



\## Current Project Position



The Appraisal Analyst is a portfolio prototype demonstrating:



1\. Transparent rule-based text analysis

2\. Structured application design

3\. Synthetic-data generation

4\. Automated testing

5\. Quantitative evaluation

6\. Holdout error analysis

7\. Responsible-AI controls

8\. Optional contextual LLM analysis



The goal is to demonstrate how an AI-assisted analytics application can be evaluated and governed, not simply how an LLM can be connected to a user interface.

