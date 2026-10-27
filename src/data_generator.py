
import pandas as pd
import numpy as np
from pathlib import Path

# Reproducible synthetic data
SEED = 20261022
rng = np.random.default_rng(SEED)

PLANT_ID = "PLANT-001"
METER_COUNT = 20
DAYS = 90
INTERVAL_MINUTES = 15

# 1. Create plant data
plants = pd.DataFrame({
    "Plant_ID": [PLANT_ID],
    "Plant_Name": ["Hyderabad Factory"],
    "Location": ["Hyderabad"],
    "Timezone": ["Asia/Kolkata"],
    "Status": ["ACTIVE"]
})

# 2. Create 20 machines
machines = pd.DataFrame({
    "Machine_ID": [f"MAC-{i:03d}" for i in range(1, METER_COUNT + 1)],
    "Machine_Name": [
        f"Factory Machine {i:02d}"
        for i in range(1, METER_COUNT + 1)
    ],
    "Rated_Power_kW": rng.integers(10, 51, size=METER_COUNT),
    "Status": ["ACTIVE"] * METER_COUNT
})

# 3. Create 20 meters, one for each machine
meters = pd.DataFrame({
    "Meter_ID": [
        f"MTR-{PLANT_ID}-{i:03d}"
        for i in range(1, METER_COUNT + 1)
    ],
    "Plant_ID": [PLANT_ID] * METER_COUNT,
    "Machine_ID": machines["Machine_ID"],
    "Unit": ["kWh"] * METER_COUNT,
    "Sampling_Minutes": [INTERVAL_MINUTES] * METER_COUNT
})

# 4. Generate timestamps in the plant's local timezone
start = pd.Timestamp("2026-07-25 00:00:00", tz="Asia/Kolkata")
end = start + pd.Timedelta(days=DAYS)

timestamps = pd.date_range(
    start=start,
    end=end,
    freq=f"{INTERVAL_MINUTES}min",
    inclusive="left"
)

# 5. Generate energy readings
readings = []

for machine_number, machine in machines.iterrows():
    meter_id = meters.iloc[machine_number]["Meter_ID"]
    rated_power = machine["Rated_Power_kW"]

    # Random power level for each 15-minute interval
    power_values = rng.uniform(
        rated_power * 0.25,
        rated_power * 0.80,
        size=len(timestamps)
    )

    energy_values = power_values * INTERVAL_MINUTES / 60

    for timestamp, power, energy in zip(
        timestamps, power_values, energy_values
    ):
        readings.append({
            "Reading_ID": (
                f"ENG-{meter_id}-"
                f"{timestamp.strftime('%Y%m%d%H%M')}"
            ),
            "Meter_ID": meter_id,
            "Timestamp": timestamp.isoformat(),
            "Average_Power_kW": round(float(power), 3),
            "Energy_kWh": round(float(energy), 3)
        })

energy_readings = pd.DataFrame(readings)

# 6. Save generated datasets
output_folder = Path("data") / "raw"
output_folder.mkdir(parents=True, exist_ok=True)

plants.to_csv(output_folder / "plants.csv", index=False)
machines.to_csv(output_folder / "machines.csv", index=False)
meters.to_csv(output_folder / "meters.csv", index=False)
energy_readings.to_csv(
    output_folder / "energy_readings.csv",
    index=False
)

# 7. Display generation summary
print("YottaFlex AI - Synthetic Data Generator")
print("-" * 45)
print("Random seed:", SEED)
print("Plants:", len(plants))
print("Machines:", len(machines))
print("Meters:", len(meters))
print("Days:", DAYS)
print("Readings per meter:", len(timestamps))
print("Total energy readings:", len(energy_readings))
print("\nFiles saved in:", output_folder.resolve())
