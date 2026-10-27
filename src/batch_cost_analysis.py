
import pandas as pd
from pathlib import Path

# Input and output files
input_file = Path("data/processed/batch_anomaly_results.csv")
output_folder = Path("data/processed")
output_folder.mkdir(parents=True, exist_ok=True)

# Illustrative electricity price
price_per_kwh = 7.0

# Load the batch analysis
df = pd.read_csv(input_file)

# Calculate energy cost for each batch
df["Estimated_Energy_Cost_Rs"] = (
    df["Matched_Energy_kWh"] * price_per_kwh
)

# Separate flagged and normal batches
flagged = df[df["Anomaly_Status"] == "INVESTIGATE"].copy()

# Save the detailed report
output_file = output_folder / "batch_cost_analysis.csv"
df.to_csv(output_file, index=False)

# Summarize the results
print("YottaFlex AI - Batch Cost Analysis")
print("-" * 45)
print("Total batches:", len(df))
print("Flagged batches:", len(flagged))
print(
    "Energy used by flagged batches (kWh):",
    round(flagged["Matched_Energy_kWh"].sum(), 2),
)
print(
    "Energy cost of flagged batches (Rs):",
    round(flagged["Estimated_Energy_Cost_Rs"].sum(), 2),
)

print("\nTop 5 flagged batches by energy cost:")
print(
    flagged.nlargest(5, "Estimated_Energy_Cost_Rs")[
        [
            "Machine_ID",
            "Batch_ID",
            "Matched_Energy_kWh",
            "Estimated_Energy_Cost_Rs",
            "Intensity_Z_Score",
        ]
    ].to_string(index=False)
)

print(f"\nReport saved to: {output_file.resolve()}")
