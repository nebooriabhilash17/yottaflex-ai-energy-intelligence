
import pandas as pd

# Production output recorded for each machine
production = {
    "Batch_ID": [
        "BATCH-2026-000001",
        "BATCH-2026-000002",
        "BATCH-2026-000003"
    ],
    "Machine_ID": [
        "MAC-001",
        "MAC-002",
        "MAC-003"
    ],
    "Production_Quantity": [100, 0, 150],
    "Production_Status": [
        "COMPLETED",
        "IDLE",
        "COMPLETED"
    ]
}

df = pd.DataFrame(production)

print("Production Data")
print(df)
