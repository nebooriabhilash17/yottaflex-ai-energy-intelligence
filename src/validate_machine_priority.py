
import pandas as pd
from pathlib import Path

file_path = Path("data/processed/machine_priority_report.csv")
df = pd.read_csv(file_path)

checks = {
    "Report has 20 machines": len(df) == 20,
    "Machine IDs are unique": df["Machine_ID"].is_unique,
    "Priority ranks are unique": df["Priority_Rank"].is_unique,
    "Priority ranks are sequential": (
        sorted(df["Priority_Rank"].tolist())
        == list(range(1, len(df) + 1))
    ),
    "Estimated costs are non-negative": (
        df["Estimated_Cost_Rs"] >= 0
    ).all(),
    "Flagged batch counts are positive": (
        df["Flagged_Batches"] > 0
    ).all(),
    "Report is sorted by descending cost": (
        df["Estimated_Cost_Rs"].is_monotonic_decreasing
    ),
    "Recommended actions are present": (
        df["Recommended_Action"].notna()
        & df["Recommended_Action"].str.strip().ne("")
    ).all(),
}

print("YottaFlex AI - Machine Priority Validation")
print("-" * 48)

for name, passed in checks.items():
    print(f"{'PASSED' if passed else 'FAILED'}: {name}")

print(f"\nTotal checks: {len(checks)}")
print(f"Passed: {sum(checks.values())}")
print(f"Failed: {len(checks) - sum(checks.values())}")
