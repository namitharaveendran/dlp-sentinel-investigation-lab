
import unittest

import pandas as pd

from calculate_sla import calculate_sla


class TestSLACalculation(unittest.TestCase):

    def make_df(self, created, reviewed, target=15):
        return pd.DataFrame({
            "incident_id": ["INC-TEST"],
            "created_at": [created],
            "first_review_at": [reviewed],
            "sla_target_minutes": [target],
        })

    def test_sla_met(self):
        df = self.make_df(
            "2026-10-14 09:00:00",
            "2026-10-14 09:10:00",
        )
        result = calculate_sla(df)
        self.assertEqual(result.loc[0, "sla_result"], "Met")
        self.assertEqual(
            result.loc[0, "review_elapsed_minutes"], 10
        )

    def test_sla_breached(self):
        df = self.make_df(
            "2026-10-14 09:00:00",
            "2026-10-14 09:20:00",
        )
        result = calculate_sla(df)
        self.assertEqual(result.loc[0, "sla_result"], "Breached")

    def test_exact_sla_boundary_is_met(self):
        df = self.make_df(
            "2026-10-14 09:00:00",
            "2026-10-14 09:15:00",
        )
        result = calculate_sla(df)
        self.assertEqual(result.loc[0, "sla_result"], "Met")

    def test_review_before_creation_is_rejected(self):
        df = self.make_df(
            "2026-10-14 09:15:00",
            "2026-10-14 09:00:00",
        )
        with self.assertRaises(ValueError):
            calculate_sla(df)

    def test_zero_sla_target_is_rejected(self):
        df = self.make_df(
            "2026-10-14 09:00:00",
            "2026-10-14 09:05:00",
            target=0,
        )
        with self.assertRaises(ValueError):
            calculate_sla(df)


if __name__ == "__main__":
    unittest.main()
