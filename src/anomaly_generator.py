
import pandas as pd
from pathlib import Path

# Load the original energy readings
energy = pd.read_csv("data/raw/energy_readings.csv")

# Work on a separate copy so the original remains unchanged
test_data = energy.head(100).copy()

# Start with every reading marked as normal
test_data["Anomaly_Type"] = "NORMAL"

# Create a separate ground-truth record
ground_truth = []

# Anomaly 1: duplicate a reading
duplicate = test_data.iloc[[0]].copy()
duplicate["Anomaly_Type"] = "DUPLICATE_READING"

test_data.loc[test_data.index[0], "Anomaly_Type"] = (
    "DUPLICATE_READING"
)

test_data = pd.concat(
    [test_data, duplicate],
    ignore_index=True
)

ground_truth.append({
    "Reading_ID": duplicate.iloc[0]["Reading_ID"],
    "Anomaly_Type": "DUPLICATE_READING",
    "Description": "Reading appears more than once"
})

# Anomaly 2: create an incorrect energy value
test_data.loc[1, "Energy_kWh"] = (
    test_data.loc[1, "Energy_kWh"] + 10
)
test_data.loc[1, "Anomaly_Type"] = "ENERGY_MISMATCH"

ground_truth.append({
    "Reading_ID": test_data.loc[1, "Reading_ID"],
    "Anomaly_Type": "ENERGY_MISMATCH",
    "Description": "Energy does not match average power"
})

# Save test data and ground truth separately
raw_folder = Path("data/raw")
truth_folder = Path("data/ground_truth")

raw_folder.mkdir(parents=True, exist_ok=True)
truth_folder.mkdir(parents=True, exist_ok=True)

test_data.to_csv(
    raw_folder / "energy_anomaly_test.csv",
    index=False
)

pd.DataFrame(ground_truth).to_csv(
    truth_folder / "energy_anomaly_ground_truth.csv",
    index=False
)

print("Anomaly test data created!")
print("Test readings:", len(test_data))
print("Ground-truth labels:", len(ground_truth))
print("\nAnomaly types:")
print(test_data["Anomaly_Type"].value_counts())
print("\nOriginal energy_readings.csv was not changed.")
