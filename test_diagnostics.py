import json
from pathlib import Path

import pytest

from diagnostics.diagnostics import analyze_events, load_events


def test_success(tmp_path):
    data = {"events": [{"service": "demo", "level": "INFO", "status_code": 200}]}
    path = tmp_path / "events.json"
    path.write_text(json.dumps(data), encoding="utf-8")

    loaded = load_events(path)
    result = analyze_events(loaded)

    assert result["event_count"] == 1
    assert result["status"] == "PASS"


def test_missing_dependency_path():
    with pytest.raises(FileNotFoundError):
        load_events("does-not-exist.json")


def test_malformed_configuration(tmp_path):
    path = tmp_path / "bad.json"
    path.write_text("{invalid-json", encoding="utf-8")

    with pytest.raises(ValueError, match="Malformed configuration"):
        load_events(path)
