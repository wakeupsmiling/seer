# Seer v0 — Operator Checklist

*Step-by-step procedure for running a forecast through the full chain.*

---

## Before you start

- [ ] Confirm you have a target system in mind
- [ ] Confirm it passes the admissibility gate (bounded, organized, consequential change, observable signals)

---

## Phase 1: Specification (Lock A)

1. Open a Seer conversation (Claude with Genesis protocol skills)
2. Name the system: "Run a prediction on [system]"
3. Work through the specification:
   - System identification and scope agreement
   - Object type classification
   - Forecast target class (trajectory / sustainability / breakpoint / transition / comparison / conditional)
   - Specific target statement
   - Horizon (start date, end date)
   - Resolution criteria with component weights (must sum to 1.0)
   - Strongest-available baseline (source, position, divergence, hinge)
   - Shock sensitivity assessment
   - Forecast class (standard / speculative)
   - Evidence sufficiency estimate
   - Publication class (research-grade / standard / exploratory)
4. Export specification as JSON
5. Save as a file (e.g., `tesla_spec.json`)
6. Run the lock script:
   ```
   python3 scripts/lock.py spec tesla_spec.json
   ```
7. Note the forecast ID (e.g., SEER-2026-0001)
8. Confirm: **"Lock A confirmed"**

---

## Phase 2: Research + Evidence (Lock B)

1. In the same conversation, run the research protocol
2. Present evidence brief to yourself — review for:
   - Coverage across all four SIRF channels
   - Source diversity and quality
   - Critical gaps acknowledged
   - Contradictions surfaced
3. Export evidence summary as JSON
4. Save as a file (e.g., `tesla_evidence.json`)
5. Run the lock script:
   ```
   python3 scripts/lock.py evidence tesla_evidence.json --forecast-id SEER-2026-0001
   ```
6. Confirm go/no-go decision
7. Confirm: **"Lock B confirmed"**

---

## Phase 3: Diagnostic + Prediction (Lock C)

1. Run the diagnostic protocol on locked evidence
2. Review diagnostic findings — challenge yourself:
   - Is the bottleneck channel identification clear?
   - Is the regime classification supported by evidence?
   - Is the margin assessment grounded or speculative?
   - What would change the diagnosis?
3. Run the prediction protocol from the locked diagnostic
4. Review the forecast:
   - Is the statement specific enough to score?
   - Do the scenarios span the plausible space?
   - Do probabilities sum to 1.0?
   - Are falsification criteria genuinely falsifiable?
   - Does the baseline contrast identify a real hinge?
5. Export forecast as JSON
6. Save as a file (e.g., `tesla_forecast.json`)
7. Run the lock script:
   ```
   python3 scripts/lock.py forecast tesla_forecast.json --forecast-id SEER-2026-0001
   ```
8. Confirm: **"Lock C confirmed — forecast is locked"**

---

## Phase 4: Publish

1. Review the complete forecast object at `forecasts/SEER-2026-0001.json`
2. Commit and push to the registry:
   ```
   git add forecasts/SEER-2026-0001.json
   git commit -m "Lock SEER-2026-0001: [system] [target class]"
   git push
   ```
3. The forecast is now public, timestamped, and verifiable
4. Write the Substack post if this is a public-facing prediction

---

## Monitoring (optional, lightweight)

- Periodically review live forecasts (weekly for short-horizon, monthly for long)
- If something relevant happened, add a monitoring note:
  1. Open the forecast JSON
  2. Add an entry to `monitoring.notes` with timestamp and observation
  3. Update `monitoring.landing_confidence` if warranted
  4. Commit and push the updated file
- Do NOT modify any locked content (specification, evidence, forecast)

---

## Scoring (at resolution)

1. Horizon expires or early settlement conditions are met
2. Gather outcome evidence (document sources)
3. Gather baseline outcome (what did the consensus predict, and what happened?)
4. Create outcome file (e.g., `tesla_outcome.json`):
   ```json
   {
     "outcome_evidence": ["Evidence item 1", "Evidence item 2"],
     "component_outcomes": [
       {
         "criterion": "criterion text from spec",
         "outcome": "what actually happened",
         "score": 0.75
       }
     ],
     "baseline_outcome": "What the baseline predicted and how it fared",
     "baseline_score": 0.60,
     "calibration_notes": "What this scoring reveals"
   }
   ```
5. Run the scoring script:
   ```
   python3 scripts/score.py SEER-2026-0001 tesla_outcome.json
   ```
6. Review scores
7. Commit and push:
   ```
   git add forecasts/SEER-2026-0001.json
   git commit -m "Score SEER-2026-0001: [brief result]"
   git push
   ```

---

## For retrodiction runs

Same as above, with these additions:

- At Phase 2, declare the temporal cutoff (prediction date)
- Confirm research is restricted to evidence available at or before that date
- After Lock C, lift the cutoff and run the scoring phase against actual outcomes
- Record the retrodiction scorecard in the forecast object

---

## The sentence to remember

**Lock → Publish → Wait → Score. Honestly.**
