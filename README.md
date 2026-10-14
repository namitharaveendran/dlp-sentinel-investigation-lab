
# DLP Sentinel — Investigation Lab

## Overview

DLP Sentinel is a Python-based cybersecurity learning project that generates synthetic Data Loss Prevention (DLP) events, detects potentially risky data-handling activities using five rule-based detection conditions, and produces initial investigation records.

The project demonstrates foundational skills in security monitoring, alert triage, rule-based detection, investigation documentation, and Python-based log analysis.

**Note:** This is a learning lab using fictional data. It is not a production DLP platform.

## Features

- Synthetic DLP event generation
- Five rule-based detection conditions
- Severity-based alert generation
- Detection of potentially risky external sharing and data transfers
- Bulk-download threshold monitoring
- Cloud-upload and removable-media activity checks
- CSV-based alert and investigation records
- Initial investigation priorities and recommended actions
- Markdown incident investigation report
- Automated unit tests using Python's `unittest` framework

## Technology Stack

- Python 3.10
- pandas
- CSV datasets
- Python `unittest`
- Git and GitHub
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
├── test_detect_alerts.py
├── requirements.txt
├── .gitignore
└── README.md
```

The `.venv/` directory is created locally when setting up the virtual environment and is excluded from Git.

## Detection Rules

| Rule ID | Detection condition | Severity |
|---|---|---|
| DLP-001 | Confidential or Restricted data sent to an unapproved destination | High |
| DLP-002 | External sharing involving Confidential or Restricted information | High |
| DLP-003 | Bulk download involving at least 100 files | Medium |
| DLP-004 | Upload to the configured `unapproved_cloud` destination | High for Confidential or Restricted data; otherwise Medium |
| DLP-005 | Copy to a `usb_drive` destination without approval | Medium |

These rules identify activity requiring review. An alert does not, by itself, establish a confirmed data leak, malicious intent, or policy violation.

## Workflow

1. Generate 30 synthetic DLP events.
2. Apply the five detection rules.
3. Assign alert severity based on the configured conditions.
4. Save generated alert records to CSV.
5. Select events for initial investigation.
6. Record priorities, recommendations, and investigation dispositions.
7. Document findings, limitations, and follow-up actions.

## Setup

### 1. Clone the repository

```powershell
git clone https://github.com/namitharaveendran/dlp-sentinel-investigation-lab.git
cd dlp-sentinel-investigation-lab
```

### 2. Create a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

## How to Run

Run the scripts in this order from the project root:

```powershell
python generate_events.py
python detect_alerts.py
python investigate_alerts.py
```

The scripts generate the synthetic dataset, produce alert records, and create the initial investigation log.

Running the event generator again overwrites the existing synthetic dataset. The generated records are fictional.

## Automated Testing

DLP Sentinel includes automated unit tests implemented with Python's built-in `unittest` framework.

The test suite contains nine tests covering:

- All five detection rules
- Bulk-download threshold behaviour at 100 files
- Non-triggering behaviour below the threshold
- Severity assignment for cloud uploads
- Approved USB activity handling
- Rejection of invalid destination-approval values

Run the tests with:

```powershell
python -m unittest -v test_detect_alerts.py
```

**Latest recorded test result:** 9 tests passed, 0 failures.

This result applies to the tested scenarios and code version. Re-run the tests after making changes.

## Observed Results

The initial synthetic dataset run produced the following results:

| Metric | Observed result |
|---|---:|
| Source events analysed | 30 |
| Alert records generated | 30 |
| Unique events flagged | 21 |
| High-severity alert records | 18 |
| Medium-severity alert records | 12 |
| Unique events selected for initial investigation | 5 |

### Alert records by rule

| Rule ID | Alert records |
|---|---:|
| DLP-001 | 9 |
| DLP-002 | 6 |
| DLP-003 | 6 |
| DLP-004 | 6 |
| DLP-005 | 3 |

These are observed results from the synthetic dataset, not benchmarks of real-world detection performance. One event can trigger multiple rules, so alert records can exceed the number of unique events flagged.

## Investigation and Evidence Handling

The investigation workflow records initial priorities, reasons for review, and recommended actions.

Before reaching a final disposition, an analyst should validate authorization and business context, review applicable policy and approval records, and correlate relevant identity, endpoint, cloud, or network evidence when available.

The current lab uses synthetic event fields. It does not independently verify user identities, authorization records, or actual file transfers. Investigation dispositions therefore remain **Inconclusive** until supported by additional evidence.

## Limitations

- The dataset is synthetic and does not represent production telemetry.
- Detection conditions and severity assignments are predefined and require validation.
- The tests validate selected rule behaviours, not every possible event or attack scenario.
- No production DLP platform integration is implemented.
- The project does not establish a real-world false-positive rate or production detection accuracy.

## Future Improvements

- Add configurable detection thresholds.
- Expand automated test coverage with additional edge cases.
- Improve duplicate-alert handling.
- Evaluate detection quality using labelled test data.
- Add richer investigation evidence and audit fields.
- Explore authorised hands-on practice with enterprise DLP tooling.

## Disclaimer

This project is intended for educational and defensive cybersecurity practice. It uses fictional data and does not monitor real employees or connect to production systems.
