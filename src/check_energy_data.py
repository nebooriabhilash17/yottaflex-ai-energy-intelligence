
import pandas as pd
from pathlib import Path

# Load the generated datasets
energy = pd.read_csv("data/raw/energy_readings.csv")
meters = pd.read_csv("data/raw/meters.csv")

print("YottaFlex AI - Data Quality Check")
print("-" * 40)

# 1. Check for duplicate reading IDs
duplicate_count = energy["Reading_ID"].duplicated().sum()
print("Duplicate reading IDs:", duplicate_count)

# 2. Check for missing values
missing_count = energy.isnull().sum().sum()
print("Missing values:", missing_count)

# 3. Check for negative energy values
negative_count = (energy["Energy_kWh"] < 0).sum()
print("Negative energy readings:", negative_count)

# 4. Check whether every reading has a valid meter
invalid_meter_count = (
    ~energy["Meter_ID"].isin(meters["Meter_ID"])
).sum()
print("Readings with unknown meters:", invalid_meter_count)

# 5. Check the relationship between power and energy
expected_energy = energy["Average_Power_kW"] * 15 / 60

energy_difference = (
    energy["Energy_kWh"] - expected_energy
).abs()

incorrect_energy_count = (energy_difference > 0.001).sum()
print("Incorrect energy calculations:", incorrect_energy_count)

# Save validation results
results = pd.DataFrame({
    "Check": [
        "Duplicate reading IDs",
        "Missing values",
        "Negative energy readings",
        "Readings with unknown meters",
        "Incorrect energy calculations"
    ],
    "Issue_Count": [
        duplicate_count,
        missing_count,
        negative_count,
        invalid_meter_count,
        incorrect_energy_count
    ]
})

output_folder = Path("data/processed")
output_folder.mkdir(parents=True, exist_ok=True)

output_file = output_folder / "data_quality_report.csv"
results.to_csv(output_file, index=False)

print("\nValidation Summary")
print(results.to_string(index=False))
print("\nReport saved to:", output_file.resolve())
