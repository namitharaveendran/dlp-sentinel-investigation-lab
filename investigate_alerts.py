
from pathlib import Path
import pandas as pd

# --------------------------------------------------
# DLP SENTINEL - INVESTIGATION AND TRIAGE
# Synthetic data only. Not a production DLP system.
# --------------------------------------------------

ALERTS_FILE = Path("data") / "dlp_alerts.csv"
EVENTS_FILE = Path("data") / "synthetic_dlp_events.csv"
OUTPUT_FILE = Path("reports") / "investigation_log.csv"

# --------------------------------------------------
# 1. Validate input files
# --------------------------------------------------

if not ALERTS_FILE.exists():
    raise FileNotFoundError(
        f"Alert file not found: {ALERTS_FILE}\n"
        "Run: python detect_alerts.py"
    )

if not EVENTS_FILE.exists():
    raise FileNotFoundError(
        f"Event dataset not found: {EVENTS_FILE}\n"
        "Run: python generate_events.py"
    )

alerts = pd.read_csv(ALERTS_FILE)
events = pd.read_csv(EVENTS_FILE)

if alerts.empty:
    print("No alerts available for investigation.")
    raise SystemExit(0)

# --------------------------------------------------
# 2. Select five unique events for review
# --------------------------------------------------

selected_ids = alerts["event_id"].drop_duplicates().head(5)

sample = events[
    events["event_id"].isin(selected_ids)
].copy()

if sample.empty:
    print("No matching events found in the source dataset.")
    raise SystemExit(1)

# --------------------------------------------------
# 3. Initial risk assessment
# These are triage recommendations, not verdicts.
# --------------------------------------------------

def assess_event(row):
    activity = str(row["activity"])
    sensitivity = str(row["sensitivity"])
    destination = str(row["destination"])
    approved = str(row["destination_approved"]).lower() == "true"
    count = int(row["files_count"])
    justification = str(
        row["business_justification"]
    ).strip()

    sensitive_data = sensitivity in [
        "Confidential",
        "Restricted",
    ]

    no_justification = justification.lower() in [
        "",
        "not provided",
        "nan",
        "none",
    ]

    # Rule 1: Sensitive data and unapproved destination.
    if sensitive_data and not approved:
        return pd.Series({
            "initial_priority": "High",
            "recommended_action": "Escalate for review",
            "assessment_rationale": (
                f"{sensitivity} data involved destination "
                f"'{destination}', which is marked unapproved. "
                "Validate authorization and transfer details."
            ),
        })

    # Rule 2: Large download of sensitive information.
    if activity == "bulk_download" and count >= 100:
        if no_justification:
            return pd.Series({
                "initial_priority": "High",
                "recommended_action": (
                    "Validate business purpose and authorization"
                ),
                "assessment_rationale": (
                    f"{count} files downloaded; no business "
                    "justification is stated. Verify whether "
                    "the activity was expected and authorized."
                ),
            })

        return pd.Series({
            "initial_priority": "Medium",
            "recommended_action": (
                "Validate business purpose and authorization"
            ),
            "assessment_rationale": (
                f"{count} files downloaded. A business purpose "
                "is stated but has not been independently verified."
            ),
        })

    # Rule 3: Unapproved removable-media activity.
    if (
        activity == "removable_media_copy"
        and destination == "usb_drive"
        and not approved
    ):
        return pd.Series({
            "initial_priority": "Medium",
            "recommended_action": (
                "Review removable-media activity"
            ),
            "assessment_rationale": (
                "The USB destination is marked unapproved. "
                "Validate applicable policy, authorization, "
                "and business context."
            ),
        })

    # Rule 4: Unapproved cloud upload.
    if (
        activity == "cloud_upload"
        and destination == "unapproved_cloud"
    ):
        return pd.Series({
            "initial_priority": "High" if sensitive_data else "Medium",
            "recommended_action": (
                "Validate cloud destination and file transfer"
            ),
            "assessment_rationale": (
                "Upload targeted an unapproved cloud destination. "
                "Validate file sensitivity, transfer details, "
                "and authorization."
            ),
        })

    # Default: context still requires review.
    return pd.Series({
        "initial_priority": "Low",
        "recommended_action": "Review event context",
        "assessment_rationale": (
            "No high-priority condition matched these rules. "
            "Review the applicable policy and event context."
        ),
    })


assessments = sample.apply(
    assess_event,
    axis=1,
)

sample = pd.concat(
    [sample.reset_index(drop=True),
     assessments.reset_index(drop=True)],
    axis=1,
)

# --------------------------------------------------
# 4. Add investigation fields
# --------------------------------------------------

sample["evidence_reviewed"] = (
    "Synthetic event fields only; no independent validation"
)

sample["disposition"] = "Inconclusive"

sample["analyst_notes"] = (
    "Initial triage only. Further validation required."
)

sample["reviewed_by"] = "Student Analyst - DLP Sentinel Lab"

# --------------------------------------------------
# 5. Save investigation log
# --------------------------------------------------

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True,
)

sample.to_csv(
    OUTPUT_FILE,
    index=False,
)

# --------------------------------------------------
# 6. Display investigation results
# --------------------------------------------------

print("=" * 65)
print("DLP SENTINEL - INITIAL INVESTIGATION RESULTS")
print("=" * 65)

print(f"Total source events: {len(events)}")
print(f"Alert records available: {len(alerts)}")
print(f"Unique events selected: {len(sample)}")
print(f"Investigation log: {OUTPUT_FILE}")

print("\nInitial priority distribution:")
print(
    sample["initial_priority"]
    .value_counts()
    .to_string()
)

print("\nSelected events:")
print(
    sample[
        [
            "event_id",
            "activity",
            "sensitivity",
            "destination",
            "destination_approved",
            "files_count",
            "initial_priority",
            "disposition",
        ]
    ].to_string(index=False)
)

print("\nInvestigation recommendations:")
for _, row in sample.iterrows():
    print(f"\nEvent: {row['event_id']}")
    print(f"Priority: {row['initial_priority']}")
    print(f"Reason: {row['assessment_rationale']}")
    print(f"Action: {row['recommended_action']}")

print("\n" + "=" * 65)
print("Investigation log saved successfully.")
print("All dispositions remain Inconclusive pending review.")
print("=" * 65)
