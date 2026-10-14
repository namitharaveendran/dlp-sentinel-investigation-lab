
from pathlib import Path

import pandas as pd

REGISTER_PATH = Path("reports/incident_register.csv")
OUTPUT_PATH = Path("reports/sla_results.csv")


def calculate_sla(df: pd.DataFrame) -> pd.DataFrame:
    required = {
        "incident_id",
        "created_at",
        "first_review_at",
        "sla_target_minutes",
    }

    missing = required - set(df.columns)
    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}"
        )

    result = df.copy()

    created = pd.to_datetime(
        result["created_at"], errors="raise"
    )
    reviewed = pd.to_datetime(
        result["first_review_at"], errors="raise"
    )
    target = pd.to_numeric(
        result["sla_target_minutes"], errors="raise"
    )

    if target.isna().any() or (target <= 0).any():
        raise ValueError("SLA targets must be positive numbers.")

    elapsed = (reviewed - created).dt.total_seconds() / 60

    if elapsed.isna().any() or (elapsed < 0).any():
        raise ValueError(
            "Review timestamps must be present and not precede creation."
        )

    result["review_elapsed_minutes"] = elapsed.round(2)
    result["sla_result"] = [
        "Met" if actual <= limit else "Breached"
        for actual, limit in zip(elapsed, target)
    ]

    return result


def main():
    df = pd.read_csv(REGISTER_PATH)
    results = calculate_sla(df)

    results.to_csv(OUTPUT_PATH, index=False)

    print("SLA review results")
    print("==================")
    print(
        results[
            [
                "incident_id",
                "priority",
                "review_elapsed_minutes",
                "sla_target_minutes",
                "sla_result",
            ]
        ].to_string(index=False)
    )

    print(f"\nResults saved to: {OUTPUT_PATH}")
    print(f"Incidents analysed: {len(results)}")
    print(
        "SLA targets met: "
        f"{(results['sla_result'] == 'Met').sum()}"
    )
    print(
        "SLA targets breached: "
        f"{(results['sla_result'] == 'Breached').sum()}"
    )


if __name__ == "__main__":
    main()
