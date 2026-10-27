
import pandas as pd

# Electricity usage recorded every 15 minutes
readings = {
    "Reading_ID": [
        "ENG-001",
        "ENG-002",
        "ENG-003",
        "ENG-004"
    ],
    "Meter_ID": [
        "MTR-PLANT-001-001",
        "MTR-PLANT-001-001",
        "MTR-PLANT-001-002",
        "MTR-PLANT-001-002"
    ],
    "Timestamp": [
        "2026-10-22 09:00:00",
        "2026-10-22 09:15:00",
        "2026-10-22 09:00:00",
        "2026-10-22 09:15:00"
    ],
    "Average_Power_kW": [20, 18, 15, 10],
    "Energy_kWh": [5.0, 4.5, 3.75, 2.5]
}

df = pd.DataFrame(readings)

print("Energy Readings Dataset")
print(df)
