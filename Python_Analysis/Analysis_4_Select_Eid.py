import pandas as pd

### Step 1: Load the Feather File ###
df = pd.read_feather("Round_2_Data/ukb27307.subset7.feather")

# Display general information
print("\nOriginal DataFrame Info:")
print(df.info())

### Step 2: Load Column Names to Keep from a Text File ###
columns_file = "Round_2_Data/ukb27307.subset7.colnames.txt"  # Change this to your actual file path

# Read the text file and extract column names
with open(columns_file, "r") as file:
    all_columns = file.read().splitlines()

# Display all available columns for selection
print("\nAvailable Columns in File:")
for i, col in enumerate(all_columns):
    print(f"{i}: {col}")

# Manually select row numbers (excluding header row at index 0)
selected_rows = input("\n1 - 25): ")
selected_indices = [int(i) for i in selected_rows.split(",")]

# Extract selected column names
columns_to_keep = [all_columns[i] for i in selected_indices]

# Ensure 'eid' is always included
columns_to_keep.insert(0, "eid")

# Filter DataFrame to keep only selected columns
df = df[columns_to_keep]

print(f"\nFiltered DataFrame contains {len(columns_to_keep)} columns.")

### Step 3: Load Case-Control Labels ###
case_control_file = "GRIN2A_combined.txt"  # Change to actual file path

# Read the case-control text file
case_control_df = pd.read_csv(case_control_file, sep="\s+", usecols=["eid", "label"], dtype=str)

# Convert 'eid' to string for consistency
df["eid"] = df["eid"].astype(str)
case_control_df["eid"] = case_control_df["eid"].astype(str)

# Merge case-control labels into DataFrame
df = df.merge(case_control_df, on="eid", how="left")

# Assign "others" to rows not found in the case-control file
df["label"] = df["label"].fillna("others")

print("\nUpdated DataFrame with case/control/others assigned:")
print(df["label"].value_counts())

### Step 4: Process Each Feature Column Separately ###
# Exclude 'eid' and 'label' from feature selection
feature_columns = [col for col in df.columns if col not in ["eid", "label"]]

for feature in feature_columns:
    # Select rows where the feature column is NOT NaN or None
    feature_df = df.dropna(subset=[feature])

    # Save separate CSV and DataFrame
    feature_df.to_csv(f"filtered_{feature}.csv", index=False)
    feature_df.to_feather(f"filtered_{feature}.feather")

    print(f"Saved: filtered_{feature}.csv & filtered_{feature}.feather")

print("\nAll filtered datasets have been saved.")
