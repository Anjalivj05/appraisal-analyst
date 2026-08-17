\# Responsible Use and Governance



The Appraisal Analyst reviews the quality of written employee performance-feedback comments.



It is designed to help identify comments that may be vague, unsupported by evidence, focused too heavily on personality, or inconsistent with the selected performance rating.



It is not designed to make employment decisions.



\---



\## What the Application Does



The application reviews four areas:



\- Vagueness

\- Missing supporting evidence

\- Potentially biased or personality-focused language

\- Rating mismatch



Two different approaches are used:



1\. A transparent rule-based baseline

2\. A context-aware large language model (LLM)



The results are shown side by side so the differences between the two approaches are visible.



\---



\## What It Does Not Do



The application does not decide:



\- Employee ratings

\- Promotions

\- Compensation

\- Hiring

\- Termination

\- Discipline



A flag simply means that a comment may deserve closer review.



It does not mean that the employee, manager, or comment has been judged as biased, unfair, or incorrect.



\---



\## Data and Privacy



This portfolio project uses synthetic data for development and evaluation.



Real employee performance reviews can contain sensitive personal or workplace information. A production version would require stronger privacy controls before real HR data could be used.



Examples include:



\- Limiting access to authorized users

\- Removing unnecessary personal information

\- Encrypting stored and transmitted data

\- Defining retention and deletion rules

\- Reviewing the data-use terms of any external model provider



For the public demo, users are asked to enter only synthetic or non-sensitive text.



\---



\## Rule-Based Analysis



The rule-based system uses predefined phrases, evidence terms, word-count checks, and rating-alignment rules.



Its main strength is transparency. It is easy to see why a rule was triggered.



Its limitation is that it cannot fully understand language or context.



For example, a rule may detect the word `attitude`, but miss another phrase that communicates a similar personality-based judgment.



\---



\## Contextual LLM Analysis



The application also uses Llama 3.3 70B through Cloudflare Workers AI.



The large language model reviews the full meaning of the comment instead of relying only on predefined keywords.



This helps with unfamiliar wording and more context-dependent comments.



However, the model is not automatically correct.



It may:



\- Interpret an ambiguous comment differently from a reviewer

\- Flag something that does not need revision

\- Miss an issue that should have been flagged

\- Produce different judgments on borderline wording



For that reason, the application presents the LLM result as another source of analysis rather than as a final answer.



If the external model is unavailable, the rule-based analysis can still operate independently.



\---



\## Bias and Fairness



Performance-review language can be subjective.



Words about personality, likability, temperament, or culture fit may sometimes be relevant to workplace behavior, but they can also introduce unfair or unsupported judgments.



The application therefore highlights this type of wording for closer review.



A flag does not prove that bias exists.



The purpose is to make potentially problematic wording easier to notice.



\---



\## Evaluation



Both approaches are tested using synthetic appraisal comments with expected labels.



The project includes:



\- A 20-record development dataset

\- A separate 12-record challenge dataset



The challenge dataset is used to see how well each approach handles less familiar wording.



The results show that the rule-based system and contextual LLM have different strengths.



Full evaluation results are available in \[`evaluation.md`](evaluation.md).



Because the datasets are small and synthetic, the reported results should not be treated as production-level accuracy.



\---



\## Errors and Review



Both false positives and false negatives matter.



A false positive could send an acceptable comment for unnecessary revision.



A false negative could allow a weak or potentially problematic comment to pass without being noticed.



The application therefore shows the reasons behind the analysis instead of hiding them behind a single score.



The final interpretation should remain with the person reviewing the feedback.



\---



\## Project Scope



The Appraisal Analyst is a portfolio prototype showing how rule-based NLP and a contextual LLM can be compared within the same application.



The goal is not to automate HR decisions.



The goal is to demonstrate a practical way to improve the quality and consistency of written performance feedback while keeping the limitations of both approaches visible.

