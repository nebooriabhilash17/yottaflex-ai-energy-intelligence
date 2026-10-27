import numpy as np
import pandas as pd
from pathlib import Path

SEED = 20261022          # fixed seed = same data every run
N_METERS = 20

rng = np.random.default_rng(SEED)   # ALL randomness must come from this
out = Path("data")
out.mkdir(exist_ok=True)

# --- Table 1: Plant ---
plants = pd.DataFrame({
    "plant_id": ["P01"],
    "plant_name": ["Hyderabad Plant"],
    "timezone": ["Asia/Kolkata"],
})

# --- Table 2: Meter (each belongs to the plant) ---
meters = pd.DataFrame({
    "meter_id": [f"MTR-P01-{i:03d}" for i in range(1, N_METERS + 1)],
    "plant_id": "P01",
})

# --- Table 3: Machine (each belongs to a meter) ---
rows = []
counter = 1
for meter_id in meters["meter_id"]:
    for _ in range(rng.integers(2, 5)):        # 2 to 4 machines per meter
        rows.append({
            "machine_id": f"MCH-P01-{counter:03d}",
            "meter_id": meter_id,
            "rated_kw": int(rng.integers(10, 80)),   # machine power rating
            "idle_kw": 0,                             # we'll fill this later
        })
        counter += 1
machines = pd.DataFrame(rows)
machines["idle_kw"] = (machines["rated_kw"] * 0.15).round(2)   # derived, not random

plants.to_csv(out / "plant.csv", index=False)
meters.to_csv(out / "meter.csv", index=False)
machines.to_csv(out / "machine.csv", index=False)
print("Done:", len(plants), "plant,", len(meters), "meters,", len(machines), "machines")