
import pandas as pd
from pathlib import Path

# Load generated CSV files
energy = pd.read_csv("data/raw/energy_readings.csv")
meters = pd.read_csv("data/raw/meters.csv")

# Connect each reading to its meter information
df = pd.merge(
    energy,
    meters[["Meter_ID", "Meter_Name", "Plant_ID"]],
    on="Meter_ID",
    how="left",
    validate="many_to_one"
)

# Summarize energy consumption for each meter
summary = df.groupby(
    ["Meter_ID", "Meter_Name", "Plant_ID"],
    as_index=False
).agg(
    Total_Energy_kWh=("Energy_kWh", "sum"),
    Average_Power_kW=("Average_Power_kW", "mean"),
    Reading_Count=("Reading_ID", "count")
)

# Round the results for readability
summary["Total_Energy_kWh"] = summary["Total_Energy_kWh"].round(2)
summary["Average_Power_kW"] = summary["Average_Power_kW"].round(2)

# Save the summary
output_folder = Path("data/processed")
output_folder.mkdir(parents=True, exist_ok=True)

output_file = output_folder / "energy_summary.csv"
summary.to_csv(output_file, index=False)

print("Energy Consumption Summary")
print(summary.to_string(index=False))
print("\nTotal factory energy consumption:",
      round(df["Energy_kWh"].sum(), 2), "kWh")
print("\nSaved to:", output_file.resolve())
