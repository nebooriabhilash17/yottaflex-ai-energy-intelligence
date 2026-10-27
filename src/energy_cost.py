
import pandas as pd

# Electricity readings
energy_data = {
    "Machine_ID": ["MAC-001", "MAC-002", "MAC-003"],
    "Machine_Name": [
        "Cutting Machine",
        "Drilling Machine",
        "Packaging Machine"
    ],
    "Energy_kWh": [5.0, 3.75, 2.5],
    "Price_Per_kWh": [7.0, 7.0, 10.0]
}

df = pd.DataFrame(energy_data)

# Calculate electricity cost
df["Energy_Cost"] = df["Energy_kWh"] * df["Price_Per_kWh"]

print("Machine Electricity Cost")
print(df)

print("\nTotal Electricity Consumption:", df["Energy_kWh"].sum(), "kWh")
print("Total Electricity Cost: ₹", df["Energy_Cost"].sum())
