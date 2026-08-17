\# Evaluation



\## What Was Tested



The project uses two synthetic datasets:



\* \*\*20-record development set\*\* — used to build and validate the rule-based baseline

\* \*\*12-record challenge set\*\* — used to test how both approaches handle less familiar and more context-dependent wording



The challenge set is the more useful comparison because it was not used to shape the original rules.



\## Rule-Based vs Contextual LLM



| Challenge-Set Metric      | Rule-Based | Contextual LLM |

| ------------------------- | ---------: | -------------: |

| Vagueness Accuracy        |   \*\*0.83\*\* |           0.75 |

| Missing Evidence Accuracy |       0.50 |       \*\*0.92\*\* |

| Potential Bias Accuracy   |       0.75 |       \*\*1.00\*\* |

| Rating Mismatch Accuracy  |       0.75 |       \*\*0.92\*\* |

| Overall Revision Accuracy |       0.67 |       \*\*1.00\*\* |



\## Key Findings



The rule-based approach works well when comments match words and patterns already defined in the rules. It is easy to explain and audit, but it struggles when the same idea is written in a different way.



The contextual LLM handled unfamiliar wording much better, especially for:



\* supporting evidence

\* personality-focused language

\* rating alignment



For example, the rule-based system missed phrases such as \*\*“abrasive”\*\* and \*\*“not leadership material”\*\* because those exact terms were not included in its keyword list. The LLM was able to understand the meaning of those comments.



The LLM was not perfect either. It sometimes treated borderline comments as vague even when the reference label did not, and it missed one expected rating-mismatch case.



\## Why Keep Both Approaches?



The two methods have different strengths.



\*\*Rule-based analysis\*\*



\* predictable

\* easy to audit

\* easy to explain

\* limited by predefined rules and phrases



\*\*Contextual LLM analysis\*\*



\* better at understanding meaning and unfamiliar wording

\* more flexible with different writing styles

\* can still make judgment errors



The application keeps both approaches so their results can be compared instead of treating either method as automatically correct.



\## Important Limitation



These results come from a small synthetic challenge set of 12 comments.



They are useful for comparing the two approaches, but they should not be treated as real-world or production-level accuracy claims.
