import argparse
import json
import sys

from .diagnostics import analyze_events, load_events
from .report import build_report, human_report, save_json
from .system_info import get_system_info


def main():
    parser = argparse.ArgumentParser(
        description="Inspect a machine and produce a diagnostic report."
    )
    parser.add_argument(
        "--events",
        default="samples/diagnostic-events.json",
        help="Path to diagnostic events JSON file.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print structured JSON instead of a human-readable report.",
    )
    parser.add_argument(
        "--output",
        help="Optional path to save the JSON report.",
    )
    args = parser.parse_args()

    try:
        data = load_events(args.events)
        report = build_report(get_system_info(), analyze_events(data))

        if args.output:
            save_json(report, args.output)

        if args.json:
            print(json.dumps(report, indent=2))
        else:
            print(human_report(report))

        return 1 if report["overall_status"] == "FAIL" else 0

    except FileNotFoundError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 3
    except Exception as exc:
        print(f"ERROR: Unexpected failure: {exc}", file=sys.stderr)
        return 4


if __name__ == "__main__":
    raise SystemExit(main())
