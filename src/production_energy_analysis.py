
import pandas as pd
from pathlib import Path

# Load generated datasets
energy = pd.read_csv("data/raw/energy_readings.csv")
batches = pd.read_csv("data/raw/production_batches.csv")
meters = pd.read_csv("data/raw/meters.csv")

# Convert all timestamps to the same timezone.
# Energy timestamps already contain timezone information.
energy["Timestamp"] = pd.to_datetime(
    energy["Timestamp"], utc=True
)

# Production times are factory-local times in Asia/Kolkata.
batches["Start_Time"] = pd.to_datetime(
    batches["Start_Time"]
).dt.tz_localize("Asia/Kolkata").dt.tz_convert("UTC")

batches["End_Time"] = pd.to_datetime(
    batches["End_Time"]
).dt.tz_localize("Asia/Kolkata").dt.tz_convert("UTC")

# Connect each meter to its machine
energy = energy.merge(
    meters[["Meter_ID", "Machine_ID"]],
    on="Meter_ID",
    how="left",
    validate="many_to_one"
)

# Match readings only to batches for the same machine.
# Process one machine at a time to avoid a huge intermediate table.
results = []

for machine_id, machine_energy in energy.groupby("Machine_ID"):
    machine_batches = batches[
        batches["Machine_ID"] == machine_id
    ]

    if machine_batches.empty:
        continue

    for _, batch in machine_batches.iterrows():
        mask = (
            (machine_energy["Timestamp"] >= batch["Start_Time"]) &
            (machine_energy["Timestamp"] < batch["End_Time"])
        )

        matched_readings = machine_energy.loc[mask]

        if not matched_readings.empty:
            results.append({
                "Machine_ID": machine_id,
                "Batch_ID": batch["Batch_ID"],
                "Production_Quantity": batch["Production_Quantity"],
                "Matched_Readings": len(matched_readings),
                "Matched_Energy_kWh": matched_readings["Energy_kWh"].sum()
            })

# Create the results table
summary = pd.DataFrame(results)

if not summary.empty:
    summary["Energy_Intensity_kWh_per_Unit"] = (
        summary["Matched_Energy_kWh"] /
        summary["Production_Quantity"].replace(0, float("nan"))
    )

    summary["Matched_Energy_kWh"] = (
        summary["Matched_Energy_kWh"].round(2)
    )

    summary["Energy_Intensity_kWh_per_Unit"] = (
        summary["Energy_Intensity_kWh_per_Unit"].round(4)
    )

# Save the report
output_folder = Path("data/processed")
output_folder.mkdir(parents=True, exist_ok=True)

output_file = output_folder / "production_energy_analysis.csv"
summary.to_csv(output_file, index=False)

print("Production and Energy Analysis")
print("-" * 40)
print("Matched batch records:", len(summary))
print("\nFirst five results:")
print(summary.head().to_string(index=False))
print("\nReport saved to:", output_file.resolve())
