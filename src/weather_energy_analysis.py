
import pandas as pd
from pathlib import Path

# Load energy and weather datasets
energy = pd.read_csv("data/raw/energy_readings.csv")
weather = pd.read_csv("data/raw/weather_observations.csv")

# Convert timestamps to India local time
energy["Timestamp"] = pd.to_datetime(
    energy["Timestamp"], utc=True
).dt.tz_convert("Asia/Kolkata")

weather["Timestamp"] = pd.to_datetime(
    weather["Timestamp"]
)

# Remove timezone information after converting energy to local time.
# Both datasets now use the same local clock for matching.
energy["Timestamp"] = energy["Timestamp"].dt.tz_localize(None)

# Match each energy reading to the weather observation
# from the same hour.
energy["Weather_Hour"] = energy["Timestamp"].dt.floor("h")
weather["Weather_Hour"] = weather["Timestamp"].dt.floor("h")

combined = energy.merge(
    weather[[
        "Plant_ID",
        "Weather_Hour",
        "Temperature_C",
        "Humidity_Percent"
    ]],
    left_on="Weather_Hour",
    right_on="Weather_Hour",
    how="left",
    validate="many_to_one"
)

# Summarize electricity usage by temperature range
combined["Temperature_Range"] = pd.cut(
    combined["Temperature_C"],
    bins=[-float("inf"), 25, 30, 35, float("inf")],
    labels=["Below 25C", "25-30C", "30-35C", "Above 35C"]
)

summary = combined.groupby(
    "Temperature_Range",
    observed=True,
    as_index=False
).agg(
    Average_Energy_kWh=("Energy_kWh", "mean"),
    Total_Energy_kWh=("Energy_kWh", "sum"),
    Reading_Count=("Reading_ID", "count")
)

summary["Average_Energy_kWh"] = summary[
    "Average_Energy_kWh"
].round(3)

summary["Total_Energy_kWh"] = summary[
    "Total_Energy_kWh"
].round(2)

# Save the analysis
output_folder = Path("data/processed")
output_folder.mkdir(parents=True, exist_ok=True)

output_file = output_folder / "weather_energy_analysis.csv"
summary.to_csv(output_file, index=False)

print("Weather and Energy Analysis")
print("-" * 40)
print(summary.to_string(index=False))

print("\nEnergy readings without matched weather:",
      combined["Temperature_C"].isna().sum())

print("\nReport saved to:", output_file.resolve())
