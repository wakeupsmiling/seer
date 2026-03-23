#!/usr/bin/env python3
"""
Seer v0 — Scoring Script

Takes a locked forecast object and outcome data, computes:
  - Component scores (per resolution criterion)
  - Weighted aggregate forecast score
  - Brier score
  - Log score
  - Differential accuracy (Seer vs. declared baseline)

Usage:
    python3 score.py <forecast_id> <outcome_file>

    forecast_id: e.g., SEER-2026-0001
    outcome_file: JSON file with outcome data

Outcome file format:
{
    "outcome_evidence": ["Evidence item 1", "Evidence item 2"],
    "component_outcomes": [
        {
            "criterion": "criterion text (must match spec)",
            "outcome": "what actually happened",
            "score": 0.0 to 1.0
        }
    ],
    "baseline_outcome": "What the baseline actually predicted and how it fared",
    "baseline_score": 0.0 to 1.0,
    "calibration_notes": "Optional notes on what this reveals"
}
"""

import argparse
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
FORECASTS_DIR = PROJECT_DIR / "forecasts"


def compute_brier(predicted_prob: float, outcome: float) -> float:
    """
    Brier score: (predicted_probability - outcome)^2
    outcome is 1.0 if the predicted event occurred, 0.0 if not.
    Perfect = 0.0, worst = 1.0, coin flip = 0.25.
    """
    return (predicted_prob - outcome) ** 2


def compute_log_score(predicted_prob: float, outcome: float) -> float:
    """
    Logarithmic scoring rule: -log(p) where p is the probability assigned
    to the event that actually occurred.
    More punishing of confident wrong predictions than Brier.
    """
    # Clamp to avoid log(0)
    eps = 1e-10
    if outcome >= 0.5:
        p = max(predicted_prob, eps)
    else:
        p = max(1.0 - predicted_prob, eps)
    return -math.log(p)


def compute_weighted_aggregate(component_scores: list, resolution_criteria: list) -> float:
    """
    Compute weighted aggregate score from component scores and their weights.
    """
    total = 0.0
    weight_sum = 0.0
    for comp in component_scores:
        # Find matching criterion weight
        criterion_text = comp["criterion"]
        weight = None
        for rc in resolution_criteria:
            if rc["criterion"] == criterion_text:
                weight = rc["weight"]
                break
        if weight is None:
            print(f"  Warning: No matching weight for criterion '{criterion_text}'. Using equal weight.")
            weight = 1.0 / len(component_scores)
        total += comp["score"] * weight
        weight_sum += weight

    if weight_sum == 0:
        return 0.0
    return total / weight_sum


def main():
    parser = argparse.ArgumentParser(description="Seer v0 Scoring Script")
    parser.add_argument("forecast_id", help="Forecast ID, e.g., SEER-2026-0001")
    parser.add_argument("outcome_file", help="Path to JSON file with outcome data")
    args = parser.parse_args()

    # Load forecast object
    forecast_path = FORECASTS_DIR / f"{args.forecast_id}.json"
    if not forecast_path.exists():
        print(f"Error: Forecast object not found: {forecast_path}")
        sys.exit(1)

    with open(forecast_path) as f:
        forecast_obj = json.load(f)

    # Verify forecast is locked
    if not forecast_obj.get("forecast_hash"):
        print(f"Error: Forecast {args.forecast_id} has not completed Lock C. Cannot score.")
        sys.exit(1)

    # Load outcome data
    try:
        with open(args.outcome_file) as f:
            outcome = json.load(f)
    except FileNotFoundError:
        print(f"Error: Outcome file not found: {args.outcome_file}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in outcome file: {e}")
        sys.exit(1)

    # Validate outcome structure
    required_fields = ["outcome_evidence", "component_outcomes"]
    for field in required_fields:
        if field not in outcome:
            print(f"Error: Outcome file missing required field: '{field}'")
            sys.exit(1)

    # Compute weighted aggregate
    resolution_criteria = forecast_obj["specification"]["resolution_criteria"]
    component_scores = outcome["component_outcomes"]
    forecast_score = compute_weighted_aggregate(component_scores, resolution_criteria)

    # Compute Brier score
    # Use the primary scenario probability as the predicted probability
    # and the forecast score as the outcome indicator
    scenarios = forecast_obj["forecast"]["scenarios"]
    # The base case / highest-probability scenario
    primary_scenario = max(scenarios, key=lambda s: s["probability"])
    primary_prob = primary_scenario["probability"]
    # Brier: how well calibrated was the primary prediction?
    # outcome = forecast_score (1.0 = perfectly right, 0.0 = completely wrong)
    brier = compute_brier(primary_prob, forecast_score)

    # Compute Log score
    log_score = compute_log_score(primary_prob, forecast_score)

    # Compute differential accuracy
    baseline_score = outcome.get("baseline_score")
    differential = None
    if baseline_score is not None:
        differential = forecast_score - baseline_score

    # Build resolution object
    resolution = {
        "resolved_at": datetime.now(timezone.utc).isoformat(),
        "outcome_evidence": outcome["outcome_evidence"],
        "component_scores": component_scores,
        "forecast_score": round(forecast_score, 4),
        "brier_score": round(brier, 4),
        "log_score": round(log_score, 4),
        "baseline_outcome": outcome.get("baseline_outcome", ""),
        "calibration_notes": outcome.get("calibration_notes", ""),
    }
    if differential is not None:
        resolution["differential_accuracy"] = round(differential, 4)

    # Write resolution into forecast object
    forecast_obj["resolution"] = resolution
    forecast_obj["status"] = "scored"

    with open(forecast_path, "w") as f:
        json.dump(forecast_obj, f, indent=2, ensure_ascii=False)

    # Report
    print()
    print(f"  === Scoring Complete: {args.forecast_id} ===")
    print()
    print(f"  Forecast score (weighted aggregate): {forecast_score:.4f}")
    print(f"  Brier score:                         {brier:.4f}")
    print(f"  Log score:                           {log_score:.4f}")
    if differential is not None:
        sign = "+" if differential > 0 else ""
        print(f"  Differential accuracy (vs baseline): {sign}{differential:.4f}")
        if differential > 0:
            print(f"    → Seer outperformed the baseline.")
        elif differential < 0:
            print(f"    → Baseline outperformed Seer.")
        else:
            print(f"    → Seer matched the baseline.")
    print()
    print(f"  Component scores:")
    for comp in component_scores:
        print(f"    - {comp['criterion']}: {comp['score']:.2f} ({comp['outcome']})")
    print()
    print(f"  Status updated to: SCORED")
    print(f"  Saved to: {forecast_path}")
    print()
    print(f"  Next steps:")
    print(f"    1. Review the scores and calibration notes")
    print(f"    2. Push to the registry: git add, git commit, git push")
    print(f"    3. Write the Substack post if this is a public forecast")


if __name__ == "__main__":
    main()
