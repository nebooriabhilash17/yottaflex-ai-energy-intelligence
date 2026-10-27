
import pandas as pd
from pathlib import Path

# Define file paths
input_file = Path("data/raw/energy_readings.csv")
output_folder = Path("data/processed")
output_folder.mkdir(parents=True, exist_ok=True)

# Load energy readings
df = pd.read_csv(input_file)

# Convert timestamps into datetime format
df["Timestamp"] = pd.to_datetime(df["Timestamp"], utc=True)
df["Timestamp"] = df["Timestamp"].dt.tz_convert("Asia/Kolkata")

# Extract the date from each timestamp
df["Date"] = df["Timestamp"].dt.date

# Calculate daily energy consumption
daily = df.groupby("Date").agg(
    Total_Energy_kWh=("Energy_kWh", "sum"),
    Total_Readings=("Reading_ID", "count"),
    Average_Power_kW=("Average_Power_kW", "mean")
).reset_index()

# Calculate the average daily energy consumption
average_daily_energy = daily["Total_Energy_kWh"].mean()

# Flag days above 120% of the average
daily["Energy_Status"] = daily["Total_Energy_kWh"].apply(
    lambda value: (
        "HIGH CONSUMPTION"
        if value > average_daily_energy * 1.20
        else "NORMAL"
    )
)

# Save the report
output_file = output_folder / "daily_energy_summary.csv"
daily.to_csv(output_file, index=False)

print("YottaFlex AI - Daily Energy Summary")
print("-" * 45)
print(daily.head(10).to_string(index=False))
print(f"\nDays analyzed: {len(daily)}")
print(f"Average daily energy: {average_daily_energy:.2f} kWh")
print(f"Report saved to: {output_file.resolve()}")
