
import pandas as pd
from pathlib import Path

file_path = Path(
    "data/processed/energy_saving_recommendations.csv"
)

df = pd.read_csv(file_path)

print("YottaFlex AI - Recommendation Validation")
print("-" * 45)

checks = {
    "Report is not empty": len(df) > 0,
    "Machine IDs are unique": df["Machine_ID"].is_unique,
    "Energy intensity is non-negative": (
        df["Energy_Per_Unit_kWh"] >= 0
    ).all(),
    "Estimated energy savings are non-negative": (
        df["Estimated_Savings_kWh"] >= 0
    ).all(),
    "Estimated cost savings are non-negative": (
        df["Estimated_Savings_Rs"] >= 0
    ).all(),
    "Priority is HIGH": (
        df["Priority"] == "HIGH"
    ).all(),
    "Recommendations are present": (
        df["Recommendation"].notna()
        & df["Recommendation"].str.strip().ne("")
    ).all(),
}

for name, passed in checks.items():
    print(f"{'PASSED' if passed else 'FAILED'}: {name}")

print(f"\nTotal checks: {len(checks)}")
print(f"Passed: {sum(checks.values())}")
print(f"Failed: {len(checks) - sum(checks.values())}")
