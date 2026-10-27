
import pandas as pd
from pathlib import Path

# Load the test dataset
input_file = Path("data/raw/energy_anomaly_test.csv")
df = pd.read_csv(input_file)

# Detect duplicate reading IDs
df["Duplicate_Detected"] = df.duplicated(
    subset=["Reading_ID"],
    keep=False
)

# Calculate expected energy for a 15-minute interval
expected_energy = df["Average_Power_kW"] * 15 / 60

# Detect incorrect energy values
df["Energy_Mismatch_Detected"] = (
    (df["Energy_kWh"] - expected_energy).abs() > 0.01
)

# Flag a row if either rule detects an issue
df["Anomaly_Detected"] = (
    df["Duplicate_Detected"] |
    df["Energy_Mismatch_Detected"]
)

# Describe the detected issues
df["Detected_Anomaly_Type"] = "NORMAL"

df.loc[
    df["Duplicate_Detected"],
    "Detected_Anomaly_Type"
] = "DUPLICATE_READING"

df.loc[
    df["Energy_Mismatch_Detected"],
    "Detected_Anomaly_Type"
] = "ENERGY_MISMATCH"

# Create output folder
output_folder = Path("data/processed")
output_folder.mkdir(parents=True, exist_ok=True)

# Save results
output_file = output_folder / "anomaly_detection_results.csv"
df.to_csv(output_file, index=False)

print("YottaFlex AI - Anomaly Detection")
print("-" * 40)
print("Total rows checked:", len(df))
print("Rows flagged:", int(df["Anomaly_Detected"].sum()))
print("\nDetected records:")
print(
    df.loc[df["Anomaly_Detected"], [
        "Reading_ID",
        "Detected_Anomaly_Type"
    ]].to_string(index=False)
)

print("\nResults saved to:", output_file.resolve())
