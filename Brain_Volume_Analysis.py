
# -*- coding: utf-8 -*-
"""
Compare the volumnes of 5 different brain areas between cases and controls

@author: Elena Dreosti 7.Feb.2025
"""

## This script compares the volumenof 5 different brain areas between cases and controls
## It loads a text files

# Load environment file and variables
import os
from dotenv import load_dotenv
load_dotenv()
libs_path = os.getenv('LIBS_PATH') + "/../Behaviour/ED/libs"
base_path = os.getenv('BASE_PATH')



import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind, mannwhitneyu, shapiro

# Load data, skipping the first row
# file_path = "your_file.txt"

file_path = base_path + r'XPO7/XPO7.txt'
# file_path = base_path + r'GRIN2A/GRIN2A.txt'

file_name = os.path.basename(file_path).replace(".txt", "")

# Get the folder path where the file is located
output_folder = os.path.dirname(file_path)

columns = ["eid", "group", 
           "volume_of_peripheral_cortical_grey_matter", 
           "volume_of_ventricular_cerebrospinal_fluid",
           "volume_of_grey_matter", 
           "volume_of_white_matter", 
           "volume_of_brain_greywhite_matter"]

df = pd.read_csv(file_path, sep='\s+', skiprows=1, names=columns, na_values="NA")  # FIXED WARNING

# Drop rows where all volume columns are NaN
df = df.dropna(subset=columns[2:], how="all")

# Convert volume columns to numeric
for col in columns[2:]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Split into cases and controls
cases = df[df["group"] == "case"]
controls = df[df["group"] == "control"]

# Ensure DataFrames are not empty before saving
if not cases.empty:
    cases.to_csv(os.path.join(output_folder, "cases.csv"), index=False)

if not controls.empty:
    controls.to_csv(os.path.join(output_folder, "controls.csv"), index=False)

# Perform statistical tests for each volume column
results = []
for col in columns[2:]:
    case_values = cases[col].dropna()
    control_values = controls[col].dropna()

    if case_values.empty or control_values.empty:
        continue  # Skip columns with only NaN values

    # Check for normality
    stat_case, p_case = shapiro(case_values) if len(case_values) > 3 else (None, None)
    stat_control, p_control = shapiro(control_values) if len(control_values) > 3 else (None, None)

    normal = (p_case and p_case > 0.05) and (p_control and p_control > 0.05)

    if normal:
        stat, p = ttest_ind(case_values, control_values, equal_var=False)
        test_name = "T-test"
    else:
        stat, p = mannwhitneyu(case_values, control_values, alternative="two-sided")
        test_name = "Mann-Whitney U test"

    results.append((col, test_name, stat, p))

# Convert results to DataFrame
stats_df = pd.DataFrame(results, columns=["Brain Area", "Test", "Statistic", "P-value"])

# Save statistics to a text file
stats_file_path = os.path.join(output_folder, "statistical_results.txt")
with open(stats_file_path, "w") as f:
    f.write("Statistical Analysis of Brain Volume Differences\n")
    f.write("="*50 + "\n")
    f.write(stats_df.to_string() + "\n\n")

    significant_results = stats_df[stats_df["P-value"] < 0.05]
    if significant_results.empty:
        f.write("No significant differences were found (p < 0.05).\n")
    else:
        f.write("Significant differences found:\n")
        f.write(significant_results.to_string())

print(f"Statistical results saved in: {stats_file_path}")

# Set Seaborn style for better visuals
sns.set(style="whitegrid")

# **Plot Separate Boxplots for Each Brain Area**
for col in columns[2:]:
    plt.figure(figsize=(10, 6))  # Bigger figure for readability
    
    # Check if there are valid values before plotting
    if df[col].dropna().empty:
        print(f"Skipping {col}, as it has only NaN values.")
        continue

    sns.boxplot(x="group", y=col, hue="group", data=df, palette="coolwarm", dodge=False)
    plt.title(f"Comparison of {col} between Cases and Controls")
    plt.xlabel("Group")
    plt.ylabel("Volume")
    plt.xticks(rotation=30, ha="right")  # Ensures readability
    plt.legend(title="Group", loc="best")
    plt.tight_layout()  # Prevents clipping
    plt.show()

# **Plot Combined Graph for All Brain Areas**
df_melted = df.melt(id_vars=["group"], value_vars=columns[2:], var_name="Brain Area", value_name="Volume")

if not df_melted["Volume"].dropna().empty:  # Ensure valid data before plotting
    plt.figure(figsize=(12, 6))
    sns.boxplot(x="Brain Area", y="Volume", hue="group", data=df_melted, palette="coolwarm")

    plt.title("Comparison of Brain Volumes Across All Areas")
    plt.title(f"{file_name} - {col} Comparison")  
    plt.xlabel("Brain Area")
    plt.ylabel("Volume")
    plt.xticks(rotation=20, ha="right", wrap=True)
    plt.legend(title="Group", loc="best")
    plt.tight_layout()

    combined_plot_path = os.path.join(output_folder, "brain_volume_comparison.pdf")
    plt.savefig(combined_plot_path, format="pdf")

    print(f"Combined figure saved as: {combined_plot_path}")

    plt.show()
