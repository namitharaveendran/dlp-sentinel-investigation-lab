
from pathlib import Path

import pandas as pd

from detect_alerts import detect_alerts

INPUT_FILE = Path("data") / "synthetic_dlp_events.csv"
OUTPUT_FILE = Path("reports") / "dlp_scenario_validation.csv"

SCENARIOS = [
    {
        "scenario_id": "SC-001",
        "test_case": "Sensitive data to unapproved destination",
        "event": {
            "event_id": "TEST-001",
            "activity": "cloud_upload",
            "sensitivity": "Confidential",
            "destination": "unapproved_cloud",
            "destination_approved": False,
            "files_count": 1,
        },
        "expected_rule": "DLP-001",
        "expected_severity": "High",
    },
    {
        "scenario_id": "SC-002",
        "test_case": "Sensitive external file sharing",
        "event": {
            "event_id": "TEST-002",
            "activity": "external_file_share",
            "sensitivity": "Confidential",
            "destination": "external_email",
            "destination_approved": True,
            "files_count": 1,
        },
        "expected_rule": "DLP-002",
        "expected_severity": "High",
    },
    {
        "scenario_id": "SC-003",
        "test_case": "Bulk download of 100 files",
        "event": {
            "event_id": "TEST-003",
            "activity": "bulk_download",
            "sensitivity": "Internal",
            "destination": "corporate_device",
            "destination_approved": True,
            "files_count": 100,
        },
        "expected_rule": "DLP-003",
        "expected_severity": "Medium",
    },
    {
        "scenario_id": "SC-004",
        "test_case": "Bulk download of 99 files",
        "event": {
            "event_id": "TEST-004",
            "activity": "bulk_download",
            "sensitivity": "Internal",
            "destination": "corporate_device",
            "destination_approved": True,
            "files_count": 99,
        },
        "expected_rule": None,
        "expected_severity": None,
    },
    {
        "scenario_id": "SC-005",
        "test_case": "Sensitive upload to unapproved cloud",
        "event": {
            "event_id": "TEST-005",
            "activity": "cloud_upload",
            "sensitivity": "Restricted",
            "destination": "unapproved_cloud",
            "destination_approved": False,
            "files_count": 1,
        },
        "expected_rule": "DLP-004",
        "expected_severity": "High",
    },
    {
        "scenario_id": "SC-006",
        "test_case": "Internal upload to unapproved cloud",
        "event": {
            "event_id": "TEST-006",
            "activity": "cloud_upload",
            "sensitivity": "Internal",
            "destination": "unapproved_cloud",
            "destination_approved": False,
            "files_count": 1,
        },
        "expected_rule": "DLP-004",
        "expected_severity": "Medium",
    },
    {
        "scenario_id": "SC-007",
        "test_case": "Unapproved USB transfer",
        "event": {
            "event_id": "TEST-007",
            "activity": "removable_media_copy",
            "sensitivity": "Internal",
            "destination": "usb_drive",
            "destination_approved": False,
            "files_count": 1,
        },
        "expected_rule": "DLP-005",
        "expected_severity": "Medium",
    },
    {
        "scenario_id": "SC-008",
        "test_case": "Approved public USB transfer",
        "event": {
            "event_id": "TEST-008",
            "activity": "removable_media_copy",
            "sensitivity": "Public",
            "destination": "usb_drive",
            "destination_approved": True,
            "files_count": 1,
        },
        "expected_rule": None,
        "expected_severity": None,
    },
]


def build_event(event):
    """Add the common fields required by detect_alerts()."""
    return {
        "timestamp": "2026-10-14T10:00:00",
        "user_id": "TEST-USER",
        "file_name": "synthetic_test_file.txt",
        **event,
    }


def validate_scenarios():
    results = []

    for scenario in SCENARIOS:
        event = build_event(scenario["event"])
        alerts = detect_alerts(pd.DataFrame([event]))

        if scenario["expected_rule"] is None:
            passed = alerts.empty
            actual_rules = (
                "None" if alerts.empty
                else ";".join(sorted(alerts["rule_id"].unique()))
            )
            actual_severities = (
                "None" if alerts.empty
                else ";".join(sorted(alerts["severity"].unique()))
            )
        else:
            matching = alerts[
                alerts["rule_id"] == scenario["expected_rule"]
            ]
            passed = (
                len(matching) == 1
                and matching.iloc[0]["severity"]
                == scenario["expected_severity"]
            )
            actual_rules = (
                ";".join(sorted(alerts["rule_id"].unique()))
                if not alerts.empty else "None"
            )
            actual_severities = (
                ";".join(sorted(alerts["severity"].unique()))
                if not alerts.empty else "None"
            )

        results.append({
            "scenario_id": scenario["scenario_id"],
            "test_case": scenario["test_case"],
            "expected_rule": scenario["expected_rule"] or "None",
            "actual_rules": actual_rules,
            "expected_severity": (
                scenario["expected_severity"] or "None"
            ),
            "actual_severities": actual_severities,
            "pass_fail": "PASS" if passed else "FAIL",
        })

    return pd.DataFrame(results)


def main():
    results = validate_scenarios()
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    results.to_csv(OUTPUT_FILE, index=False)

    print("DLP Scenario Validation")
    print("=======================")
    print(results.to_string(index=False))

    passed = (results["pass_fail"] == "PASS").sum()
    failed = (results["pass_fail"] == "FAIL").sum()

    print(f"\nScenarios passed: {passed}")
    print(f"Scenarios failed: {failed}")
    print(f"Results saved to: {OUTPUT_FILE}")

    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
