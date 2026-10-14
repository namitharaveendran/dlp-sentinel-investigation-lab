
from pathlib import Path
import pandas as pd

# DLP Sentinel: synthetic security events for investigation practice.
# All records are fictional.
OUTPUT_FILE = Path("data") / "synthetic_dlp_events.csv"
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

scenarios = [
    {
        "activity": "external_file_share",
        "file_name": "customer_records.xlsx",
        "sensitivity": "Confidential",
        "destination": "external_email",
        "destination_approved": False,
        "files_count": 1,
        "business_justification": "Not provided",
    },
    {
        "activity": "bulk_download",
        "file_name": "employee_data.csv",
        "sensitivity": "Restricted",
        "destination": "corporate_device",
        "destination_approved": True,
        "files_count": 250,
        "business_justification": "Routine reporting claimed",
    },
    {
        "activity": "cloud_upload",
        "file_name": "financial_forecast.xlsx",
        "sensitivity": "Confidential",
        "destination": "unapproved_cloud",
        "destination_approved": False,
        "files_count": 12,
        "business_justification": "Not provided",
    },
    {
        "activity": "removable_media_copy",
        "file_name": "project_documents.zip",
        "sensitivity": "Internal",
        "destination": "usb_drive",
        "destination_approved": False,
        "files_count": 8,
        "business_justification": "Not provided",
    },
    {
        "activity": "external_file_share",
        "file_name": "public_brochure.pdf",
        "sensitivity": "Public",
        "destination": "approved_partner",
        "destination_approved": True,
        "files_count": 1,
        "business_justification": "Approved marketing activity",
    },
    {
        "activity": "cloud_upload",
        "file_name": "team_notes.docx",
        "sensitivity": "Internal",
        "destination": "approved_cloud",
        "destination_approved": True,
        "files_count": 2,
        "business_justification": "Approved team collaboration",
    },
    {
        "activity": "bulk_download",
        "file_name": "transaction_history.csv",
        "sensitivity": "Restricted",
        "destination": "corporate_device",
        "destination_approved": True,
        "files_count": 180,
        "business_justification": "Not provided",
    },
    {
        "activity": "removable_media_copy",
        "file_name": "training_material.pdf",
        "sensitivity": "Public",
        "destination": "usb_drive",
        "destination_approved": True,
        "files_count": 3,
        "business_justification": "Approved training transfer",
    },
    {
        "activity": "external_file_share",
        "file_name": "payroll_summary.xlsx",
        "sensitivity": "Restricted",
        "destination": "external_email",
        "destination_approved": False,
        "files_count": 1,
        "business_justification": "Urgent request; not verified",
    },
    {
        "activity": "cloud_upload",
        "file_name": "internal_project_plan.docx",
        "sensitivity": "Internal",
        "destination": "unapproved_cloud",
        "destination_approved": False,
        "files_count": 5,
        "business_justification": "Personal backup",
    },
]

events = []

for i in range(30):
    scenario = scenarios[i % len(scenarios)].copy()

    events.append({
        "event_id": f"DLP-{i + 1:03d}",
        "timestamp": (
            pd.Timestamp("2026-10-12 09:00:00")
            + pd.Timedelta(minutes=15 * i)
        ).isoformat(),
        "user_id": f"EMP-{101 + (i % 7)}",
        **scenario,
    })

df = pd.DataFrame(events)
df.to_csv(OUTPUT_FILE, index=False)

print(f"Dataset created: {OUTPUT_FILE}")
print(f"Total events: {len(df)}")

print("\nActivity distribution:")
print(df["activity"].value_counts().to_string())

print("\nSensitivity distribution:")
print(df["sensitivity"].value_counts().to_string())

print("\nFirst five events:")
print(df.head().to_string(index=False))
