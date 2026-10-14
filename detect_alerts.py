
from pathlib import Path
import pandas as pd

INPUT_FILE = Path("data") / "synthetic_dlp_events.csv"
OUTPUT_FILE = Path("data") / "dlp_alerts.csv"

if not INPUT_FILE.exists():
    raise FileNotFoundError(
        f"Dataset not found: {INPUT_FILE}. "
        "Run generate_events.py first."
    )

df = pd.read_csv(INPUT_FILE)

# Ensure approval values are interpreted as Boolean values.
df["destination_approved"] = (
    df["destination_approved"]
    .astype(str)
    .str.strip()
    .str.lower()
    .map({"true": True, "false": False})
)

if df["destination_approved"].isna().any():
    raise ValueError("Invalid destination_approved values found.")

# Each event may trigger more than one rule.
alerts = []

def add_alert(row, rule_id, reason, severity):
    alerts.append({
        "event_id": row["event_id"],
        "timestamp": row["timestamp"],
        "user_id": row["user_id"],
        "file_name": row["file_name"],
        "activity": row["activity"],
        "sensitivity": row["sensitivity"],
        "destination": row["destination"],
        "rule_id": rule_id,
        "alert_reason": reason,
        "severity": severity,
        "investigation_status": "Needs review",
        "disposition": "Unclassified",
    })

for _, row in df.iterrows():
    activity = row["activity"]
    sensitivity = row["sensitivity"]
    destination = row["destination"]
    approved = row["destination_approved"]
    file_count = int(row["files_count"])

    # Rule 1: Sensitive data sent to an unapproved destination.
    if (
        sensitivity in ["Confidential", "Restricted"]
        and not approved
    ):
        add_alert(
            row,
            "DLP-001",
            "Sensitive data involved an unapproved destination.",
            "High",
        )

    # Rule 2: External sharing involving sensitive information.
    if (
        activity == "external_file_share"
        and sensitivity in ["Confidential", "Restricted"]
    ):
        add_alert(
            row,
            "DLP-002",
            "Sensitive file shared externally; validate authorization.",
            "High",
        )

    # Rule 3: Bulk downloads above the lab threshold.
    if activity == "bulk_download" and file_count >= 100:
        add_alert(
            row,
            "DLP-003",
            f"Bulk download involved {file_count} files; review context.",
            "Medium",
        )

    # Rule 4: Upload to an unapproved cloud destination.
    if (
        activity == "cloud_upload"
        and destination == "unapproved_cloud"
    ):
        add_alert(
            row,
            "DLP-004",
            "Cloud upload targeted an unapproved destination.",
            "High" if sensitivity in ["Confidential", "Restricted"]
            else "Medium",
        )

    # Rule 5: Copy to removable media without approval.
    if (
        activity == "removable_media_copy"
        and destination == "usb_drive"
        and not approved
    ):
        add_alert(
            row,
            "DLP-005",
            "Removable-media copy lacks destination approval.",
            "Medium",
        )

columns = [
    "event_id", "timestamp", "user_id", "file_name",
    "activity", "sensitivity", "destination", "rule_id",
    "alert_reason", "severity", "investigation_status",
    "disposition",
]

alerts_df = pd.DataFrame(alerts, columns=columns)
alerts_df.to_csv(OUTPUT_FILE, index=False)

print(f"Events analysed: {len(df)}")
print(f"Alert records generated: {len(alerts_df)}")
print(f"Unique events flagged: {alerts_df['event_id'].nunique()}")
print(f"Output saved: {OUTPUT_FILE}")

if not alerts_df.empty:
    print("\nAlerts by severity:")
    print(alerts_df["severity"].value_counts().to_string())

    print("\nAlerts by rule:")
    print(alerts_df["rule_id"].value_counts().to_string())

    print("\nAlert preview:")
    print(alerts_df[
        ["event_id", "rule_id", "alert_reason", "severity"]
    ].head(10).to_string(index=False))
else:
    print("No alerts generated. Review the detection rules and dataset.")
