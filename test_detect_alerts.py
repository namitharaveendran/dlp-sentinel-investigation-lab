
import unittest
import pandas as pd

from detect_alerts import detect_alerts


def make_event(
    activity,
    sensitivity="Internal",
    destination="corporate_device",
    destination_approved=True,
    files_count=1,
):
    """Build one synthetic event for a focused rule test."""
    return {
        "event_id": "TEST-001",
        "timestamp": "2026-10-12T09:00:00",
        "user_id": "TEST-USER",
        "file_name": "synthetic_test_file.csv",
        "activity": activity,
        "sensitivity": sensitivity,
        "destination": destination,
        "destination_approved": destination_approved,
        "files_count": files_count,
        "business_justification": "Synthetic test",
    }


class TestDLPDetectionRules(unittest.TestCase):

    def get_alerts(self, event):
        return detect_alerts(pd.DataFrame([event]))

    def test_rule_001_sensitive_unapproved_destination(self):
        event = make_event(
            activity="external_file_share",
            sensitivity="Confidential",
            destination="external_email",
            destination_approved=False,
        )
        alerts = self.get_alerts(event)

        matching = alerts[alerts["rule_id"] == "DLP-001"]
        self.assertEqual(len(matching), 1)
        self.assertEqual(matching.iloc[0]["severity"], "High")

    def test_rule_002_sensitive_external_sharing(self):
        event = make_event(
            activity="external_file_share",
            sensitivity="Restricted",
            destination="approved_partner",
            destination_approved=True,
        )
        alerts = self.get_alerts(event)

        matching = alerts[alerts["rule_id"] == "DLP-002"]
        self.assertEqual(len(matching), 1)
        self.assertEqual(matching.iloc[0]["severity"], "High")

    def test_rule_003_bulk_download_at_threshold(self):
        event = make_event(
            activity="bulk_download",
            files_count=100,
        )
        alerts = self.get_alerts(event)

        matching = alerts[alerts["rule_id"] == "DLP-003"]
        self.assertEqual(len(matching), 1)
        self.assertEqual(matching.iloc[0]["severity"], "Medium")

    def test_rule_003_does_not_trigger_below_threshold(self):
        event = make_event(
            activity="bulk_download",
            files_count=99,
        )
        alerts = self.get_alerts(event)

        self.assertNotIn("DLP-003", alerts["rule_id"].tolist())

    def test_rule_004_sensitive_cloud_upload(self):
        event = make_event(
            activity="cloud_upload",
            sensitivity="Confidential",
            destination="unapproved_cloud",
            destination_approved=False,
        )
        alerts = self.get_alerts(event)

        matching = alerts[alerts["rule_id"] == "DLP-004"]
        self.assertEqual(len(matching), 1)
        self.assertEqual(matching.iloc[0]["severity"], "High")

    def test_rule_004_internal_cloud_upload_medium(self):
        event = make_event(
            activity="cloud_upload",
            sensitivity="Internal",
            destination="unapproved_cloud",
            destination_approved=False,
        )
        alerts = self.get_alerts(event)

        matching = alerts[alerts["rule_id"] == "DLP-004"]
        self.assertEqual(len(matching), 1)
        self.assertEqual(matching.iloc[0]["severity"], "Medium")

    def test_rule_005_unapproved_usb_transfer(self):
        event = make_event(
            activity="removable_media_copy",
            destination="usb_drive",
            destination_approved=False,
        )
        alerts = self.get_alerts(event)

        matching = alerts[alerts["rule_id"] == "DLP-005"]
        self.assertEqual(len(matching), 1)
        self.assertEqual(matching.iloc[0]["severity"], "Medium")

    def test_approved_public_usb_transfer_does_not_trigger_rule_005(self):
        event = make_event(
            activity="removable_media_copy",
            sensitivity="Public",
            destination="usb_drive",
            destination_approved=True,
        )
        alerts = self.get_alerts(event)

        self.assertNotIn("DLP-005", alerts["rule_id"].tolist())

    def test_invalid_approval_value_is_rejected(self):
        event = make_event(
            activity="cloud_upload",
            destination="unapproved_cloud",
            destination_approved="unknown",
        )

        with self.assertRaises(ValueError):
            self.get_alerts(event)


if __name__ == "__main__":
    unittest.main(verbosity=2)
