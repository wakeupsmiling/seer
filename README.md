# Seer — Public Forecast Registry

**Structural forecasting powered by Genesis Theory.**

Seer generates falsifiable, time-bound predictions by running a protocol chain (Research → Diagnostic → Prediction) on organized systems, then locks, registers, and scores the output.

Every forecast in this registry is:
- **Pre-registered** — specification, evidence, and prediction locked with SHA-256 hashes before publication
- **Timestamped** — UTC timestamps at each lock point, verifiable via git history
- **Scored** — accuracy computed against declared resolution criteria and baseline forecasts
- **Public** — anyone can audit the hashes, review the evidence basis, and verify the scores

---

## Forecast Registry

| ID | System | Target | Horizon | Confidence | Baseline | Status | Score | Differential |
|---|---|---|---|---|---|---|---|---|
| SEER-2026-0002 | Eastman Kodak (NYSE: EK) | Trajectory from peak through digital transformation | 1997–2011 (15 yr) | 55–65% | Wall Street / McKinsey / Christensen | **Scored** (retrodiction) | 0.9775 | **+0.8475** |
| SEER-2026-0003 | Tesla Automotive (TSLA) | Trajectory: triple trap (I×R×Navigation) erosion vs. catalyst | Mar–Sep 2026 (6 mo) | 40–51% | Wall Street / EV analyst consensus | **Locked** (live) | — | — |

---

## How to read a forecast

Each forecast in the `forecasts/` directory is a JSON file containing:

- **Specification (Lock A)** — what we're forecasting, how it resolves, and what baseline we're competing against
- **Evidence Summary (Lock B)** — the evidence basis for diagnosis, with gaps and contradictions surfaced
- **Forecast (Lock C)** — the prediction, scenarios, confidence provenance, and falsification criteria
- **Monitoring** — optional notes on live forecasts (mutable, not part of any lock)
- **Resolution** — scores computed at horizon expiry (when applicable)

### Verification

To verify a lock hasn't been tampered with:

1. Extract the locked content (e.g., the `specification` field)
2. Serialize as JSON with sorted keys and no extra whitespace
3. Compute SHA-256 of the result
4. Compare against the published hash

```python
import hashlib, json
with open("forecasts/SEER-2026-0002.json") as f:
    obj = json.load(f)
content = json.dumps(obj["specification"], sort_keys=True,
                     separators=(",", ":"), ensure_ascii=False)
print(hashlib.sha256(content.encode("utf-8")).hexdigest())
# Should match obj["specification_hash"]
```

---

## Scoring methodology

See [SCORING_POLICY.md](docs/SCORING_POLICY.md) for the complete scoring rules.

Summary: every forecast is scored on component accuracy (per-criterion), Brier score (calibration), Log score (overconfidence penalty), and differential accuracy (Seer vs. declared baseline). Positive differential accuracy means Seer outperformed conventional analysis.

---

## About Genesis Theory

Genesis Theory is a candidate physics of organized transformation at human scale. It synthesizes established results from thermodynamics, information theory, and far-from-equilibrium dynamics into a formal framework for diagnosing how potential emerges, converts, stalls, or collapses across human-scale systems.

All claims carry confidence intervals. All predictions are publicly scored. Including the misses.

Learn more: [genesistheory.org](https://genesistheory.org)

---

## Project structure

```
seer-v0/
├── README.md              ← You are here (public registry)
├── forecasts/             ← One JSON file per forecast
├── schemas/               ← JSON schemas for lockable objects
│   ├── specification.schema.json
│   ├── evidence_summary.schema.json
│   ├── forecast.schema.json
│   └── forecast_object.schema.json
├── scripts/
│   ├── lock.py            ← Lock script (hash + timestamp)
│   └── score.py           ← Scoring script (Brier, Log, differential)
├── docs/
│   ├── SCORING_POLICY.md  ← Published scoring rules
│   └── OPERATOR_CHECKLIST.md
└── templates/             ← Report templates (coming soon)
```

---

*Seer is built and operated by Paul Campillo as part of the Genesis Theory research program.*
