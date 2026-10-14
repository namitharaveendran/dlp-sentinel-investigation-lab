# DLP Sentinel — Investigation Lab

## Overview

DLP Sentinel is a Python-based cybersecurity learning project that generates synthetic Data Loss Prevention (DLP) events, detects potentially risky activities using configurable rules, and produces initial investigation records.

The project demonstrates foundational skills in security monitoring, alert triage, investigation documentation, and Python-based log analysis.

## Features

- Synthetic DLP event generation
- Rule-based detection of potentially risky data-handling activities
- Initial alert prioritisation
- Investigation recommendations
- CSV-based alert and investigation records
- Markdown incident investigation report

## Technology Stack

- Python 3.10
- pandas
- CSV datasets
- PowerShell
- Visual Studio Code

## Project Structure

```text
dlp-sentinel-investigation-lab/
├── data/
│   ├── synthetic_dlp_events.csv
│   └── dlp_alerts.csv
├── reports/
│   ├── investigation_log.csv
│   └── incident_investigation_report.md
├── generate_events.py
├── detect_alerts.py
├── investigate_alerts.py
└── README.md
```

## Workflow

1. Generate synthetic DLP events.
2. Apply detection rules to identify potentially risky activity.
3. Assign initial priorities and recommend investigation actions.
4. Save selected investigation records to CSV.
5. Document findings, limitations, and follow-up actions.

## How to Run

Activate your virtual environment and run:

```powershell
python generate_events.py
python detect_alerts.py
python investigate_alerts.py
```

Run these commands in order because each stage uses output from the previous stage.

Install the required dependency with:

```powershell
python -m pip install pandas
```

## Important Limitations

This is a learning lab using synthetic data. Its alerts and priority assignments are not proof of a confirmed data leak, malicious intent, or a real policy violation. Investigation outcomes remain inconclusive until supported by additional evidence.

## Future Improvements

- Add configurable detection thresholds
- Improve duplicate-alert handling
- Add unit tests for detection rules
- Measure alert quality and false positives
- Add automated tests and sample investigation scenarios

## Disclaimer

This project is intended for educational and defensive cybersecurity practice. It does not connect to production systems or monitor real employees.