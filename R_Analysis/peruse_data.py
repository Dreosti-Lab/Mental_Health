import pandas as pd

# Specify feather path
#feather_path = "ukb27307.subset5.feather"
#feather_path = "Round_2_Data/ukb27307.subset1.feather"
feather_path = "Round_2_Data/ukb27307.subset7.feather"

# Load the Feather file
df = pd.read_feather(feather_path)

# Display general information about the DataFrame
print(df.info())

# Show the first 5 rows
print(df.head())

# Show the number of rows and columns
print(f"\nShape of the dataset: {df.shape}")  # (rows, columns)

# List all column names (categories)
categories = df.columns.tolist()

# Look for imaging data
imaging_strings = ["T1", "freesurf", "brain", "volume"]
for category in categories:
    if any(substring in category for substring in imaging_strings):  # Check for partial match
        print(category)

#FIN