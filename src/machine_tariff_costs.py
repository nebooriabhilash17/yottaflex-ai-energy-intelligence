
import pandas as pd
from pathlib import Path

# --------------------------------------------------
# 1. Set project folders
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

# --------------------------------------------------
# 2. Load datasets
# --------------------------------------------------
energy = pd.read_csv(RAW_DIR / "energy_readings.csv")
meters = pd.read_csv(RAW_DIR / "meters.csv")
tariffs = pd.read_csv(RAW_DIR / "tariffs.csv")

# --------------------------------------------------
# 3. Convert energy timestamps to India local time
# --------------------------------------------------
energy["Timestamp"] = pd.to_datetime(
    energy["Timestamp"],
    utc=True,
    errors="raise",
).dt.tz_convert("Asia/Kolkata")

energy["Hour"] = energy["Timestamp"].dt.hour

# --------------------------------------------------
# 4. Validate and prepare tariff columns
# --------------------------------------------------
tariffs["Start_Hour"] = pd.to_numeric(
    tariffs["Start_Hour"], errors="raise"
)
tariffs["End_Hour"] = pd.to_numeric(
    tariffs["End_Hour"], errors="raise"
)
tariffs["Price_Per_kWh"] = pd.to_numeric(
    tariffs["Price_Per_kWh"], errors="raise"
)

if tariffs["Tariff_ID"].duplicated().any():
    raise ValueError("Duplicate Tariff_ID values found.")

# --------------------------------------------------
# 5. Match readings with tariffs using plant and hour
# --------------------------------------------------
energy = energy.merge(
    meters[["Meter_ID", "Plant_ID", "Machine_ID"]],
    on="Meter_ID",
    how="left",
    validate="many_to_one",
)

if energy["Machine_ID"].isna().any():
    raise ValueError("Some energy readings have no machine mapping.")

matched = energy.merge(
    tariffs,
    on="Plant_ID",
    how="left",
    validate="many_to_many",
)

matched = matched[
    (matched["Hour"] >= matched["Start_Hour"])
    & (matched["Hour"] < matched["End_Hour"])
].copy()

# Every reading must match exactly one tariff period.
match_counts = matched.groupby("Reading_ID").size()

if len(match_counts) != len(energy):
    raise ValueError("Some readings do not match a tariff period.")

if not match_counts.eq(1).all():
    raise ValueError("Some readings match multiple tariff periods.")

# --------------------------------------------------
# 6. Calculate actual tariff-based costs
# --------------------------------------------------
matched["Energy_Cost_Rs"] = (
    matched["Energy_kWh"] * matched["Price_Per_kWh"]
)

# --------------------------------------------------
# 7. Summarize by machine
# --------------------------------------------------
machine_costs = matched.groupby(
    "Machine_ID",
    as_index=False,
).agg(
    Total_Energy_kWh=("Energy_kWh", "sum"),
    Total_Electricity_Cost_Rs=("Energy_Cost_Rs", "sum"),
    Reading_Count=("Reading_ID", "count"),
)

machine_costs["Total_Energy_kWh"] = (
    machine_costs["Total_Energy_kWh"].round(2)
)

machine_costs["Total_Electricity_Cost_Rs"] = (
    machine_costs["Total_Electricity_Cost_Rs"].round(2)
)

machine_costs = machine_costs.sort_values(
    "Total_Electricity_Cost_Rs",
    ascending=False,
).reset_index(drop=True)

machine_costs.insert(
    0,
    "Cost_Rank",
    range(1, len(machine_costs) + 1),
)

# --------------------------------------------------
# 8. Save report
# --------------------------------------------------
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

output_file = PROCESSED_DIR / "machine_tariff_costs.csv"
machine_costs.to_csv(output_file, index=False)

# --------------------------------------------------
# 9. Display results
# --------------------------------------------------
print("YottaFlex AI - Machine Tariff Cost Analysis")
print("-" * 50)
print(machine_costs.head(10).to_string(index=False))

print(f"\nMachines analyzed: {machine_costs['Machine_ID'].nunique()}")
print(f"Total readings priced: {matched['Reading_ID'].nunique():,}")
print(
    "Total electricity cost: Rs "
    f"{matched['Energy_Cost_Rs'].sum():,.2f}"
)
print(f"\nReport saved to: {output_file}")
