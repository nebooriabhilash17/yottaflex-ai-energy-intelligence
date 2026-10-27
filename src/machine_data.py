
import pandas as pd

# Create factory machine data
machines = {
    "Machine_ID": ["MAC-001", "MAC-002", "MAC-003"],
    "Machine_Name": [
        "Cutting Machine",
        "Drilling Machine",
        "Packaging Machine"
    ],
    "Power_kW": [20, 15, 10],
    "Status": ["RUNNING", "IDLE", "RUNNING"]
}

# Convert the data into a table
df = pd.DataFrame(machines)

# Display the table
print(df)
