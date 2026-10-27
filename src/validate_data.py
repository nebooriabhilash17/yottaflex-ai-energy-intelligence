
import pandas as pd

# Sample energy readings
data = {
    "Reading_ID": ["ENG-001", "ENG-002", "ENG-003", "ENG-003"],
    "Meter_ID": [
        "MTR-PLANT-001-001",
        "MTR-PLANT-001-001",
        "MTR-PLANT-001-002",
        "MTR-PLANT-001-002"
    ],
    "Energy_kWh": [5.0, 4.5, 3.75, -2.0]
}

df = pd.DataFrame(data)

print("Original Energy Readings")
print(df.to_string(index=False))

# Check for duplicate reading IDs
duplicate_rows = df[df.duplicated("Reading_ID", keep=False)]

# Check for missing values
missing_values = df[df.isnull().any(axis=1)]

# Check for negative energy
negative_energy = df[df["Energy_kWh"] < 0]

print("\nDuplicate Reading IDs:")
print(duplicate_rows.to_string(index=False))

print("\nRows with Missing Values:")
if missing_values.empty:
    print("No missing values found.")
else:
    print(missing_values.to_string(index=False))

print("\nRows with Negative Energy:")
print(negative_energy.to_string(index=False))
