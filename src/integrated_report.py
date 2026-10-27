
import pandas as pd
from pathlib import Path

# --------------------------------------------------
# 1. Set project folders
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"

# --------------------------------------------------
# 2. Load analysis files
# --------------------------------------------------
priority = pd.read_csv(
    PROCESSED_DIR / "machine_priority_report.csv"
)

efficiency = pd.read_csv(
    PROCESSED_DIR / "machine_efficiency.csv"
)

batch_anomalies = pd.read_csv(
    PROCESSED_DIR / "batch_anomaly_results.csv"
)

daily_anomalies = pd.read_csv(
    PROCESSED_DIR / "daily_anomaly_results.csv"
)

tariff_costs = pd.read_csv(
    PROCESSED_DIR / "machine_tariff_costs.csv"
)

# --------------------------------------------------
# 3. Select machine efficiency columns
# --------------------------------------------------
efficiency_columns = [
    "Machine_ID",
    "Total_Energy_kWh",
    "Total_Units",
    "Energy_Per_Unit_kWh",
    "Efficiency_Status",
    "Potential_Savings_kWh",
    "Potential_Savings_Rs",
]

efficiency = efficiency[efficiency_columns]

# Rename overlapping energy column before merging
efficiency = efficiency.rename(
    columns={
        "Total_Energy_kWh": "Efficiency_Total_Energy_kWh"
    }
)

# --------------------------------------------------
# 4. Prepare actual tariff cost columns
# --------------------------------------------------
tariff_columns = [
    "Machine_ID",
    "Total_Energy_kWh",
    "Total_Electricity_Cost_Rs",
    "Cost_Rank",
]

tariff_costs = tariff_costs[tariff_columns]

tariff_costs = tariff_costs.rename(
    columns={
        "Total_Energy_kWh": "Tariff_Total_Energy_kWh"
    }
)

if tariff_costs["Machine_ID"].duplicated().any():
    raise ValueError("Duplicate machine IDs in tariff cost report.")

# --------------------------------------------------
# 5. Combine priority, efficiency and tariff costs
# --------------------------------------------------
report = priority.merge(
    efficiency,
    on="Machine_ID",
    how="left",
    validate="one_to_one",
)

report = report.merge(
    tariff_costs,
    on="Machine_ID",
    how="left",
    validate="one_to_one",
)

if report["Total_Electricity_Cost_Rs"].isna().any():
    raise ValueError("Missing actual tariff costs for some machines.")

# --------------------------------------------------
# 6. Count batches requiring investigation
# --------------------------------------------------
batch_status = (
    batch_anomalies["Anomaly_Status"]
    .fillna("")
    .astype(str)
    .str.strip()
    .str.upper()
)

flagged_batches = batch_anomalies[
    batch_status == "INVESTIGATE"
]

flagged_counts = (
    flagged_batches.groupby("Machine_ID")
    .size()
    .reset_index(name="Flagged_Batch_Count")
)

report = report.merge(
    flagged_counts,
    on="Machine_ID",
    how="left",
    validate="one_to_one",
)

report["Flagged_Batch_Count"] = (
    report["Flagged_Batch_Count"]
    .fillna(0)
    .astype(int)
)

# --------------------------------------------------
# 7. Count unusual daily energy consumption days
# --------------------------------------------------
daily_status = (
    daily_anomalies["Anomaly_Status"]
    .fillna("")
    .astype(str)
    .str.strip()
    .str.upper()
)

daily_flags = daily_anomalies[
    daily_status == "UNUSUAL CONSUMPTION"
]

daily_anomaly_days = int(
    daily_flags["Date"].nunique()
)

report["Daily_Anomaly_Days"] = daily_anomaly_days

# --------------------------------------------------
# 8. Add cost assumptions and labels
# --------------------------------------------------
report["Cost_Assumption_Rs_per_kWh"] = 7.0

report["Actual_Tariff_Cost_Source"] = (
    "Time-based synthetic tariff schedule"
)

# --------------------------------------------------
# 9. Sort by investigation priority
# --------------------------------------------------
report = report.sort_values(
    "Priority_Rank"
).reset_index(drop=True)

# --------------------------------------------------
# 10. Save integrated report
# --------------------------------------------------
output_file = (
    PROCESSED_DIR / "integrated_yottaflex_report.csv"
)

report.to_csv(output_file, index=False)

# --------------------------------------------------
# 11. Display results
# --------------------------------------------------
print("YottaFlex AI - Integrated Report")
print("-" * 50)

print(f"Machines included: {report['Machine_ID'].nunique()}")
print(f"Flagged batches: {len(flagged_batches)}")
print(f"Daily anomaly days detected: {daily_anomaly_days}")

print(
    "Total tariff-based electricity cost: Rs "
    f"{report['Total_Electricity_Cost_Rs'].sum():,.2f}"
)

print("\nDaily anomaly status counts:")
print(daily_status.value_counts().to_string())

print("\nTop 5 machines requiring investigation:")

display_columns = [
    "Priority_Rank",
    "Machine_ID",
    "Efficiency_Status",
    "Flagged_Batch_Count",
    "Estimated_Cost_Rs",
    "Total_Electricity_Cost_Rs",
    "Cost_Rank",
    "Recommended_Action",
]

print(
    report[display_columns]
    .head(5)
    .to_string(index=False)
)

print(f"\nReport saved to: {output_file}")

print("\nImportant notes:")
print("- Total electricity costs use the time-based tariff schedule.")
print("- Estimated_Cost_Rs retains the existing flagged-batch estimate.")
print("- The Rs 7/kWh assumption is retained for existing estimates.")
print("- Flagged energy cost is not confirmed avoidable waste.")
print("- Daily and batch anomalies require investigation.")
print("- The dataset and tariff schedule are synthetic.")
