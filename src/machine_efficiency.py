
import pandas as pd
from pathlib import Path

# Project folders
raw_folder = Path("data/raw")
output_folder = Path("data/processed")
output_folder.mkdir(parents=True, exist_ok=True)

# Load energy and production data
energy = pd.read_csv(raw_folder / "energy_readings.csv")
production = pd.read_csv(raw_folder / "production_batches.csv")
meters = pd.read_csv(raw_folder / "meters.csv")

# Connect meters to machines
energy = energy.merge(
    meters[["Meter_ID", "Machine_ID"]],
    on="Meter_ID",
    how="left"
)

# Total energy consumed by each machine
energy_summary = energy.groupby("Machine_ID").agg(
    Total_Energy_kWh=("Energy_kWh", "sum")
).reset_index()

# Total production by each machine
production_summary = production.groupby("Machine_ID").agg(
    Total_Units=("Production_Quantity", "sum")
).reset_index()

# Combine energy and production summaries
result = energy_summary.merge(
    production_summary,
    on="Machine_ID",
    how="left"
)

# Calculate energy consumed per unit produced
result["Energy_Per_Unit_kWh"] = (
    result["Total_Energy_kWh"] / result["Total_Units"]
)

# Sort machines by energy intensity
result = result.sort_values(
    "Energy_Per_Unit_kWh",
    ascending=False
)

# Save results
output_file = output_folder / "machine_efficiency.csv"
result.to_csv(output_file, index=False)

print("Machine efficiency analysis completed!")
print(result.to_string(index=False))
print(f"\nResults saved to: {output_file.resolve()}")

# Classify machines using the average energy intensity
average_intensity = result["Energy_Per_Unit_kWh"].mean()

result["Efficiency_Status"] = result["Energy_Per_Unit_kWh"].apply(
    lambda value:
        "HIGH ENERGY INTENSITY"
        if value > average_intensity * 1.25
        else "LOW ENERGY INTENSITY"
        if value < average_intensity * 0.75
        else "NORMAL"
)

# Save the updated report
result.to_csv(output_file, index=False)

print("\nMachine Efficiency Classification")
print(result[[
    "Machine_ID",
    "Energy_Per_Unit_kWh",
    "Efficiency_Status"
]].to_string(index=False))

print(f"\nAverage energy intensity: {average_intensity:.3f} kWh/unit")


# Estimate potential savings for high-intensity machines
average_intensity = result["Energy_Per_Unit_kWh"].mean()

result["Potential_Savings_kWh"] = 0.0

high_intensity = result["Energy_Per_Unit_kWh"] > average_intensity * 1.25

result.loc[high_intensity, "Potential_Savings_kWh"] = (
    result.loc[high_intensity, "Total_Units"]
    * (
        result.loc[high_intensity, "Energy_Per_Unit_kWh"]
        - average_intensity
    )
)

# Assume an illustrative electricity price of ₹7 per kWh
assumed_price_per_kwh = 7.0

result["Potential_Savings_Rs"] = (
    result["Potential_Savings_kWh"] * assumed_price_per_kwh
)

# Save the updated report
result.to_csv(output_file, index=False)

print("\nPotential Energy Savings")
print(
    result.loc[
        high_intensity,
        [
            "Machine_ID",
            "Potential_Savings_kWh",
            "Potential_Savings_Rs",
        ],
    ].to_string(index=False)
)

print(
    "\nTotal potential savings (kWh):",
    round(result["Potential_Savings_kWh"].sum(), 2),
)

print(
    "Total potential savings (₹):",
    round(result["Potential_Savings_Rs"].sum(), 2),
)

