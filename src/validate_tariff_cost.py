
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

energy = pd.read_csv(RAW_DIR / "energy_readings.csv")
tariffs = pd.read_csv(RAW_DIR / "tariffs.csv")
summary = pd.read_csv(PROCESSED_DIR / "tariff_cost_analysis.csv")

checks = []

checks.append((
    "All 172,800 energy readings are priced",
    summary["Reading_Count"].sum() == len(energy)
))

checks.append((
    "Tariff IDs exist in the tariff schedule",
    summary["Tariff_ID"].isin(tariffs["Tariff_ID"]).all()
))

checks.append((
    "Energy values are non-negative",
    (summary["Total_Energy_kWh"] >= 0).all()
))

checks.append((
    "Costs are non-negative",
    (summary["Total_Cost_Rs"] >= 0).all()
))

expected_cost = (
    summary["Total_Energy_kWh"] * summary["Price_Per_kWh"]
)

checks.append((
    "Reported costs match energy multiplied by tariff",
    (summary["Total_Cost_Rs"] - expected_cost).abs().max() <= 0.06
))

checks.append((
    "Each meter and tariff combination is unique",
    not summary.duplicated(
        ["Meter_ID", "Tariff_ID"]
    ).any()
))

print("YottaFlex AI - Tariff Cost Validation")
print("-" * 45)

for name, passed in checks:
    print(f"{'PASSED' if passed else 'FAILED'}: {name}")

print(f"\nTotal checks: {len(checks)}")
print(f"Passed: {sum(p for _, p in checks)}")
print(f"Failed: {sum(not p for _, p in checks)}")
