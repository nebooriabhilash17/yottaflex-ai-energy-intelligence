
import pandas as pd
from pathlib import Path

input_file = Path("data/processed/batch_cost_analysis.csv")
output_file = Path("data/processed/machine_priority_report.csv")

df = pd.read_csv(input_file)

# Keep only batches flagged for investigation
flagged = df[df["Anomaly_Status"] == "INVESTIGATE"].copy()

# Summarize flagged batches by machine
report = flagged.groupby("Machine_ID").agg(
    Flagged_Batches=("Batch_ID", "count"),
    Energy_kWh=("Matched_Energy_kWh", "sum"),
    Estimated_Cost_Rs=("Estimated_Energy_Cost_Rs", "sum"),
    Average_Z_Score=("Intensity_Z_Score", "mean"),
).reset_index()

# Rank machines by estimated electricity cost
report = report.sort_values(
    "Estimated_Cost_Rs",
    ascending=False
).reset_index(drop=True)

report["Priority_Rank"] = range(1, len(report) + 1)

# Add investigation guidance
report["Recommended_Action"] = (
    "Inspect operating conditions, production mix, "
    "idle energy use, and meter accuracy."
)

# Save the report
report.to_csv(output_file, index=False)

print("YottaFlex AI - Machine Priority Report")
print("-" * 45)
print(report.head(10).round(2).to_string(index=False))
print(f"\nMachines ranked: {len(report)}")
print(f"Report saved to: {output_file.resolve()}")
