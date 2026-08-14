\# Baseline Evaluation



\## Purpose



The Appraisal Analyst includes a transparent rule-based baseline for identifying common quality issues in employee performance-review comments.



The baseline currently evaluates four issue categories:



\- Vagueness

\- Missing supporting evidence

\- Personality-focused or potentially biased language

\- Rating-comment mismatch



It also produces an overall recommendation indicating whether the comment may need revision.



\## Evaluation Dataset



The initial evaluation uses a curated synthetic dataset containing 20 appraisal examples.



The examples were designed to represent different:



\- Departments

\- Job levels

\- Performance ratings

\- Comment-quality issues

\- Positive and negative performance scenarios



Each record contains manually assigned reference labels indicating whether specific review-quality concerns are expected.



No real employee or company performance-review data is used.



\## Current Baseline Results



| Evaluation Target | Accuracy | Precision | Recall | F1 Score |

|---|---:|---:|---:|---:|

| Vagueness | 1.00 | 1.00 | 1.00 | 1.00 |

| Missing Evidence | 1.00 | 1.00 | 1.00 | 1.00 |

| Potential Bias | 1.00 | 1.00 | 1.00 | 1.00 |

| Rating Mismatch | 1.00 | 1.00 | 1.00 | 1.00 |

| Overall Revision | 1.00 | 1.00 | 1.00 | 1.00 |



\## Important Interpretation



These results represent performance only on the current 20-record synthetic evaluation set.



They do not mean that the rule-based system is 100% accurate on unseen or real-world performance-review comments.



The current dataset is small and was intentionally created to test known rule behaviors. Performance may change significantly when the system encounters:



\- Different writing styles

\- Indirect or subtle feedback

\- Unfamiliar vocabulary

\- Longer and more complex comments

\- Context-dependent language

\- Evidence expressed in ways not covered by existing rules

\- More ambiguous rating-comment relationships



For this reason, the current results should be interpreted as baseline validation rather than evidence of production-level accuracy.



\## Example of Baseline Improvement



During initial evaluation, two valid negative-performance comments were incorrectly flagged as lacking supporting evidence.



For example, comments describing missed deadlines and repeated errors contained specific evidence, but the original evidence rule mainly recognized positive performance terms.



The rule was updated so that concrete negative-performance examples can also count as supporting evidence.



This reduced false positives on the current evaluation set while preserving the transparent rule-based approach.



\## Limitations of the Rule-Based Baseline



The baseline relies on predefined keywords, phrases, word counts, and simple heuristics.



This makes the system:



\- Transparent

\- Explainable

\- Easy to test

\- Easy to modify



However, it also limits the system's ability to understand meaning and context.



A comment can be vague without containing a predefined vague phrase, and a meaningful performance example may use language that is not included in the evidence-term list.



Rating alignment is particularly difficult to determine using keywords alone.



\## Planned Evaluation Expansion



Future versions of the project will extend the evaluation beyond the initial curated dataset by introducing:



\- More challenging synthetic comments

\- Edge cases and ambiguous examples

\- A separate holdout evaluation set

\- Error analysis for false positives and false negatives

\- Comparison between the rule-based baseline and optional LLM-assisted analysis



The goal is not to achieve artificially perfect metrics, but to understand where each approach performs well and where it fails.



\## Challenge-Set Evaluation



To test whether the rule-based baseline generalized beyond the examples used during initial development, the system was evaluated on a separate 12-record synthetic challenge set containing less familiar wording and more context-dependent examples.



The rules were evaluated without modifying them for these examples first.



\### Results



| Evaluation Target | Accuracy | Precision | Recall | F1 Score |

|---|---:|---:|---:|---:|

| Vagueness | 0.83 | 0.00 | 0.00 | 0.00 |

| Missing Evidence | 0.50 | 0.40 | 1.00 | 0.57 |

| Potential Bias | 0.75 | 0.00 | 0.00 | 0.00 |

| Rating Mismatch | 0.75 | 0.60 | 0.75 | 0.67 |

| Overall Revision | 0.67 | 0.60 | 1.00 | 0.75 |



The overall revision check identified all six comments that were labeled as requiring revision, resulting in recall of 1.00. However, it also flagged four acceptable comments, resulting in lower precision and overall accuracy.



\### Error Analysis



The challenge set exposed several limitations of the rule-based approach.



\*\*Vagueness\*\*



The rules missed comments that were vague in meaning but did not contain predefined vague phrases. For example, general statements about being dependable or bringing positive energy may still lack specific performance evidence.



\*\*Supporting Evidence\*\*



Several acceptable comments were incorrectly flagged because they expressed evidence using verbs that were not included in the predefined evidence dictionary, such as building workflows, coordinating transitions, handling responsibilities, or closing opportunities.



\*\*Personality-Focused Language\*\*



The keyword approach missed contextual personality judgments such as descriptions of someone being abrasive, difficult to work with, or not being leadership material.



\*\*Rating Alignment\*\*



Simple positive and negative word counts did not always capture whether the overall meaning of a comment supported its selected rating.



\### Interpretation



The difference between the initial curated-set results and the challenge-set results demonstrates an important limitation of deterministic keyword-based rules.



The baseline performs well when language follows patterns represented in its dictionaries and heuristics, but its performance decreases when the same concepts are expressed using unfamiliar wording or require contextual interpretation.



These results are therefore more useful than a perfect score alone: they establish a measurable baseline that can later be compared with a context-aware LLM-assisted approach.



The rule-based system will remain intentionally transparent rather than being repeatedly expanded to memorize every challenge-set example.

