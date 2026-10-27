
import pandas as pd

# Sample machine energy and production data
data = {
    "Machine_ID": ["MAC-001", "MAC-002", "MAC-003", "MAC-004"],
    "Machine_Name": [
        "Cutting Machine",
        "Drilling Machine",
        "Packaging Machine",
        "Welding Machine"
    ],
    "Energy_kWh": [5.0, 4.0, 2.5, 3.0],
    "Production_Quantity": [100, 0, 150, 0],
    "Machine_Status": ["RUNNING", "IDLE", "RUNNING", "IDLE"]
}

df = pd.DataFrame(data)

# Flag machines using electricity without production
df["Potential_Waste"] = (
    (df["Energy_kWh"] > 0) &
    (df["Production_Quantity"] == 0)
)

print("Energy Waste Detection Results")
print(df.to_string(index=False))

print("\nMachines requiring investigation:")
print(df[df["Potential_Waste"] == True][
    ["Machine_ID", "Machine_Name", "Energy_kWh"]
].to_string(index=False))
