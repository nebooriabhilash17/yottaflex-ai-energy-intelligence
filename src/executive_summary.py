
import pandas as pd
from pathlib import Path

# --------------------------------------------------
# 1. Set project folders
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"

# --------------------------------------------------
# 2. Load reports
# --------------------------------------------------
report = pd.read_csv(
    DATA_DIR / "integrated_yottaflex_report.csv"
)

batches = pd.read_csv(
    DATA_DIR / "batch_anomaly_results.csv"
)

daily = pd.read_csv(
    DATA_DIR / "daily_anomaly_results.csv"
)

# --------------------------------------------------
# 3. Calculate project summary metrics
# --------------------------------------------------
total_machines = report["Machine_ID"].nunique()

flagged_batches = batches[
    batches["Anomaly_Status"].astype(str).str.strip().str.upper()
    == "INVESTIGATE"
]

total_flagged_batches = len(flagged_batches)

unusual_days = daily.loc[
    daily["Anomaly_Status"].astype(str).str.strip().str.upper()
    == "UNUSUAL CONSUMPTION",
    "Date"
].nunique()

flagged_energy_kwh = flagged_batches["Matched_Energy_kWh"].sum()

# Existing estimate: flat assumed rate
assumed_rate = 7.0
flagged_cost_estimate_rs = flagged_energy_kwh * assumed_rate

# Actual time-based tariff costs from the integrated report
actual_tariff_cost_rs = report[
    "Total_Electricity_Cost_Rs"
].sum()

# Machine efficiency summary
high_intensity_machines = (
    report.loc[
        report["Efficiency_Status"] == "HIGH ENERGY INTENSITY",
        "Machine_ID"
    ].nunique()
)

# --------------------------------------------------
# 4. Prepare top-priority machines
# --------------------------------------------------
top_machines = report[
    [
        "Priority_Rank",
        "Machine_ID",
        "Efficiency_Status",
        "Flagged_Batch_Count",
        "Estimated_Cost_Rs",
        "Total_Electricity_Cost_Rs",
        "Cost_Rank",
    ]
].head(5)

# --------------------------------------------------
# 5. Create executive summary
# --------------------------------------------------
summary = f"""
YOTTAFLEX AI
INDUSTRIAL ENERGY MONITORING - EXECUTIVE SUMMARY
================================================

PROJECT OVERVIEW
----------------
Machines analyzed: {total_machines}
Production batches requiring investigation: {total_flagged_batches}
Days with unusual energy consumption: {unusual_days}
Machines classified as high energy intensity: {high_intensity_machines}

ELECTRICITY COST ANALYSIS
-------------------------
Total tariff-based machine electricity cost: Rs {actual_tariff_cost_rs:,.2f}
Energy associated with flagged batches: {flagged_energy_kwh:,.2f} kWh
Estimated flagged-batch cost at assumed Rs {assumed_rate:.2f}/kWh:
Rs {flagged_cost_estimate_rs:,.2f}

TOP 5 MACHINES REQUIRING INVESTIGATION
-------------------------------------
{top_machines.to_string(index=False)}

IMPORTANT INTERPRETATION
------------------------
The results are generated from synthetic project data.
Anomaly flags identify records for investigation; they do not
prove that energy was wasted.

Total electricity cost uses the time-based synthetic tariff schedule.
Flagged-batch cost uses an assumed rate of Rs 7/kWh.
Flagged-batch costs are not confirmed avoidable costs or savings.
High energy intensity is a screening indicator, not proof of a fault.
Real-world use would require validated meter, production, and tariff data.
"""

# --------------------------------------------------
# 6. Save summary
# --------------------------------------------------
output_file = DATA_DIR / "yottaflex_executive_summary.txt"

output_file.write_text(
    summary.strip() + "\n",
    encoding="utf-8"
)

print(summary)
print(f"\nExecutive summary saved to: {output_file}")
