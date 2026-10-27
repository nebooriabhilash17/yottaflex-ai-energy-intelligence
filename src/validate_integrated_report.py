
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"

report = pd.read_csv(
    DATA_DIR / "integrated_yottaflex_report.csv"
)
batches = pd.read_csv(
    DATA_DIR / "batch_anomaly_results.csv"
)
daily = pd.read_csv(
    DATA_DIR / "daily_anomaly_results.csv"
)
tariffs = pd.read_csv(
    DATA_DIR / "machine_tariff_costs.csv"
)

checks = []

# Original checks
checks.append((
    "Report contains 20 machines",
    len(report) == 20
))

checks.append((
    "Machine IDs are unique",
    report["Machine_ID"].is_unique
))

checks.append((
    "Priority ranks are unique",
    report["Priority_Rank"].is_unique
))

checks.append((
    "All flagged batches are counted",
    report["Flagged_Batch_Count"].sum()
    == (batches["Anomaly_Status"] == "INVESTIGATE").sum()
))

expected_daily_flags = (
    daily.loc[
        daily["Anomaly_Status"] == "UNUSUAL CONSUMPTION",
        "Date"
    ].nunique()
)

checks.append((
    "Unusual consumption days are recorded correctly",
    report["Daily_Anomaly_Days"].eq(expected_daily_flags).all()
))

checks.append((
    "Priority ranks are sorted",
    report["Priority_Rank"].is_monotonic_increasing
))

# New tariff-cost checks
checks.append((
    "Actual tariff-cost column exists",
    "Total_Electricity_Cost_Rs" in report.columns
))

checks.append((
    "All machines have tariff costs",
    report["Total_Electricity_Cost_Rs"].notna().all()
))

checks.append((
    "Tariff costs are non-negative",
    (report["Total_Electricity_Cost_Rs"] >= 0).all()
))

expected_cost = tariffs["Total_Electricity_Cost_Rs"].sum()
actual_cost = report["Total_Electricity_Cost_Rs"].sum()

checks.append((
    "Machine tariff costs reconcile within Rs 0.25",
    abs(actual_cost - expected_cost) < 0.25
))

checks.append((
    "Tariff cost ranks are present for all machines",
    report["Cost_Rank"].notna().all()
))

print("YottaFlex AI - Integrated Report Validation")
print("-" * 50)

for name, passed in checks:
    print(f"{'PASSED' if passed else 'FAILED'}: {name}")

passed_count = sum(passed for _, passed in checks)

print(f"\nTotal checks: {len(checks)}")
print(f"Passed: {passed_count}")
print(f"Failed: {len(checks) - passed_count}")

print(f"\nIntegrated report tariff cost: Rs {actual_cost:,.2f}")
print(f"Source tariff cost: Rs {expected_cost:,.2f}")
print(f"Difference: Rs {abs(actual_cost - expected_cost):,.2f}")
