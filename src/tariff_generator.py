
import pandas as pd
from pathlib import Path

# Sample electricity tariff schedule
tariffs = pd.DataFrame({
    "Tariff_ID": [
        "TAR-2026-001",
        "TAR-2026-002",
        "TAR-2026-003"
    ],
    "Plant_ID": [
        "PLANT-001",
        "PLANT-001",
        "PLANT-001"
    ],
    "Period": [
        "OFF_PEAK",
        "NORMAL",
        "PEAK"
    ],
    "Start_Hour": [0, 6, 18],
    "End_Hour": [6, 18, 22],
    "Price_Per_kWh": [4.0, 7.0, 10.0]
})

# Add the missing late-evening period
late_evening = pd.DataFrame([{
    "Tariff_ID": "TAR-2026-004",
    "Plant_ID": "PLANT-001",
    "Period": "OFF_PEAK",
    "Start_Hour": 22,
    "End_Hour": 24,
    "Price_Per_kWh": 4.0
}])

tariffs = pd.concat(
    [tariffs, late_evening],
    ignore_index=True
)

# Check that the periods cover all 24 hours
total_hours = (
    tariffs["End_Hour"] - tariffs["Start_Hour"]
).sum()

assert total_hours == 24, "Tariff periods must cover 24 hours."

# Save the tariff schedule
output_folder = Path("data") / "raw"
output_folder.mkdir(parents=True, exist_ok=True)

output_file = output_folder / "tariffs.csv"
tariffs.to_csv(output_file, index=False)

print("Tariff schedule generated successfully!")
print(tariffs.to_string(index=False))
print("\nHours covered:", total_hours)
print("Saved to:", output_file.resolve())
