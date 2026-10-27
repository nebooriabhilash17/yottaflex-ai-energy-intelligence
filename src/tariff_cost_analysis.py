
import pandas as pd
from pathlib import Path

# --------------------------------------------------
# 1. Set project paths
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

# --------------------------------------------------
# 2. Load energy readings and tariff schedule
# --------------------------------------------------
energy = pd.read_csv(RAW_DIR / "energy_readings.csv")
tariffs = pd.read_csv(RAW_DIR / "tariffs.csv")

# --------------------------------------------------
# 3. Validate tariff data
# --------------------------------------------------
required_columns = {
    "Tariff_ID",
    "Plant_ID",
    "Period",
    "Start_Hour",
    "End_Hour",
    "Price_Per_kWh",
}

missing = required_columns - set(tariffs.columns)

if missing:
    raise ValueError(f"Missing tariff columns: {sorted(missing)}")

if tariffs.empty:
    raise ValueError("The tariff schedule is empty.")

if tariffs["Price_Per_kWh"].isna().any():
    raise ValueError("Tariff prices cannot be empty.")

if (tariffs["Price_Per_kWh"] < 0).any():
    raise ValueError("Tariff prices cannot be negative.")

# --------------------------------------------------
# 4. Convert timestamps to India local time
# --------------------------------------------------
energy["Timestamp"] = pd.to_datetime(
    energy["Timestamp"],
    utc=True,
    errors="raise",
).dt.tz_convert("Asia/Kolkata")

energy["Hour"] = energy["Timestamp"].dt.hour

# --------------------------------------------------
# 5. Match each reading to its tariff period
# --------------------------------------------------
energy["Plant_ID"] = "PLANT-001"

tariffs["Start_Hour"] = pd.to_numeric(
    tariffs["Start_Hour"], errors="raise"
)
tariffs["End_Hour"] = pd.to_numeric(
    tariffs["End_Hour"], errors="raise"
)
tariffs["Price_Per_kWh"] = pd.to_numeric(
    tariffs["Price_Per_kWh"], errors="raise"
)

# Find all tariff periods that match each reading's plant and hour.
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
    raise ValueError(
        "Some energy readings do not match any tariff period."
    )

if not match_counts.eq(1).all():
    raise ValueError(
        "Some energy readings match multiple tariff periods."
    )

# --------------------------------------------------
# 6. Calculate energy cost
# --------------------------------------------------
matched["Energy_Cost_Rs"] = (
    matched["Energy_kWh"] * matched["Price_Per_kWh"]
)

# --------------------------------------------------
# 7. Summarize costs by meter and tariff period
# --------------------------------------------------
summary = matched.groupby(
    ["Meter_ID", "Tariff_ID", "Period", "Price_Per_kWh"],
    as_index=False,
).agg(
    Total_Energy_kWh=("Energy_kWh", "sum"),
    Total_Cost_Rs=("Energy_Cost_Rs", "sum"),
    Reading_Count=("Reading_ID", "count"),
)
summary["Total_Energy_kWh"] = summary["Total_Energy_kWh"].round(2)
summary["Total_Cost_Rs"] = summary["Total_Cost_Rs"].round(2)

# --------------------------------------------------
# 8. Save detailed summary
# --------------------------------------------------
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

output_file = PROCESSED_DIR / "tariff_cost_analysis.csv"
summary.to_csv(output_file, index=False)

# --------------------------------------------------
# 9. Print results
# --------------------------------------------------
total_energy = matched["Energy_kWh"].sum()
total_cost = matched["Energy_Cost_Rs"].sum()

print("YottaFlex AI - Tariff Cost Analysis")
print("-" * 45)
print("\nCost summary by meter and tariff period:")
print(summary.head(10).to_string(index=False))

print(f"\nTotal readings priced: {matched['Reading_ID'].nunique():,}")
print(f"Total energy: {total_energy:,.2f} kWh")
print(f"Total electricity cost: Rs {total_cost:,.2f}")
print(f"\nReport saved to: {output_file}")
