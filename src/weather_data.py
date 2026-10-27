
import pandas as pd

# Sample weather observations for our factory
weather = {
    "Weather_ID": [
        "WEA-001",
        "WEA-002",
        "WEA-003",
        "WEA-004"
    ],
    "Plant_ID": [
        "PLANT-001",
        "PLANT-001",
        "PLANT-001",
        "PLANT-001"
    ],
    "Timestamp": [
        "2026-10-22 09:00:00",
        "2026-10-22 12:00:00",
        "2026-10-22 15:00:00",
        "2026-10-22 18:00:00"
    ],
    "Temperature_C": [25, 32, 34, 29],
    "Humidity_Percent": [55, 45, 40, 50]
}

df = pd.DataFrame(weather)

print("Factory Weather Data")
print(df)
