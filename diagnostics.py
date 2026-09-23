import json
from pathlib import Path


def load_events(path):
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Configuration path not found: {path}")

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Malformed configuration: {exc}") from exc

    if not isinstance(data, dict) or not isinstance(data.get("events"), list):
        raise ValueError("Malformed configuration: 'events' must be a list")

    return data


def analyze_events(data):
    events = data["events"]
    errors = [e for e in events if e.get("level") == "ERROR"]
    warnings = [e for e in events if e.get("level") == "WARN"]

    valid_status_codes = all(
        isinstance(e.get("status_code"), int) for e in events
    )

    return {
        "event_count": len(events),
        "error_count": len(errors),
        "warning_count": len(warnings),
        "services": sorted({e.get("service") for e in events if e.get("service")}),
        "status": "FAIL" if errors else ("WARN" if warnings else "PASS"),
        "status_codes_valid": valid_status_codes,
    }
