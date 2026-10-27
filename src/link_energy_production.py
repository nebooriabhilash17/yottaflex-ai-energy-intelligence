
import pandas as pd
from pathlib import Path

# Load the generated CSV files
energy = pd.read_csv("data/raw/energy_readings.csv")
production = pd.read_csv("data/raw/production_batches.csv")

# Convert timestamps into datetime format
energy["Timestamp"] = pd.to_datetime(energy["Timestamp"])
production["Start_Time"] = pd.to_datetime(production["Start_Time"])
production["End_Time"] = pd.to_datetime(production["End_Time"])

# Create a summary of production by machine
production_summary = production.groupby("Machine_ID").agg(
    Total_Production=("Production_Quantity", "sum"),
    Total_Batches=("Batch_ID", "count")
).reset_index()

print("Production Summary")
print(production_summary.to_string(index=False))

# Show the energy readings
print("\nEnergy Readings")
print(energy.head(10).to_string(index=False))

# Save the production summary
output_folder = Path("data") / "processed"
output_folder.mkdir(parents=True, exist_ok=True)

output_file = output_folder / "production_summary.csv"
production_summary.to_csv(output_file, index=False)

print("\nProduction summary saved to:", output_file.resolve())
