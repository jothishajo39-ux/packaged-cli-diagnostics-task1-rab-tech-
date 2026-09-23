# Packaged CLI Diagnostics Tool

A small installable Python command-line tool that inspects a machine and
produces a human-readable or JSON diagnostic report.

## Features

- Python version and executable information
- Disk-space inspection
- Selected environment-variable checks
- Detection of Git, pip, and pytest
- Diagnostic event analysis
- Structured JSON output
- Useful exit codes
- Unit tests for success, missing paths, and malformed configuration

## Installation

Create and activate a virtual environment, then install the project:

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

pip install .
```

## Usage

Human-readable report:

```bash
diagnostics --events samples/diagnostic-events.json
```

JSON report:

```bash
diagnostics --events samples/diagnostic-events.json --json
```

Save a JSON report:

```bash
diagnostics --events samples/diagnostic-events.json --output reports/sample-report.json
```

## Exit codes

- `0` = PASS/WARN completed successfully
- `1` = diagnostic events contain errors
- `2` = requested configuration/event path is missing
- `3` = malformed JSON/configuration
- `4` = unexpected runtime error

## Tests

```bash
pip install pytest
pytest
```
