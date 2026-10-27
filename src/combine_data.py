
import pandas as pd

# Machine information
machines = {
    "Machine_ID": ["MAC-001", "MAC-002", "MAC-003"],
    "Machine_Name": [
        "Cutting Machine",
        "Drilling Machine",
        "Packaging Machine"
    ],
    "Power_kW": [20, 15, 10]
}

machine_df = pd.DataFrame(machines)

# Production information
production = {
    "Batch_ID": [
        "BATCH-2026-000001",
        "BATCH-2026-000002",
        "BATCH-2026-000003"
    ],
    "Machine_ID": ["MAC-001", "MAC-002", "MAC-003"],
    "Production_Quantity": [100, 0, 150]
}

production_df = pd.DataFrame(production)

# Combine both datasets using Machine_ID
combined_df = pd.merge(
    machine_df,
    production_df,
    on="Machine_ID",
    how="left"
)

print("Combined Machine and Production Data")
print(combined_df)
