
import pandas as pd
from pathlib import Path

input_file = Path("data/processed/production_energy_analysis.csv")
output_file = Path("data/processed/batch_anomaly_results.csv")

df = pd.read_csv(input_file)

# Calculate each machine's average and standard deviation
baseline = df.groupby("Machine_ID")[
    "Energy_Intensity_kWh_per_Unit"
].agg(["mean", "std"]).reset_index()

baseline = baseline.rename(columns={
    "mean": "Machine_Average_Intensity",
    "std": "Machine_Std_Intensity"
})

# Add the machine baseline to each batch
df = df.merge(baseline, on="Machine_ID", how="left")

# Calculate how far each batch is from its machine baseline
df["Intensity_Z_Score"] = (
    df["Energy_Intensity_kWh_per_Unit"]
    - df["Machine_Average_Intensity"]
) / df["Machine_Std_Intensity"].replace(0, float("nan"))

# Flag batches more than 2 standard deviations above baseline
df["Anomaly_Status"] = df["Intensity_Z_Score"].apply(
    lambda z: "INVESTIGATE" if pd.notna(z) and z > 2 else "NORMAL"
)

df.to_csv(output_file, index=False)

flagged = df[df["Anomaly_Status"] == "INVESTIGATE"]

print("YottaFlex AI - Batch Anomaly Detection")
print("-" * 45)
print("Total batches:", len(df))
print("Batches flagged for investigation:", len(flagged))

print("\nTop flagged batches:")
print(
    flagged.nlargest(10, "Intensity_Z_Score")[
        [
            "Machine_ID",
            "Batch_ID",
            "Production_Quantity",
            "Energy_Intensity_kWh_per_Unit",
            "Machine_Average_Intensity",
            "Intensity_Z_Score",
        ]
    ].to_string(index=False)
)

print(f"\nReport saved to: {output_file.resolve()}")
