
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"
RAW_DIR = BASE_DIR / "data" / "raw"

report = pd.read_csv(DATA_DIR / "machine_tariff_costs.csv")
energy = pd.read_csv(RAW_DIR / "energy_readings.csv")
meters = pd.read_csv(RAW_DIR / "meters.csv")

checks = []

checks.append((
    "All 20 machines are included",
    report["Machine_ID"].nunique() == 20
))

checks.append((
    "Machine IDs are unique",
    report["Machine_ID"].is_unique
))

checks.append((
    "All 172,800 readings are accounted for",
    report["Reading_Count"].sum() == len(energy)
))

checks.append((
    "All machine IDs exist in the meter mapping",
    report["Machine_ID"].isin(meters["Machine_ID"]).all()
))

checks.append((
    "Energy totals are non-negative",
    (report["Total_Energy_kWh"] >= 0).all()
))

checks.append((
    "Electricity costs are non-negative",
    (report["Total_Electricity_Cost_Rs"] >= 0).all()
))

checks.append((
    "Cost ranking is in descending order",
    report["Total_Electricity_Cost_Rs"].is_monotonic_decreasing
))

checks.append((
    "Total machine costs match the tariff report",
    abs(
        report["Total_Electricity_Cost_Rs"].sum()
        - pd.read_csv(DATA_DIR / "tariff_cost_analysis.csv")["Total_Cost_Rs"].sum()
    ) < 0.25
))

print("YottaFlex AI - Machine Tariff Cost Validation")
print("-" * 50)

for name, passed in checks:
    print(f"{'PASSED' if passed else 'FAILED'}: {name}")

print(f"\nTotal checks: {len(checks)}")
print(f"Passed: {sum(p for _, p in checks)}")
print(f"Failed: {sum(not p for _, p in checks)}")
