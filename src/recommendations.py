
import pandas as pd
from pathlib import Path

# File locations
input_file = Path("data/processed/machine_efficiency.csv")
output_folder = Path("data/processed")
output_folder.mkdir(parents=True, exist_ok=True)

# Load machine efficiency results
df = pd.read_csv(input_file)

# Keep machines classified as high energy intensity
recommendations = df[
    df["Efficiency_Status"] == "HIGH ENERGY INTENSITY"
].copy()

# Create a recommendation for each flagged machine
recommendations["Priority"] = "HIGH"

recommendations["Recommendation"] = (
    "Inspect machine operating hours, idle consumption, "
    "production mix, and meter accuracy."
)

recommendations["Estimated_Savings_kWh"] = (
    recommendations["Potential_Savings_kWh"]
)

recommendations["Estimated_Savings_Rs"] = (
    recommendations["Potential_Savings_Rs"]
)

# Select report columns
report = recommendations[
    [
        "Machine_ID",
        "Energy_Per_Unit_kWh",
        "Priority",
        "Recommendation",
        "Estimated_Savings_kWh",
        "Estimated_Savings_Rs",
    ]
].sort_values("Estimated_Savings_Rs", ascending=False)

# Save report
output_file = output_folder / "energy_saving_recommendations.csv"
report.to_csv(output_file, index=False)

print("YottaFlex AI - Energy Saving Recommendations")
print("-" * 55)
print(report.to_string(index=False))

print("\nMachines requiring investigation:", len(report))
print(
    "Total estimated savings (Rs):",
    round(report["Estimated_Savings_Rs"].sum(), 2),
)
print(f"\nReport saved to: {output_file.resolve()}")
