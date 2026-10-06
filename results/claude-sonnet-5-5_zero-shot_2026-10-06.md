# Claude Sonnet 5.5 — Zero-shot evaluation

**Date:** 2026-10-06  
**Model:** `claude-sonnet-5-5`  
**Prompt:** `prompts/zero_shot.txt`  
**Cases:** 10  
**Runs per case:** 3  
**Total classifications:** 30

## Summary

| Metric | Result |
|---|---:|
| Accuracy | 1.0 (100 %) |
| Underestimation rate | 0.0 (0 %) |
| Consistency | 1.0 (100 %) |
| Invalid responses | 0 |

## Accuracy by difficulty

| Difficulty | Accuracy |
|---|---:|
| leicht | 1.0 |
| mittel | 1.0 |
| schwer | 1.0 |

## Confusion matrix

The first run for each case produced the following classifications:

| Expected class | minimal | limited | high | prohibited | invalid |
|---|---:|---:|---:|---:|---:|
| minimal | 3 | 0 | 0 | 0 | 0 |
| limited | 0 | 2 | 0 | 0 | 0 |
| high | 0 | 0 | 3 | 0 | 0 |
| prohibited | 0 | 0 | 0 | 2 | 0 |

## Interpretation

Claude Sonnet 5.5 classified all ten benchmark cases correctly in all three repeated runs. No underestimation and no invalid JSON outputs occurred in this run.

This result should be treated as an initial technical benchmark only. The sample is small, the cases are synthetic and relatively concise, and the expected labels reflect a reasoned interpretation of the EU AI Act rather than binding legal advice. A broader evaluation should include more cases, additional prompt variants, edge cases, and expert review of the reference labels.
