
# DLP Sentinel — Investigation Lab

[![DLP Sentinel Tests](https://github.com/namitharaveendran/dlp-sentinel-investigation-lab/actions/workflows/tests.yml/badge.svg)](https://github.com/namitharaveendran/dlp-sentinel-investigation-lab/actions/workflows/tests.yml)

## Overview

DLP Sentinel is a Python-based cybersecurity learning project that generates synthetic Data Loss Prevention (DLP) events, applies five rule-based detection conditions, and produces alert records for investigation.

The project demonstrates foundational skills in DLP monitoring simulation, security event analysis, detection-rule validation, incident documentation, simulated SLA tracking, automated testing, and continuous integration.

The project uses fictional data and illustrative review targets. It is not a production DLP platform and does not connect to an enterprise DLP service.

## Features

- Synthetic DLP event generation
- Five rule-based detection conditions
- Severity-based alert generation
- Detection of potentially risky external sharing and data transfers
- Bulk-download threshold monitoring
- Cloud-upload and removable-media activity checks
- CSV-based alert and investigation records
- Incident register with priorities, analyst actions, and escalation reasons
- Simulated SLA calculation and review-target tracking
- Eight executable DLP scenario validations
- Fourteen automated unit tests
- Markdown incident investigation report
- GitHub Actions workflow for automated testing and scenario validation

## Technology Stack

- Python 3.10
- pandas
- CSV datasets
- Python `unittest`
- Git and GitHub
- GitHub Actions
- PowerShell
- Visual Studio Code

## Project Structure

```text
dlp-sentinel-investigation-lab/
├── .github/
│   └── workflows/
│       └── tests.yml
├── data/
│   ├── synthetic_dlp_events.csv
│   └── dlp_alerts.csv
├── reports/
│   ├── investigation_log.csv
│   ├── incident_investigation_report.md
│   ├── incident_register.csv
│   ├── sla_results.csv
│   └── dlp_scenario_validation.csv
├── generate_events.py
├── detect_alerts.py
├── investigate_alerts.py
├── calculate_sla.py
├── validate_scenarios.py
├── test_detect_alerts.py
├── test_calculate_sla.py
├── requirements.txt
├── .gitignore
└── README.md
```

The `.venv/` directory is created locally during setup and is excluded from Git.

## Detection Rules

| Rule ID | Detection condition | Severity |
|---|---|---|
| DLP-001 | Confidential or Restricted data sent to an unapproved destination | High |
| DLP-002 | External sharing involving Confidential or Restricted information | High |
| DLP-003 | Bulk download involving at least 100 files | Medium |
| DLP-004 | Upload to the configured `unapproved_cloud` destination | High for Confidential or Restricted data; otherwise Medium |
| DLP-005 | Copy to a `usb_drive` destination without approval | Medium |

These custom rules identify activity requiring review. An alert does not, by itself, establish a confirmed data leak, malicious intent, or policy violation.

An event can trigger multiple rules. For example, a sensitive upload to an unapproved cloud destination can trigger both DLP-001 and DLP-004.

## Workflow

1. Generate synthetic DLP events.
2. Apply five detection rules.
3. Assign severity based on configured conditions.
4. Save alert records to CSV.
5. Select events for initial investigation.
6. Record priorities, analyst actions, recommendations, and dispositions.
7. Calculate elapsed review time against illustrative SLA targets.
8. Validate expected detection behaviour through executable scenarios.
9. Run automated unit tests and scenario validation in GitHub Actions.

## Setup

### 1. Clone the repository

```powershell
git clone https://github.com/namitharaveendran/dlp-sentinel-investigation-lab.git
cd dlp-sentinel-investigation-lab
```

### 2. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

## How to Run

Execute the scripts from the project root.

### Generate synthetic events

```powershell
python generate_events.py
```

This generates the fictional event dataset in `data/synthetic_dlp_events.csv`.

### Generate DLP alerts

```powershell
python detect_alerts.py
```

This applies the five detection rules and writes alert records to `data/dlp_alerts.csv`.

### Generate investigation records

```powershell
python investigate_alerts.py
```

This creates initial investigation records and the investigation report according to the implemented workflow.

### Calculate simulated SLA results

```powershell
python calculate_sla.py
```

This reads `reports/incident_register.csv`, calculates elapsed review time, compares it with the configured targets, and writes `reports/sla_results.csv`.

### Validate DLP scenarios

```powershell
python validate_scenarios.py
```

This executes eight synthetic scenarios against the actual `detect_alerts()` function and writes the results to `reports/dlp_scenario_validation.csv`.

A failed scenario causes the script to exit with a non-zero status, allowing the CI workflow to detect the failure.

**Note:** Running the event generator again overwrites the existing synthetic dataset. Generated records are fictional.

## Detection Scenario Validation

The scenario validator covers eight executable scenarios.

| Scenario | Expected behaviour |
|---|---|
| Sensitive data to an unapproved destination | DLP-001, High |
| Sensitive external file sharing | DLP-002, High |
| Bulk download of 100 files | DLP-003, Medium |
| Bulk download of 99 files | No alert from DLP-003 |
| Sensitive upload to unapproved cloud | DLP-004, High |
| Internal upload to unapproved cloud | DLP-004, Medium |
| Unapproved USB transfer | DLP-005, Medium |
| Approved public USB transfer | No alert from DLP-005 |

The scenarios validate selected rule conditions and severity assignments. Some events can trigger more than one rule, and the validator accounts for the expected rule being present.

Invalid destination-approval input is tested separately in the unit test suite.

## Automated Testing

DLP Sentinel includes 14 unit tests implemented using Python's built-in `unittest` framework.

### DLP detection tests

Nine tests cover:

- Sensitive data sent to an unapproved destination
- Sensitive external sharing
- Bulk-download threshold behaviour at 100 files
- Non-triggering behaviour below the threshold
- High severity for sensitive cloud uploads
- Medium severity for internal cloud uploads
- Unapproved USB transfer
- Approved USB activity handling
- Rejection of invalid destination-approval values

Run:

```powershell
python -m unittest -v test_detect_alerts.py
```

### SLA calculation tests

Five tests cover:

- Review completed within the SLA target
- Review completed after the SLA target
- Review exactly at the SLA boundary
- Rejection of a review timestamp before incident creation
- Rejection of a zero SLA target

Run:

```powershell
python -m unittest -v test_calculate_sla.py
```

### Run both test suites

```powershell
python -m unittest -v test_detect_alerts.py test_calculate_sla.py
```

The expected result is 14 passing tests when the current implementation remains unchanged.

### Run scenario validation

```powershell
python validate_scenarios.py
```

The previously observed validation result was eight scenarios passed and zero failed.

Re-run the commands after modifying the detection logic, test cases, or validation scenarios.

## Continuous Integration with GitHub Actions

The workflow is defined in `.github/workflows/tests.yml`.

It runs on pushes and pull requests targeting `main`, and supports manual execution through the GitHub Actions interface.

The workflow:

1. Checks out the repository.
2. Sets up Python 3.10.
3. Installs dependencies from `requirements.txt`.
4. Runs the DLP detection unit tests.
5. Runs the SLA calculation unit tests.
6. Executes DLP scenario validation.

The repository has had three successful workflow runs during development. Workflow status can be viewed on the [GitHub Actions page](https://github.com/namitharaveendran/dlp-sentinel-investigation-lab/actions).

## Observed Results

The initial synthetic dataset run produced these results.

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

These figures are observed results from the initial synthetic dataset, not benchmarks of real-world detection performance. Alert records can exceed unique events because one event can trigger multiple rules.

## Incident Management and Investigation

The incident register is stored at `reports/incident_register.csv`.

It contains five illustrative incident records with fields for:

- Incident and event identifiers
- Priority and status
- Creation and first-review timestamps
- Configured review-target duration
- Analyst action and escalation reason
- Disposition and evidence limitations

The sample records demonstrate how a DLP analyst can document review and escalation decisions.

All example dispositions remain `Inconclusive` because the dataset does not independently establish authorization, actual data transfer, or data exposure.

A suspicious alert should not automatically be treated as a confirmed incident. A real investigation would require appropriate identity, access, approval, endpoint, cloud, or network evidence.

## Simulated SLA Monitoring

The SLA calculation module compares the elapsed time between incident creation and first review with a configured target.

Run:

```powershell
python calculate_sla.py
```

The output is saved to `reports/sla_results.csv`.

For the current illustrative sample, the expected results are:

| Metric | Result |
|---|---:|
| Incidents analysed | 5 |
| Review targets met | 3 |
| Review targets breached | 2 |

These are simulated results based on manually supplied example timestamps and review targets. They do not represent real operational performance, company SLAs, or compliance with an external standard.

## Enterprise DLP Learning

The project uses custom Python rules and does not integrate with Microsoft Purview or another production DLP platform.

Enterprise DLP concepts that can be studied alongside this lab include:

- Sensitive information identification
- Policy conditions and exceptions
- Data movement restrictions
- Alert review and investigation
- User notifications and escalation
- False-positive analysis

For introductory material, refer to [Microsoft Learn — Data Loss Prevention](https://learn.microsoft.com/en-us/purview/dlp-learn-about-dlp).

Studying these concepts does not constitute hands-on experience with the enterprise platform. Any future platform practice should be documented separately and accurately.

## Limitations

- All event records are synthetic.
- Detection conditions and severity assignments are predefined.
- Test coverage addresses selected behaviours, not every possible event or attack.
- Scenario validation uses constructed test events and does not establish production detection accuracy.
- The incident register contains illustrative records.
- SLA targets and timestamps are fictional.
- No production DLP platform integration is implemented.
- No real-world false-positive rate or detection accuracy has been established.
- The project does not prove that real data exfiltration occurred.

## Future Improvements

- Add configurable detection thresholds.
- Expand automated tests with additional edge cases.
- Improve duplicate-alert handling.
- Add scenario checks for all detection-rule interactions.
- Generate richer investigation evidence and audit fields.
- Add automated validation for incident-register data.
- Explore authorised hands-on practice with enterprise DLP tooling.
- Improve reporting and visualisation of alerts and review metrics.

## Disclaimer

DLP Sentinel is an educational and defensive cybersecurity project. It uses fictional data and does not monitor real employees, access actual confidential information, or connect to production systems.
