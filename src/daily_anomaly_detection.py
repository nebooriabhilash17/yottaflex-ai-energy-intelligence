
import pandas as pd
from pathlib import Path

# Load the daily energy report
input_file = Path("data/processed/daily_energy_summary.csv")
output_file = Path("data/processed/daily_anomaly_results.csv")

df = pd.read_csv(input_file)

# Calculate the mean and standard deviation
mean_energy = df["Total_Energy_kWh"].mean()
std_energy = df["Total_Energy_kWh"].std()

if std_energy == 0 or pd.isna(std_energy):
    df["Z_Score"] = 0.0
else:
    df["Z_Score"] = (
        (df["Total_Energy_kWh"] - mean_energy) / std_energy
    )

# Flag days more than 2 standard deviations from the mean
df["Anomaly_Status"] = df["Z_Score"].apply(
    lambda z: "UNUSUAL CONSUMPTION"
    if abs(z) > 2
    else "NORMAL"
)

df.to_csv(output_file, index=False)

print("YottaFlex AI - Daily Anomaly Detection")
print("--------------------------------------")
print(f"Average daily energy: {mean_energy:.2f} kWh")
print(f"Standard deviation: {std_energy:.2f} kWh")
print(
    "Unusual days detected:",
    (df["Anomaly_Status"] == "UNUSUAL CONSUMPTION").sum()
)

print("\nDays flagged:")
print(
    df.loc[
        df["Anomaly_Status"] == "UNUSUAL CONSUMPTION",
        ["Date", "Total_Energy_kWh", "Z_Score"]
    ].to_string(index=False)
)

print(f"\nReport saved to: {output_file.resolve()}")
