
import pandas as pd

# Sample energy and production data
data = {
    "Machine_ID": ["MAC-001", "MAC-002", "MAC-003", "MAC-004"],
    "Machine_Name": [
        "Cutting Machine",
        "Drilling Machine",
        "Packaging Machine",
        "Welding Machine"
    ],
    "Energy_kWh": [5.0, 4.0, 2.5, 3.0],
    "Production_Quantity": [100, 0, 150, 0],
    "Price_Per_kWh": [7.0, 7.0, 10.0, 10.0]
}

df = pd.DataFrame(data)

# Flag possible energy waste
df["Potential_Waste"] = (
    (df["Energy_kWh"] > 0) &
    (df["Production_Quantity"] == 0)
)

# Calculate energy cost for every machine
df["Energy_Cost"] = df["Energy_kWh"] * df["Price_Per_kWh"]

# Calculate cost associated with flagged readings
df["Potential_Waste_Cost"] = (
    df["Energy_Cost"] * df["Potential_Waste"].astype(int)
)

print("Energy Waste Cost Analysis")
print(df.to_string(index=False))

print("\nPotential Waste Energy:",
      df.loc[df["Potential_Waste"], "Energy_kWh"].sum(), "kWh")

print("Potential Waste Cost: ₹",
      df["Potential_Waste_Cost"].sum())
