
import pandas as pd

# Electricity prices for different time periods
tariffs = {
    "Tariff_ID": [
        "TAR-2026-001",
        "TAR-2026-002",
        "TAR-2026-003"
    ],
    "Period": [
        "OFF_PEAK",
        "NORMAL",
        "PEAK"
    ],
    "Start_Hour": [0, 6, 18],
    "End_Hour": [6, 18, 22],
    "Price_Per_kWh": [4.0, 7.0, 10.0]
}

df = pd.DataFrame(tariffs)

print("Electricity Tariff Data")
print(df)
