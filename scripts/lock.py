#!/usr/bin/env python3
"""
Seer v0 — Lock Script

Takes a JSON file (specification, evidence summary, or forecast),
validates it against its schema, computes SHA-256 hash, records UTC
timestamp, and writes the result into a forecast object.

Usage:
    python3 lock.py <phase> <json_file> [--forecast-id SEER-YYYY-NNNN]

    phase: spec | evidence | forecast
    json_file: path to the JSON file to lock

Examples:
    # Lock a new specification (creates a new forecast object):
    python3 lock.py spec my_spec.json

    # Lock evidence into an existing forecast object:
    python3 lock.py evidence my_evidence.json --forecast-id SEER-2026-0001

    # Lock the forecast into an existing forecast object:
    python3 lock.py forecast my_forecast.json --forecast-id SEER-2026-0001
"""

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# Paths relative to this script
SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent
SCHEMAS_DIR = PROJECT_DIR / "schemas"
FORECASTS_DIR = PROJECT_DIR / "forecasts"

PHASE_CONFIG = {
    "spec": {
        "schema_file": "specification.schema.json",
        "object_key": "specification",
        "hash_key": "specification_hash",
        "locked_at_key": "specification_locked_at",
        "lock_name": "Lock A (Specification)",
    },
    "evidence": {
        "schema_file": "evidence_summary.schema.json",
        "object_key": "evidence_summary",
        "hash_key": "evidence_hash",
        "locked_at_key": "evidence_locked_at",
        "lock_name": "Lock B (Evidence)",
    },
    "forecast": {
        "schema_file": "forecast.schema.json",
        "object_key": "forecast",
        "hash_key": "forecast_hash",
        "locked_at_key": "forecast_locked_at",
        "lock_name": "Lock C (Forecast)",
    },
}


def compute_hash(data: dict) -> str:
    """Compute SHA-256 hash of canonical JSON (sorted keys, no extra whitespace)."""
    canonical = json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def generate_forecast_id() -> str:
    """Generate the next forecast ID by scanning existing forecasts."""
    year = datetime.now(timezone.utc).strftime("%Y")
    existing = list(FORECASTS_DIR.glob(f"SEER-{year}-*.json"))
    if not existing:
        return f"SEER-{year}-0001"
    numbers = []
    for f in existing:
        try:
            num = int(f.stem.split("-")[-1])
            numbers.append(num)
        except ValueError:
            continue
    next_num = max(numbers) + 1 if numbers else 1
    return f"SEER-{year}-{next_num:04d}"


def validate_json(data: dict, schema_file: str) -> list[str]:
    """
    Basic structural validation against required fields.
    Uses the schema file to check required properties.
    (Full jsonschema validation available if jsonschema package is installed.)
    """
    errors = []
    try:
        import jsonschema
        schema_path = SCHEMAS_DIR / schema_file
        with open(schema_path) as f:
            schema = json.load(f)
        jsonschema.validate(data, schema)
    except ImportError:
        # Fall back to basic required-field checking
        schema_path = SCHEMAS_DIR / schema_file
        with open(schema_path) as f:
            schema = json.load(f)
        required = schema.get("required", [])
        for field in required:
            if field not in data:
                errors.append(f"Missing required field: '{field}'")
    except Exception as e:
        errors.append(str(e))
    return errors


def load_or_create_forecast_object(forecast_id: str = None, phase: str = None) -> tuple[dict, str]:
    """Load an existing forecast object or create a new one."""
    if forecast_id:
        forecast_path = FORECASTS_DIR / f"{forecast_id}.json"
        if not forecast_path.exists():
            print(f"Error: Forecast object {forecast_id} not found at {forecast_path}")
            sys.exit(1)
        with open(forecast_path) as f:
            return json.load(f), forecast_id
    else:
        if phase != "spec":
            print("Error: --forecast-id is required for evidence and forecast locks.")
            print("       Only 'spec' creates a new forecast object.")
            sys.exit(1)
        forecast_id = generate_forecast_id()
        now = datetime.now(timezone.utc).isoformat()
        forecast_obj = {
            "id": forecast_id,
            "created": now,
            "status": "draft",
        }
        return forecast_obj, forecast_id


def main():
    parser = argparse.ArgumentParser(description="Seer v0 Lock Script")
    parser.add_argument("phase", choices=["spec", "evidence", "forecast"],
                        help="Which phase to lock: spec, evidence, or forecast")
    parser.add_argument("json_file", help="Path to the JSON file to lock")
    parser.add_argument("--forecast-id", dest="forecast_id", default=None,
                        help="Existing forecast ID (required for evidence and forecast phases)")
    args = parser.parse_args()

    config = PHASE_CONFIG[args.phase]

    # Load the input JSON
    try:
        with open(args.json_file) as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found: {args.json_file}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {args.json_file}: {e}")
        sys.exit(1)

    # Validate against schema
    errors = validate_json(data, config["schema_file"])
    if errors:
        print(f"Validation errors for {config['lock_name']}:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)

    # Load or create forecast object
    FORECASTS_DIR.mkdir(parents=True, exist_ok=True)
    forecast_obj, forecast_id = load_or_create_forecast_object(args.forecast_id, args.phase)

    # Check that this phase hasn't already been locked
    if config["hash_key"] in forecast_obj and forecast_obj[config["hash_key"]]:
        print(f"Error: {config['lock_name']} is already locked for {forecast_id}.")
        print(f"  Existing hash: {forecast_obj[config['hash_key']]}")
        print(f"  Locked at:     {forecast_obj[config['locked_at_key']]}")
        print(f"  Locked objects are immutable. To revise, create a successor forecast.")
        sys.exit(1)

    # Compute hash and timestamp
    content_hash = compute_hash(data)
    locked_at = datetime.now(timezone.utc).isoformat()

    # Write into forecast object
    forecast_obj[config["object_key"]] = data
    forecast_obj[config["hash_key"]] = content_hash
    forecast_obj[config["locked_at_key"]] = locked_at

    # Update status
    if args.phase == "forecast":
        forecast_obj["status"] = "locked"
    elif args.phase == "spec" and forecast_obj.get("status") == "draft":
        pass  # Stay draft until all locks are confirmed

    # Save
    forecast_path = FORECASTS_DIR / f"{forecast_id}.json"
    with open(forecast_path, "w") as f:
        json.dump(forecast_obj, f, indent=2, ensure_ascii=False)

    # Report
    print()
    print(f"  === {config['lock_name']} Confirmed ===")
    print()
    print(f"  Forecast ID:  {forecast_id}")
    print(f"  SHA-256:      {content_hash}")
    print(f"  Locked at:    {locked_at}")
    print(f"  Saved to:     {forecast_path}")
    print()

    if args.phase == "forecast":
        print(f"  All three locks confirmed. Status: LOCKED.")
        print(f"  This forecast is now immutable and ready for publication.")
        print()
        print(f"  Next steps:")
        print(f"    1. Review the forecast object: {forecast_path}")
        print(f"    2. Generate the report (see templates/)")
        print(f"    3. Push to the registry: git add, git commit, git push")
    elif args.phase == "spec":
        print(f"  Specification locked. Proceed to research phase.")
        print(f"  When evidence is ready, run:")
        print(f"    python3 lock.py evidence <evidence.json> --forecast-id {forecast_id}")
    elif args.phase == "evidence":
        print(f"  Evidence locked. Proceed to diagnostic and prediction phases.")
        print(f"  When forecast is ready, run:")
        print(f"    python3 lock.py forecast <forecast.json> --forecast-id {forecast_id}")


if __name__ == "__main__":
    main()
