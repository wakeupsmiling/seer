# SEER-2026-0003-ADDENDUM-P7 — registration record

| Field | Value |
|---|---|
| Addendum ID | SEER-2026-0003-ADDENDUM-P7 |
| Parent forecast | SEER-2026-0003 (locked 2026-03-23) |
| Registered at | 2026-08-30T20:43:45.099150+00:00 |
| Drafted | no earlier than 2026-04-22 |
| Evidence for drafting date | **none** |
| Pre-registration claim | **not asserted** |
| Q3 decision rule hash | `7da7f101a9a31670329fc83506a2e33f648cae5c77431eb34ed7fccf23b74ca9` |
| Q3 rule locked at | 2026-08-30T20:43:45.099150+00:00 |

**What is locked here and what is not.** Only the Q3 decision rule carries a hash and a lock, because only
it precedes its data. Tesla reported Q2 2026 in July, before this registration, so everything in the April
text below concerning Q1 and Q2 — including the counterfactual and the first row of the interpretation
table — is registered **post-hoc** and earns no pre-registration credit.

The April text is reproduced verbatim and unedited. Its `Lock date` and `Hash` fields were never filled in;
they are left exactly as written. Corrections and unresolved conflicts follow the text, not inside it.

---

## BEGIN APRIL 2026 TEXT — VERBATIM, UNEDITED

# ADDENDUM — P7 falsifier trigger and mechanism interpretation
## Tesla Automotive · SEER-2026-0003

**Paul Campillo · Genesis Research Lab**
**Version 1.0 · April 2026 · Pre-Q2 commitment**

---

## Status

Tesla reported Q1 2026 automotive gross margin excluding regulatory credits at **19.2%**, above P7's 18.0% resolution threshold. Per the locked criterion — *"Resolves FALSE if automotive gross margin excluding regulatory credits reaches or exceeds 18.0% in any quarter through Q3 2026"* — P7 triggered its falsifier on its first checkpoint.

**Final P7 score: FALSE. Brier contribution: 0.5625.**

This result stands regardless of Q2 or Q3 outcomes. The locked spec binds.

---

## Why this addendum exists

P7's stated falsifier mapping reads: *"R→F cascade propagation thesis is wrong."* That mapping treats the binary resolution as a binary verdict on the underlying mechanism claim. The resolution is settled. The mechanism question remains open across the full 3-quarter window.

This addendum pre-commits interpretation criteria for what Q2 and Q3 trajectories mean for the mechanism — **before those data arrive**. Without this commitment, any post-hoc reinterpretation after Q2 lands would constitute the hindsight contamination that the WeWork scrub protocol exists to prevent.

---

## Two questions, answered separately

1. **Did P7 resolve TRUE or FALSE?** Answered by locked criteria. FALSE.
2. **Does the R→F cascade mechanism survive?** Answered by pre-committed interpretation across Q1, Q2, and Q3 together.

Blending these is motivated reasoning. Keeping them separate is rigor.

---

## Pre-committed interpretation criteria

Evaluated once Q2 and Q3 2026 automotive gross margin ex-credits both report:

| Q2 margin | Q3 margin | Mechanism verdict |
|---|---|---|
| Below 18% | Below 18% | Q1 reads as an accounting spike. Mechanism claim survives with a known spec weakness: P7 should have stripped Tesla-disclosed one-time items alongside regulatory credits. Tesla v3 incorporates this correction. |
| At or above 18% | At or above 18% | Q1 was not an aberration. Margin recovered structurally. R→F cascade propagation claim is substantially wrong and requires revision or replacement. |
| Mixed (one ≥ 18%, one < 18%) | | Tiebreaker: equal-weighted average of Q1, Q2, Q3 ex-credits margin. Average ≥ 18%: mechanism claim wrong. Average < 18%: mechanism survives with known exceptions. |

The weighted average uses equal Q1/Q2/Q3 weights. No quarter gets excluded for one-time items. The spec error sits in writing them out in advance; the remedy does not run backward.

"Mechanism survives" means: this specific falsifier did not fire conceptually. It does not mean the theory is right. It means this test did not disprove it.

---

## The symmetry test

This interpretation reads as epistemically clean only under the following standard: had Tesla reported Q1 at 17.5% rather than 19.2%, I would not now be writing *"but that margin was propped up by favorable FX"* or similar downward-adjusting caveat.

I commit to this standard. If Q2 lands at 17.5% inflated by disclosed one-time items, I will not apply a reverse adjustment to argue P7 should have failed after all. Once the spec locks, it binds in both directions.

---

## What the triggered falsifier costs, regardless of mechanism outcome

Three items enter the record as permanent lessons from this case:

**Resolution criteria must strip all material one-time items when companies disclose them separately.** Q1 2026 demonstrates that "excluding regulatory credits" proves insufficient. Tesla reported warranty reserve releases and tariff refund windfalls as "one-time benefits" in its own shareholder deck. Tesla v3 criteria will strip regulatory credits *and* separately disclosed one-time items. This correction applies forward. P7 scores FALSE as written.

**P7 carried 75% confidence, not 95%.** A well-calibrated 75% prediction fails in roughly one of four cases. One miss at this confidence level does not by itself signal framework failure; it signals that confidence levels got set honestly. A framework that never misses at any stated confidence is not calibrated — it is overconfident. The aggregate Brier score will reflect this calibration rather than hide it.

**The "one-time benefits" observation is real but cannot rescue P7.** Electrek's analysis of the 10-Q and Tesla's own shareholder deck both disclose the warranty-reserve and tariff-refund contributions to the 19.2% print. Noted for spec improvement. Out of scope for resolution.

---

## Counterfactual: what a spec-improved P7 would have shown

This section documents what a Tesla v3-revised P7 would have produced on the same Q1 2026 data. It does not alter P7's locked resolution. P7 scores FALSE.

**Reported Q1 2026 auto GM ex-credits:** 19.2%
*($3,042M gross profit on $15,854M auto revenue ex-credits, per the 10-Q)*

**Disclosed one-time items attributable to the auto segment:**

- Warranty reserve true-down: ~$230M (earnings call summary, Q1 2026)
- Auto-attributable tariff benefits: magnitude not separately disclosed by Tesla; CFO confirmed ~$250M in total tariff relief from duties paid earlier, with allocation between auto and energy segments unclear across sources

**Adjusted readings, three scenarios:**

| Scenario | Items stripped | Adjusted GM ex-credits |
|---|---|---|
| Conservative (warranty only) | $230M | 17.7% |
| Mid (warranty + partial auto tariff) | $350M | 17.0% |
| Aggressive (GLJ combined estimate) | $480M | 16.2% |

Under each scenario, Q1 lands below 18%. P7 under the revised spec would not have triggered on its first checkpoint.

**Interpretation.** The counterfactual indicates that the underlying mechanism reading — structural margin compression from relational damage — remains consistent with Q1's economic substance once Tesla's own separately-disclosed non-recurring items are removed. That's diagnostic value for Tesla v3 design. It is not diagnostic value for P7, which scores FALSE on the locked criterion as written.

**Discipline commitment.** Going forward, the adjusted margin series — stripped of regulatory credits *and* company-disclosed one-time items — gets computed every reporting period regardless of whether the reported metric agrees with Genesis's structural read. Running this strip-out selectively (only when the reported print disappoints) would convert the Tesla v3 improvement into the exact escape hatch the rest of this addendum exists to prevent. The symmetry test applies here too.

---

## Registry

This addendum attaches to SEER-2026-0003 and enters the Seer registry as its own hash-locked JSON artifact. The interpretation criteria above fix at publication. Post-Q2/Q3 analysis applying these criteria will publish as SEER-2026-0003-RESOLUTION.

| Field | Value |
|---|---|
| Parent forecast | SEER-2026-0003 |
| Addendum ID | SEER-2026-0003-ADDENDUM-P7 |
| Status | Locked — pre-Q2 2026 earnings |
| Lock date | [YYYY-MM-DD] |
| Registry | github.com/wakeupsmiling/seer |
| Hash | [SHA-256 at commit] |

---

*Protocol: Genesis Prediction Protocol v2.1 · Retrodiction Protocol +1 v0.5 · Evidence: Tesla Q1 2026 10-Q (filed April 2026), Tesla Q1 2026 shareholder deck, Tesla Q1 2026 earnings call transcript (April 22, 2026).*

*P7 full resolution: January 2027, post-Q3 2026 10-Q. Mechanism verdict published alongside.*


## END APRIL 2026 TEXT

---

# Registration notes

These were written at registration on 2026-08-30. They are not part of the April text and are not covered by
any lock except where a hash is named.

## 1. The locked criterion bundles the measurement with its interpretation

P7 as locked at 2026-03-23 reads:

> "Automotive gross margin (excluding regulatory credits) stays below 18%, confirming margin compression trajectory and R→F cascade propagation"

The criterion does not merely measure margin; it states that the margin test confirms "margin compression
trajectory and R→F cascade propagation." The addendum's central move — treating the binary resolution and
the mechanism verdict as two separable questions — is a departure from that text, which ties them together.

That separation is a sound lesson for future specs. It cannot be applied backward to SEER-2026-0003 without
amending a locked criterion, which the lock forbids. **P7 scores FALSE, and under the criterion as written
that failure bears on the R→F cascade claim.** The bundling was a specification error; recording it as one
is the honest treatment. Reading it away is not.

## 2. The two published documents define Brier differently

`SCORING_POLICY.md` v1.0 computes one Brier per forecast, from the primary scenario probability against the
weighted forecast score. The public Tesla forecast card describes a per-prediction Brier, and gives worked
examples ("a prediction at 85% that resolves correctly scores 0.0225"). The addendum's headline figure of
0.5625 follows the forecast card; `score.py` implements the policy.

Both are recorded in the registration JSON. Running `score.py` on this forecast in January 2027 will produce
a number that does not match what the forecast card promised readers. That reconciliation is a scoring-policy
decision and is still open.

## 3. The Q3 threshold, stated as a single number

With Q1 at 19.2% and Q2 at 16.3%, the interpretation table's tiebreaker reduces to one figure. The
equal-weighted mean of the three quarters reaches 18.0% only if

$$Q_3 \geq 3(18.0) - 19.2 - 16.3 = 18.5\%$$

So: **Q3 at or above 18.5% means the R→F cascade claim is substantially wrong. Below 18.5% and it
survives this test.** One number, checkable in October, fixed before the data. This is the only part of this
artifact that carries a pre-commitment claim, and the hash above is what makes it checkable.

## 4. Why this sat unrecorded for four months

Seer v0's forecast object cannot represent a criterion that resolves early. `score.py` writes a
whole-forecast resolution and flips status to `scored`; the schema's status enum offers no partially-resolved
state; and `additionalProperties: false` blocks adding one. There was nowhere to put a single failed
criterion. The result is recorded in the parent's `monitoring` block, which is mutable and unhashed — the
honest place for it, and a weaker record than the miss deserves.

**Recommended for v1:** a `partial_resolutions` array on the forecast object, hashed at the time each
criterion resolves, plus a `partially_resolved` status. A registry that can only record outcomes at the
horizon will keep losing early falsifications, and early falsifications are the ones that carry the most
calibration information.
