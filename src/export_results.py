
import pandas as pd
from pathlib import Path

# Sample machine energy and production data
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

# Identify possible energy waste
df["Potential_Waste"] = (
    (df["Energy_kWh"] > 0) &
    (df["Production_Quantity"] == 0)
)

# Calculate electricity cost
df["Energy_Cost"] = df["Energy_kWh"] * df["Price_Per_kWh"]

# Cost associated with flagged readings
df["Potential_Waste_Cost"] = (
    df["Energy_Cost"] * df["Potential_Waste"].astype(int)
)

# Create an output folder
output_folder = Path("data") / "processed"
output_folder.mkdir(parents=True, exist_ok=True)

# Save the results to CSV
output_file = output_folder / "energy_waste_results.csv"
df.to_csv(output_file, index=False)

print("Results saved successfully!")
print("File location:", output_file.resolve())
print("\nSaved results:")
print(df.to_string(index=False))
