# Seer Scoring Policy

*Published before the first forecast. Governs all scoring decisions.*

**Version:** 1.0
**Effective:** March 2026
**Status:** Active

---

## Purpose

This document defines how Seer forecasts are scored. It is published before the first live forecast so that scoring rules are committed in advance — not designed after seeing outcomes.

---

## Scoring components

Every scored forecast produces five numbers:

| Metric | What it measures | Range | Better is |
|---|---|---|---|
| **Component scores** | Per-criterion accuracy | 0.0–1.0 each | Higher |
| **Forecast score** | Weighted aggregate of component scores | 0.0–1.0 | Higher |
| **Brier score** | Calibration of the primary probability estimate | 0.0–1.0 | Lower (0 = perfect) |
| **Log score** | Calibration with heavier penalty for confident wrong predictions | 0.0–∞ | Lower |
| **Differential accuracy** | Seer score minus baseline score | −1.0 to +1.0 | Positive |

---

## Component scoring

Each resolution criterion declared at Lock A receives a score between 0.0 and 1.0:

| Score | Meaning |
|---|---|
| 1.0 | Prediction fully confirmed by outcome evidence |
| 0.75 | Substantially confirmed — direction and magnitude correct, minor deviations |
| 0.50 | Partially confirmed — direction correct, magnitude or timing off |
| 0.25 | Weakly confirmed — some elements correct but major aspects wrong |
| 0.0 | Prediction contradicted by outcome evidence |

Intermediate values (e.g., 0.6, 0.85) are permitted when the outcome falls between categories.

Component weights are fixed at Lock A and cannot be adjusted after the fact.

---

## Weighted aggregate (Forecast score)

$$\text{Forecast score} = \sum_{i} w_i \times s_i$$

where $w_i$ is the component weight (declared at Lock A, summing to 1.0) and $s_i$ is the component score.

---

## Brier score

$$\text{Brier} = (p - o)^2$$

where $p$ is the probability assigned to the primary scenario at Lock C and $o$ is the outcome indicator (Forecast score serves as the continuous outcome measure).

Interpretation: 0.0 = perfect calibration, 0.25 = equivalent to coin flip, 1.0 = maximally wrong.

---

## Log score

$$\text{Log score} = -\ln(p_{\text{actual}})$$

where $p_{\text{actual}}$ is the probability assigned to the event that actually occurred. If the primary prediction was confirmed, this is the primary scenario probability. If it was refuted, this is 1 minus that probability.

The Log score punishes confident wrong predictions more severely than Brier. A forecast that assigns 90% to an outcome that doesn't occur receives a Log score of −ln(0.1) ≈ 2.30, while Brier gives 0.81. This asymmetry is intentional — overconfidence should carry a proportionally higher cost.

---

## Differential accuracy

$$\text{Differential} = \text{Seer score} - \text{Baseline score}$$

The baseline is declared at Lock A. At resolution, the baseline's prediction is scored using the same component criteria and weights.

This is the metric that earns Genesis its place. If differential accuracy is consistently zero or negative, Seer adds complexity without value — regardless of how internally coherent the analysis is.

---

## Who scores

In v0, the operator (Paul Campillo) scores all forecasts. This creates a conflict of interest that is managed through:

1. **Published scoring policy** (this document) — rules committed before outcomes are known
2. **Locked resolution criteria** — what counts as right/wrong is defined at Lock A, not at scoring time
3. **Published outcome evidence** — the evidence used for scoring is part of the public record
4. **Baseline comparison** — differential accuracy is computed against an external forecast that the scorer does not control
5. **Future adjudication** — v1 introduces independent adjudication for contested scores

The conflict is real. The mitigations are structural, not promissory. Anyone can audit a score by comparing the locked criteria against the published outcome evidence.

---

## Ambiguity

When outcome evidence doesn't clearly resolve a criterion:

1. Score at 0.50 (partial) and note the ambiguity in calibration notes
2. If the ambiguity affects the primary forecast statement, flag the forecast as "partially informative" rather than "fully resolved"
3. Do not discard ambiguous forecasts — they carry calibration information

---

## Mootness

A forecast is marked **moot** when an exogenous event outside the structural analysis invalidates the prediction. Examples: target company acquired, regulatory framework abolished, natural disaster destroys the system.

Moot forecasts are labeled in the registry but excluded from calibration statistics. The mootness declaration must specify the event and explain why it falls outside the structural analysis.

Mootness is not a refuge for wrong predictions. If the "exogenous" event was forecastable through structural analysis (e.g., a regulatory action driven by the system's own R-channel dynamics), the forecast is scored, not mooted.

---

## Retrodiction scoring

Retrodictions follow the same scoring rules with one addition: the temporal cutoff must be declared and enforced. Research is restricted to evidence available on or before the declared prediction date.

Retrodiction scores are labeled as such in the registry and analyzed separately from live prediction scores. They validate the protocol's diagnostic power but carry less weight than live predictions because hindsight contamination, while mitigated by temporal cutoff, cannot be fully eliminated.

---

## Calibration reporting

After 5 or more scored forecasts, calibration snapshots are published:

- **Calibration curve**: predicted probabilities vs. actual frequencies
- **Mean Brier score**: overall calibration quality
- **Mean differential accuracy**: overall value-add vs. baselines
- **Domain breakdown**: scores by object type and target class
- **Publication class breakdown**: research-grade vs. standard vs. exploratory

Calibration snapshots are themselves Substack content and grant evidence.

---

## Amendment policy

This scoring policy can be amended, but:

1. Amendments apply only to forecasts locked **after** the amendment date
2. All prior forecasts are scored under the policy in effect at their Lock A time
3. Amendments are published with rationale and effective date
4. The amendment history is preserved in this document's version log

---

*This document governs all Seer scoring decisions. When in doubt, this document decides.*
