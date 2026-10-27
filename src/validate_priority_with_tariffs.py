
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"

report = pd.read_csv(
    DATA_DIR / "machine_priority_with_tariffs.csv"
)

priority = pd.read_csv(
    DATA_DIR / "machine_priority_report.csv"
)

tariffs = pd.read_csv(
    DATA_DIR / "machine_tariff_costs.csv"
)

checks = []

checks.append((
    "All 20 machines are included",
    report["Machine_ID"].nunique() == 20
))

checks.append((
    "Machine IDs are unique",
    report["Machine_ID"].is_unique
))

checks.append((
    "Priority ranks are preserved",
    report["Priority_Rank"].tolist()
    == priority.sort_values("Priority_Rank")["Priority_Rank"].tolist()
))

checks.append((
    "All tariff costs are present",
    report["Total_Electricity_Cost_Rs"].notna().all()
))

checks.append((
    "Tariff costs match the source report",
    report["Total_Electricity_Cost_Rs"].sum()
    - tariffs["Total_Electricity_Cost_Rs"].sum()
    < 0.02
))

checks.append((
    "Flagged-batch costs are non-negative",
    (report["Flagged_Batch_Cost_Flat_Rate_Rs"] >= 0).all()
))

print("YottaFlex AI - Integrated Tariff Validation")
print("-" * 48)

for name, passed in checks:
    print(f"{'PASSED' if passed else 'FAILED'}: {name}")

print(f"\nTotal checks: {len(checks)}")
print(f"Passed: {sum(p for _, p in checks)}")
print(f"Failed: {sum(not p for _, p in checks)}")
