
import pandas as pd

# Electricity meter information
meters = {
    "Meter_ID": [
        "MTR-PLANT-001-001",
        "MTR-PLANT-001-002"
    ],
    "Plant_ID": [
        "PLANT-001",
        "PLANT-001"
    ],
    "Meter_Name": [
        "Cutting Machine Meter",
        "Drilling Machine Meter"
    ],
    "Unit": ["kWh", "kWh"],
    "Sampling_Minutes": [15, 15]
}

# Convert the information into a table
df = pd.DataFrame(meters)

# Display the meter table
print(df)
