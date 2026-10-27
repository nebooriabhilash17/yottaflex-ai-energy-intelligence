
import pandas as pd
from pathlib import Path

# Sample machine energy and production data
data = {
    "Machine_ID": ["MAC-001", "MAC-002", "MAC-003"],
    "Machine_Name": [
        "Cutting Machine",
        "Drilling Machine",
        "Packaging Machine"
    ],
    "Energy_kWh": [50.0, 40.0, 30.0],
    "Production_Quantity": [100, 0, 150]
}

df = pd.DataFrame(data)

# Calculate electricity used per item produced
df["Energy_Intensity_kWh_per_Unit"] = (
    df["Energy_kWh"] /
    df["Production_Quantity"].replace(0, float("nan"))
)

# Identify machines requiring investigation
df["Investigation_Required"] = (
    (df["Energy_kWh"] > 0) &
    (df["Production_Quantity"] == 0)
)

print("Machine Energy Intensity Analysis")
print(df.to_string(index=False))

# Save the results
output_folder = Path("data") / "processed"
output_folder.mkdir(parents=True, exist_ok=True)

output_file = output_folder / "energy_intensity.csv"
df.to_csv(output_file, index=False)

print("\nResults saved to:", output_file.resolve())
