
import pandas as pd
import numpy as np
from pathlib import Path

# Reproducible synthetic production data
SEED = 20261022
rng = np.random.default_rng(SEED)

MACHINE_COUNT = 20
START_DATE = pd.Timestamp("2026-07-25")
DAYS = 90

batches = []
batch_number = 1

for machine_number in range(1, MACHINE_COUNT + 1):
    machine_id = f"MAC-{machine_number:03d}"

    for day in range(DAYS):
        current_date = START_DATE + pd.Timedelta(days=day)

        # Two sample production shifts per day
        for shift_start_hour, shift_end_hour in [(6, 14), (14, 22)]:

            # Some shifts produce nothing
            if rng.random() < 0.10:
                continue

            start_time = current_date + pd.Timedelta(
                hours=shift_start_hour
            )
            end_time = current_date + pd.Timedelta(
                hours=shift_end_hour
            )

            quantity = int(rng.integers(50, 201))

            batches.append({
                "Batch_ID": f"BATCH-2026-{batch_number:06d}",
                "Machine_ID": machine_id,
                "Start_Time": start_time,
                "End_Time": end_time,
                "Production_Quantity": quantity,
                "Status": "COMPLETED"
            })

            batch_number += 1

production_df = pd.DataFrame(batches)

# Save production data
output_folder = Path("data") / "raw"
output_folder.mkdir(parents=True, exist_ok=True)

output_file = output_folder / "production_batches.csv"
production_df.to_csv(output_file, index=False)

print("Production data generated successfully!")
print("Machines:", MACHINE_COUNT)
print("Days:", DAYS)
print("Production batches:", len(production_df))
print("\nFirst five batches:")
print(production_df.head().to_string(index=False))
print("\nSaved to:", output_file.resolve())
