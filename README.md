# DLP Sentinel — DLP Detection & Investigation Lab

[![DLP Sentinel Tests](https://github.com/namitharaveendran/dlp-sentinel-investigation-lab/actions/workflows/tests.yml/badge.svg)](https://github.com/namitharaveendran/dlp-sentinel-investigation-lab/actions/workflows/tests.yml)

A Python-based Data Loss Prevention (DLP) detection and investigation lab that identifies simulated sensitive-data handling risks, generates rule-based alerts, validates detection scenarios, and calculates incident review SLA results.

This project demonstrates foundational skills in security monitoring, alert triage, incident investigation, detection testing, security documentation, and workflow automation.

> **Project scope:** This is a learning lab using synthetic event data and illustrative incident records. It is not a production DLP deployment and does not integrate with Microsoft Purview or another enterprise DLP platform.

## Objectives

- Implement transparent, rule-based DLP detection conditions.
- Assign alert severity based on event characteristics.
- Test detection thresholds and approval validation.
- Validate expected outcomes against repeatable scenarios.
- Maintain structured incident investigation records.
- Calculate incident review times against illustrative SLA targets.
- Automate testing and scenario validation through GitHub Actions.

## Detection Rules

The detection engine implements five rules:

| Rule ID | Detection condition | Severity |
|---|---|---|
| DLP-001 | Sensitive data sent to an unapproved destination | High |
| DLP-002 | Sensitive information shared externally | High |
| DLP-003 | Bulk download of 100 or more files | Medium |
| DLP-004 | Upload to an unapproved cloud destination | High for sensitive data; Medium otherwise |
| DLP-005 | Unapproved removable-media transfer to a USB drive | Medium |

A single event may trigger multiple rules. For example, a sensitive upload to an unapproved cloud destination can trigger both DLP-001 and DLP-004.

These are custom Python rules designed for this lab, not native enterprise DLP policies.

## Investigation Workflow

1. **Event analysis:** Read the synthetic event dataset.
2. **Detection:** Evaluate events against the five predefined rules.
3. **Alert generation:** Record triggered rules and assigned severity.
4. **Scenario validation:** Compare actual results with expected rules and severity.
5. **Incident investigation:** Document initial findings and recommended actions.
6. **SLA review:** Calculate elapsed time to first review and compare it with the configured target.
7. **Automated testing:** Execute unit tests and scenario validations locally and through GitHub Actions.

## Technology Stack

- **Language:** Python 3.10
- **Data processing:** pandas
- **Testing:** Python `unittest`
- **Version control:** Git and GitHub
- **CI automation:** GitHub Actions
- **Input and output:** CSV datasets and Markdown reports

## Repository Structure

```text
dlp-sentinel-investigation-lab/
├── .github/
│   └── workflows/
│       └── tests.yml
├── data/
│   ├── synthetic_dlp_events.csv
│   └── dlp_alerts.csv
├── docs/
│   └── enterprise-dlp-concept-mapping.md
├── reports/
│   ├── investigation_log.csv
│   ├── incident_investigation_report.md
│   ├── incident_register.csv
│   ├── sla_results.csv
│   └── dlp_scenario_validation.csv
├── calculate_sla.py
├── detect_alerts.py
├── generate_events.py
├── investigate_alerts.py
├── requirements.txt
├── test_calculate_sla.py
├── test_detect_alerts.py
├── validate_scenarios.py
├── .gitignore
└── README.md
```

The `.venv/` directory is created locally during setup and excluded from Git.

## Getting Started

### Prerequisites

- Python 3.10 or a compatible version
- Git
- PowerShell, Command Prompt, or another terminal

### 1. Clone the repository

```bash
git clone https://github.com/namitharaveendran/dlp-sentinel-investigation-lab.git
cd dlp-sentinel-investigation-lab
```

### 2. Create and activate a virtual environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Generate synthetic events

```bash
python generate_events.py
```

This generates the fictional event dataset at `data/synthetic_dlp_events.csv`.

**Note:** Running the event generator again overwrites the existing synthetic dataset.

### 5. Run the detection engine

```bash
python detect_alerts.py
```

The detection engine processes the synthetic events and writes alert results to `data/dlp_alerts.csv`.

### 6. Generate investigation records

```bash
python investigate_alerts.py
```

This creates investigation records and the investigation report according to the implemented workflow.

### 7. Validate detection scenarios

```bash
python validate_scenarios.py
```

The validator checks eight scenarios, including sensitive-data transfers, external sharing, bulk-download thresholds, cloud uploads, and removable-media transfers.

Results are written to `reports/dlp_scenario_validation.csv`. A failed scenario causes the script to exit with a non-zero status.

### 8. Calculate incident review SLA results

```bash
python calculate_sla.py
```

The script reads `reports/incident_register.csv`, calculates elapsed review times, compares them with configured targets, and writes `reports/sla_results.csv`.

### 9. Run automated unit tests

```bash
python -m unittest -v test_detect_alerts.py test_calculate_sla.py
```

The current test suite contains 14 unit tests covering detection rules, threshold boundaries, approval validation, severity assignment, and SLA calculations.

## Validation Evidence

The latest local validation run produced the following results:

| Validation | Result |
|---|---|
| Detection and SLA unit tests | 14 passed |
| Executable DLP scenarios | 8 passed, 0 failed |
| Illustrative incident records analysed | 5 |
| SLA targets met | 3 |
| SLA targets breached | 2 |

These results come from the project's synthetic test data. They are not production detection rates, false-positive rates, or real-world SOC performance metrics.

### Observed Detection Results

The initial synthetic dataset run produced the following results:

| Metric | Observed result |
|---|---:|
| Source events analysed | 30 |
| Alert records generated | 30 |
| Unique events flagged | 21 |
| High-severity alert records | 18 |
| Medium-severity alert records | 12 |
| Unique events selected for initial investigation | 5 |

**Alert records by rule:**

| Rule ID | Alert records |
|---|---:|
| DLP-001 | 9 |
| DLP-002 | 6 |
| DLP-003 | 6 |
| DLP-004 | 6 |
| DLP-005 | 3 |

These are observed results from the initial synthetic dataset, not benchmarks of real-world detection performance. Alert records can exceed unique events because one event can trigger multiple rules.

Re-run the validation commands after modifying the detection logic, test cases, or scenario validator.

## Automated Testing and GitHub Actions

The workflow is defined in `.github/workflows/tests.yml`.

It runs on pushes and pull requests targeting `main`, and supports manual execution through GitHub Actions.

The workflow:

1. Checks out the repository.
2. Sets up Python 3.10.
3. Installs dependencies from `requirements.txt`.
4. Runs the DLP detection unit tests.
5. Runs the SLA calculation unit tests.
6. Executes DLP scenario validation.

View current workflow results on the [GitHub Actions page](https://github.com/namitharaveendran/dlp-sentinel-investigation-lab/actions).

## Incident Investigation and SLA Tracking

The incident register is stored at `reports/incident_register.csv`.

It contains five illustrative incident records with fields for:

- Incident and event identifiers
- Priority and status
- Creation and first-review timestamps
- Configured review-target duration
- Analyst action and escalation reason
- Disposition and evidence limitations

The sample records demonstrate how an analyst can document review and escalation decisions.

All example dispositions remain **Inconclusive** because the dataset does not independently establish authorization, actual data transfer, or data exposure.

A suspicious alert should not automatically be treated as a confirmed incident. A real investigation would require appropriate identity, access, approval, endpoint, cloud, or network evidence.

## Simulated SLA Monitoring

The SLA calculation module compares the elapsed time between incident creation and first review against an illustrative review-time target.

Run:

```bash
python calculate_sla.py
```

The output is saved to `reports/sla_results.csv`.

For the current illustrative sample:

| Metric | Result |
|---|---:|
| Incidents analysed | 5 |
| Review targets met | 3 |
| Review targets breached | 2 |

These are simulated results based on example timestamps and review targets. They do not represent actual operational performance, company SLAs, or compliance with an external standard.

## Enterprise DLP Concept Mapping

The [Enterprise DLP Concept Mapping](docs/enterprise-dlp-concept-mapping.md) document maps the lab's custom rules to general enterprise DLP concepts. It covers policy-design considerations, analyst validation, investigation principles, and project limitations.

For further study, see [Microsoft Learn — Learn about Data Loss Prevention](https://learn.microsoft.com/en-us/purview/dlp-learn-about-dlp).

Studying enterprise DLP concepts does not constitute hands-on administration of Microsoft Purview or another enterprise DLP platform.

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
- Explore authorized hands-on practice with enterprise DLP tooling.
- Improve reporting and visualization of alerts and review metrics.

## Skills Demonstrated

Python automation, pandas data processing, rule-based detection, DLP concepts, security alert triage, incident investigation documentation, SLA calculation, unit testing, scenario validation, Git, GitHub, and CI automation.

## Disclaimer

DLP Sentinel is an educational and defensive cybersecurity project. It uses fictional data and does not monitor real employees, access actual confidential information, or connect to production systems.

## Author

**Namitha Raveendran**

- [GitHub](https://github.com/namitharaveendran)
- [LinkedIn](https://www.linkedin.com/in/namitha-raveendran-0464692a4)
