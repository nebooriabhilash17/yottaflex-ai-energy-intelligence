
import pandas as pd
from pathlib import Path

# Sample data containing intentional errors
data = {
    "Reading_ID": ["ENG-001", "ENG-002", "ENG-002", "ENG-004"],
    "Meter_ID": [
        "MTR-PLANT-001-001",
        "MTR-PLANT-001-001",
        "MTR-PLANT-001-002",
        "MTR-PLANT-001-002"
    ],
    "Energy_kWh": [5.0, 4.5, -2.0, 3.0]
}

df = pd.DataFrame(data)

# Collect validation problems
issues = []

for index, row in df.iterrows():

    if pd.isna(row["Reading_ID"]) or row["Reading_ID"] == "":
        issues.append({
            "Row": index + 1,
            "Reading_ID": "",
            "Problem": "Missing reading ID"
        })

    if row["Energy_kWh"] < 0:
        issues.append({
            "Row": index + 1,
            "Reading_ID": row["Reading_ID"],
            "Problem": "Negative energy"
        })

# Find duplicate reading IDs
duplicates = df[df.duplicated("Reading_ID", keep=False)]

for index, row in duplicates.iterrows():
    issues.append({
        "Row": index + 1,
        "Reading_ID": row["Reading_ID"],
        "Problem": "Duplicate reading ID"
    })

# Convert issues into a DataFrame
report = pd.DataFrame(
    issues,
    columns=["Row", "Reading_ID", "Problem"]
)

# Create output folder
output_folder = Path("data") / "processed"
output_folder.mkdir(parents=True, exist_ok=True)

# Save report
output_file = output_folder / "validation_report.csv"
report.to_csv(output_file, index=False)

print("Validation Report")
print(report.to_string(index=False))

print("\nTotal issues found:", len(report))
print("Report saved to:", output_file.resolve())
