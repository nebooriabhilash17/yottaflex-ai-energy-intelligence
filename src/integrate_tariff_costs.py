
import pandas as pd
from pathlib import Path

# Project folders
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"

# Load reports
priority = pd.read_csv(DATA_DIR / "machine_priority_report.csv")
tariff_costs = pd.read_csv(DATA_DIR / "machine_tariff_costs.csv")

# Keep only the required tariff-cost columns
tariff_columns = [
    "Machine_ID",
    "Total_Energy_kWh",
    "Total_Electricity_Cost_Rs",
    "Cost_Rank",
]

tariff_costs = tariff_costs[tariff_columns]

# Combine reports by machine
integrated = priority.merge(
    tariff_costs,
    on="Machine_ID",
    how="left",
    validate="one_to_one",
)

# Check for missing tariff costs
if integrated["Total_Electricity_Cost_Rs"].isna().any():
    raise ValueError("Some machines have no tariff-based cost.")

# Rename existing flat-rate cost for clarity
integrated = integrated.rename(
    columns={
        "Estimated_Cost_Rs": "Flagged_Batch_Cost_Flat_Rate_Rs"
    }
)

# Sort by investigation priority
integrated = integrated.sort_values(
    "Priority_Rank"
).reset_index(drop=True)

# Save integrated output
output_file = DATA_DIR / "machine_priority_with_tariffs.csv"
integrated.to_csv(output_file, index=False)

print("YottaFlex AI - Priority and Tariff Cost Integration")
print("-" * 55)
print(f"Machines included: {integrated['Machine_ID'].nunique()}")

print("\nTop 5 machines by investigation priority:")
print(
    integrated[
        [
            "Priority_Rank",
            "Machine_ID",
            "Flagged_Batches",
            "Flagged_Batch_Cost_Flat_Rate_Rs",
            "Total_Electricity_Cost_Rs",
            "Cost_Rank",
        ]
    ].head(5).to_string(index=False)
)

print(f"\nReport saved to: {output_file}")
print(
    "\nNote: Total machine electricity cost is not the same "
    "as avoidable waste cost."
)
