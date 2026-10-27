
import pandas as pd
import numpy as np
from pathlib import Path

# Fixed seed for reproducible sample data
SEED = 20261022
rng = np.random.default_rng(SEED)

PLANT_ID = "PLANT-001"
START_DATE = "2026-07-25"
DAYS = 90

# Create one weather observation every hour
timestamps = pd.date_range(
    start=START_DATE,
    periods=DAYS * 24,
    freq="h"
)

weather = pd.DataFrame({
    "Weather_ID": [
        f"WEA-{i:06d}" for i in range(1, len(timestamps) + 1)
    ],
    "Plant_ID": PLANT_ID,
    "Timestamp": timestamps,
    "Temperature_C": np.round(
        28 + 5 * np.sin(
            2 * np.pi * timestamps.hour / 24
        ) + rng.normal(0, 1.5, len(timestamps)),
        1
    ),
    "Humidity_Percent": np.round(
        rng.uniform(35, 85, len(timestamps)),
        1
    )
})

# Keep humidity values within a valid range
weather["Humidity_Percent"] = weather[
    "Humidity_Percent"
].clip(0, 100)

# Save the dataset
output_folder = Path("data") / "raw"
output_folder.mkdir(parents=True, exist_ok=True)

output_file = output_folder / "weather_observations.csv"
weather.to_csv(output_file, index=False)

print("Weather data generated!")
print("Plant:", PLANT_ID)
print("Observation count:", len(weather))
print("\nFirst five observations:")
print(weather.head().to_string(index=False))
print("\nSaved to:", output_file.resolve())
