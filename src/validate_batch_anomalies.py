
import pandas as pd
from pathlib import Path

file_path = Path("data/processed/batch_anomaly_results.csv")
df = pd.read_csv(file_path)

checks = {
    "Report is not empty": len(df) > 0,
    "Batch IDs are unique": df["Batch_ID"].is_unique,
    "Machine IDs are present": df["Machine_ID"].notna().all(),
    "Production quantities are positive": (
        df["Production_Quantity"] > 0
    ).all(),
    "Energy intensity is non-negative": (
        df["Energy_Intensity_kWh_per_Unit"] >= 0
    ).all(),
    "Machine baselines are positive": (
        df["Machine_Average_Intensity"] > 0
    ).all(),
    "Anomaly labels are valid": (
        df["Anomaly_Status"].isin(["NORMAL", "INVESTIGATE"])
    ).all(),
    "Flagged batches exceed the threshold": (
        df.loc[
            df["Anomaly_Status"] == "INVESTIGATE",
            "Intensity_Z_Score"
        ] > 2
    ).all(),
}

print("YottaFlex AI - Batch Anomaly Validation")
print("-" * 45)

for name, passed in checks.items():
    print(f"{'PASSED' if passed else 'FAILED'}: {name}")

print(f"\nTotal checks: {len(checks)}")
print(f"Passed: {sum(checks.values())}")
print(f"Failed: {len(checks) - sum(checks.values())}")
