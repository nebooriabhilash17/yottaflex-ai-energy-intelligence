
import pandas as pd

# Factory information
plants = {
    "Plant_ID": ["PLANT-001"],
    "Plant_Name": ["Hyderabad Factory"],
    "Location": ["Hyderabad"],
    "Timezone": ["Asia/Kolkata"],
    "Status": ["ACTIVE"]
}

# Convert factory information into a table
df = pd.DataFrame(plants)

# Display the plant table
print(df)
