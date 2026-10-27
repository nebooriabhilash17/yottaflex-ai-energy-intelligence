
import pandas as pd

# Create sample data with intentional errors
data = {
    "Reading_ID": [
        "ENG-001",
        "ENG-002",
        "ENG-002",
        "ENG-004"
    ],
    "Meter_ID": [
        "MTR-PLANT-001-001",
        "MTR-PLANT-001-001",
        "MTR-UNKNOWN-999",
        "MTR-PLANT-001-002"
    ],
    "Average_Power_kW": [20, 18, 15, 10],
    "Energy_kWh": [5.0, 4.5, -2.0, 9.0]
}

df = pd.DataFrame(data)

# Load the valid meter list
meters = pd.read_csv("data/raw/meters.csv")

print("Testing data with intentional errors")
print("-" * 45)

# Check duplicate IDs
duplicates = df[df.duplicated("Reading_ID", keep=False)]
print("\nDuplicate reading IDs:")
print(duplicates[["Reading_ID"]].to_string(index=False))

# Check negative energy
negative = df[df["Energy_kWh"] < 0]
print("\nNegative energy readings:")
print(negative[["Reading_ID", "Energy_kWh"]].to_string(index=False))

# Check unknown meters
unknown = df[~df["Meter_ID"].isin(meters["Meter_ID"])]
print("\nReadings with unknown meters:")
print(unknown[["Reading_ID", "Meter_ID"]].to_string(index=False))

# Check energy calculation for 15-minute readings
expected_energy = df["Average_Power_kW"] * 15 / 60
incorrect = df[
    (df["Energy_kWh"] - expected_energy).abs() > 0.001
]
print("\nIncorrect energy calculations:")
print(incorrect[["Reading_ID", "Energy_kWh"]].to_string(index=False))

print("\nTest completed.")
