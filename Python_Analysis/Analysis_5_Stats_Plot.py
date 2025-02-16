import pandas as pd
import scipy.stats as stats
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Load the Feather file
df = pd.read_feather("filtered_volume_of_brain_stem_4th_ventricle_f25025_2_0.feather")

# Display basic info
print("\nLoaded DataFrame Info:")
print(df.info())

# Ensure 'label' column exists
if "label" not in df.columns:
    raise ValueError("Error: Column 'label' not found in dataset.")

# Get feature columns (exclude 'eid' and 'label')
feature_columns = [col for col in df.columns if col not in ["eid", "label"]]

# Create directories to save results
os.makedirs("stats_results", exist_ok=True)
os.makedirs("boxplots", exist_ok=True)

# Open a file to store statistical results
stats_file = open("stats_results/statistical_comparison.txt", "w")
stats_file.write("Statistical Comparison of Case and Control\n\n")

for feature in feature_columns:
    print(f"\nProcessing Feature: {feature}")

    # Convert feature column to numeric
    df[feature] = pd.to_numeric(df[feature], errors='coerce')

    # Remove NaN values
    feature_df = df.dropna(subset=[feature])

    # Get only cases and controls (ignore "others")
    case_group = feature_df[feature_df["label"] == "case"][feature]
    control_group = feature_df[feature_df["label"] == "control"][feature]

    # Get sample sizes
    num_cases = len(case_group)
    num_controls = len(control_group)

    # Print sample sizes
    print(f"Cases: {num_cases}, Controls: {num_controls}")

    # Skip if there are not enough samples for both groups
    if num_cases == 0 or num_controls == 0:
        print(f"Skipping {feature} due to missing case or control data.")
        continue

    # Normality tests
    normal_test_case = stats.shapiro(case_group) if num_cases < 5000 else stats.kstest(case_group, 'norm')
    normal_test_control = stats.shapiro(control_group) if num_controls < 5000 else stats.kstest(control_group, 'norm')

    print("\nNormality Test Results:")
    print(f"Case Group p-value: {normal_test_case.pvalue}")
    print(f"Control Group p-value: {normal_test_control.pvalue}")

    # Decide statistical test (ignore 'others' group)
    if normal_test_case.pvalue > 0.05 and normal_test_control.pvalue > 0.05:
        print("\nUsing T-Test (parametric test)")
        stat_test = stats.ttest_ind(case_group, control_group, equal_var=False)
        test_name = "T-Test"
    else:
        print("\nUsing Mann-Whitney U Test (non-parametric test)")
        stat_test = stats.mannwhitneyu(case_group, control_group, alternative='two-sided')
        test_name = "Mann-Whitney U Test"

    # Print test results
    print("\nStatistical Test Results:")
    print(f"Test: {test_name}")
    print(f"Statistic: {stat_test.statistic}")
    print(f"P-value: {stat_test.pvalue}")

    # Save results to file
    stats_file.write(f"Feature: {feature}\n")
    stats_file.write(f"Test: {test_name}\n")
    stats_file.write(f"Statistic: {stat_test.statistic}\n")
    stats_file.write(f"P-value: {stat_test.pvalue}\n")
    stats_file.write(f"Cases: {num_cases}, Controls: {num_controls}\n")
    stats_file.write("=" * 50 + "\n")

    # Generate a boxplot for all features
    plt.figure(figsize=(8, 6))
    sns.boxplot(x=feature_df["label"], y=feature_df[feature], palette=["red", "blue", "gray"])

    # Title and labels
    plt.title(f"Comparison of {feature} Between Groups")
    plt.xlabel("Group")
    plt.ylabel(feature)
    plt.grid(True)

    # Annotate sample sizes
    plt.figtext(0.15, 0.85, f"Cases: {num_cases} | Controls: {num_controls}", fontsize=12, color="black", weight="bold")

    # Annotate the statistical test results
    plt.figtext(0.15, 0.80, f"{test_name}: p = {stat_test.pvalue:.4f}", fontsize=12, color="black")

    # Highlight significance if p-value < 0.05
    if stat_test.pvalue < 0.05:
        plt.figtext(0.15, 0.75, "**Significant Difference Cases-Controls (p < 0.05)**", 
                    fontsize=12, color="red", weight="bold")
    else:
        plt.figtext(0.15, 0.75, "No Significant Difference Cases-Controls", fontsize=12, color="black")

    # Save the plot
    plt.savefig(f"boxplots/{feature}_boxplot.png")

    # Show the plot on screen
    plt.show()

    # Close the plot to prevent overlapping figures
    plt.close()

    print(f"Saved: boxplots/{feature}_boxplot.png")

# Close the stats file
stats_file.close()

print("\nAll analyses completed. Check 'stats_results/' for statistical outputs and 'boxplots/' for saved plots.")
