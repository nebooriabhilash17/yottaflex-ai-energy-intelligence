
import pandas as pd
from pathlib import Path

# Load the existing datasets
energy = pd.read_csv("data/raw/energy_readings.csv")
batches = pd.read_csv("data/raw/production_batches.csv")

# Convert text timestamps into datetime values
energy["Timestamp"] = pd.to_datetime(energy["Timestamp"])
batches["Start_Time"] = pd.to_datetime(batches["Start_Time"])
batches["End_Time"] = pd.to_datetime(batches["End_Time"])

# Match each energy reading to a batch on the same machine
results = []

for _, reading in energy.iterrows():
    matching_batches = batches[
        (batches["Machine_ID"] == reading["Meter_ID"].replace(
            "MTR-PLANT-001-001", "MAC-001"
        ).replace(
            "MTR-PLANT-001-002", "MAC-002"
        ))
        & (batches["Start_Time"] <= reading["Timestamp"])
        & (reading["Timestamp"] < batches["End_Time"])
    ]

    if matching_batches.empty:
        results.append({
            "Reading_ID": reading["Reading_ID"],
            "Meter_ID": reading["Meter_ID"],
            "Timestamp": reading["Timestamp"],
            "Energy_kWh": reading["Energy_kWh"],
            "Batch_ID": None,
            "Production_Quantity": 0,
            "Production_Match": "NO_ACTIVE_BATCH"
        })
    else:
        batch = matching_batches.iloc[0]
        results.append({
            "Reading_ID": reading["Reading_ID"],
            "Meter_ID": reading["Meter_ID"],
            "Timestamp": reading["Timestamp"],
            "Energy_kWh": reading["Energy_kWh"],
            "Batch_ID": batch["Batch_ID"],
            "Production_Quantity": batch["Production_Quantity"],
            "Production_Match": "ACTIVE_BATCH"
        })

matched_df = pd.DataFrame(results)

# Save the matched data
output_folder = Path("data/processed")
output_folder.mkdir(parents=True, exist_ok=True)

output_file = output_folder / "matched_energy_production.csv"
matched_df.to_csv(output_file, index=False)

print("Energy and production matching completed!")
print("\nFirst 10 records:")
print(matched_df.head(10).to_string(index=False))

print("\nMatching summary:")
print(matched_df["Production_Match"].value_counts().to_string())
print("\nSaved to:", output_file.resolve())
