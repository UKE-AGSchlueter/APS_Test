#!/usr/bin/env python3\
# -*- coding: utf-8 -*-\
"""
Created on Mon Jun  5 14:19:04 2023

@author: bentesiebels
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os
import sys
from pandas.api.types import is_numeric_dtype


'''
Read the input data with Column Peptides and the samples. The two groups are 
named 1_ and 2_ in front of the column title. Complete data matrix required, 
log2 transformed values. No normalisation should be applied as this can lead to
biased values.
'''
#update you file paths here
try:
  data = pd.read_excel('C:/Users/agock/Desktop/Eppendorf_LB.xlsx')
except IOError as err:
  sys.stderr.write ( '{}\n'. format(err)) 

def calculate_gravy_number(peptide):
    # Calculate GRAVY (grand average of hydropathy) number
    aa_gravy = {'A': 1.8, 'C': 2.5, 'D': -3.5, 'E': -3.5, 'F': 2.8, 'G': -0.4,
                'H': -3.2, 'I': 4.5, 'K': -3.9, 'L': 3.8, 'M': 1.9, 'N': -3.5,
                'P': -1.6, 'Q': -3.5, 'R': -4.5, 'S': -0.8, 'T': -0.7,
                'V': 4.2, 'W': -0.9, 'Y': -1.3}
    gravy_sum = sum(aa_gravy.get(aa, 0) for aa in peptide)
    return gravy_sum / len(peptide)

def calculate_charge(peptide, ph=2.7):
    # Calculate charge at pH 2.7
    aa_charge = {'A': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0,
                 'H': 1, 'I': 0, 'K': 1, 'L': 0, 'M': 0, 'N': 0,
                 'P': 0, 'Q': 0, 'R': 1, 'S': 0, 'T': 0, 'V': 0,
                 'W': 0, 'Y': 0}
    charge = sum(aa_charge.get(aa, 0) for aa in peptide) + 1 #For N-terminus
    return charge

file_path = "C:/Users/agock/Desktop/"
directory = os.path.dirname(file_path)

# Separate the groups
group_1_columns = [col for col in data.columns if col.startswith("1_")]
group_2_columns = [col for col in data.columns if col.startswith("2_")]

if not is_numeric_dtype(group_1_columns) & is_numeric_dtype(group_2_columns):
    sys.stderr.write('Input data frame contains non-numeric values \n') 
# Extract peptides
peptides = data["Peptides"]

# Perform Welch's T-test and calculate log2 difference
p_values = []
log2_diffs = []
for peptide in peptides:
    group_1_values = data.loc[data["Peptides"] == peptide, group_1_columns].values.flatten()
    group_2_values = data.loc[data["Peptides"] == peptide, group_2_columns].values.flatten()
    t_stat, p_value = stats.ttest_ind(group_1_values, group_2_values, equal_var=False)
    log2_diff = np.mean(group_2_values) - np.mean(group_1_values)
    p_values.append(p_value)
    log2_diffs.append(log2_diff)

# Create a DataFrame with results
results = pd.DataFrame({"Peptides": peptides, "p-value": p_values, "log2 difference": log2_diffs})

# Separate the results into "Adsorbed" and "Not_Adsorbed" groups
adsorbed_results = results[(results["p-value"] < 0.05) & (results["log2 difference"] <= -1)]
not_adsorbed_results = results[(results["p-value"] > 0.05) & (results["log2 difference"] <= 1)]

# Calculate peptide length, GRAVY number, and charge
peptide_lengths = peptides.str.len()
peptide_gravy = peptides.apply(calculate_gravy_number)
peptide_charges = peptides.apply(calculate_charge)

results_df = pd.DataFrame({
    'Peptide': peptides,
    'p-value': p_values,
    'log2 difference': log2_diffs,
    'Status': ['Adsorbed' if i in adsorbed_results.index else 'Not Adsorbed' for i in range(len(peptides))],
    'GRAVY': peptide_gravy,
    'Length': peptide_lengths,
    'Charge State': peptide_charges
})
    
# Save the DataFrame as an Excel file
output_file_path_excel = os.path.join(directory, 'APS_Test_Results.xlsx')
results_df.to_excel(output_file_path_excel, index=False)
print(f"Results saved to: {output_file_path_excel}")

# Plotting
plt.figure(figsize=(12, 10))
# Add figure title
plt.suptitle("APS Test Results", fontsize=16)

# Calculate the number of adsorbed peptides
adsorbed_blue_count = adsorbed_results.shape[0]
# Volcano plot with number of adsorbed peptides
plt.subplot(2, 2, 1)
plt.scatter(results['log2 difference'], -np.log10(results['p-value']), color='gray', alpha=0.5)
plt.scatter(adsorbed_results['log2 difference'], -np.log10(adsorbed_results['p-value']), color='blue', label=f'Adsorbed ({adsorbed_blue_count})')
plt.title("Adsorbed Peptides")
plt.xlabel('log2 difference')
plt.ylabel('-log10(p-value)')
plt.legend()
# Add threshold lines
plt.axvline(x=-1, color='black', linestyle='--')
plt.axvline(x=1, color='black', linestyle='--')
plt.axhline(y=-np.log10(0.05), color='black', linestyle='--')

# Separate GRAVY numbers for adsorbed and not adsorbed peptides
adsorbed_gravy = peptide_gravy.loc[adsorbed_results.index].tolist()
not_adsorbed_gravy = peptide_gravy.loc[not_adsorbed_results.index].tolist()

# Create a violin plot for GRAVY numbers
plt.subplot(2, 2, 2)
sns.violinplot(data=[adsorbed_gravy, not_adsorbed_gravy], palette=['blue', 'gray'])
plt.title("GRAVY Numbers")
plt.ylabel("GRAVY")
plt.xticks([0, 1], ['Adsorbed', 'Not Adsorbed'])

# Print mean values
plt.text(0, -4.6, "Mean: {:.2f}".format(np.mean(adsorbed_gravy)), ha='center', va='top', color='black')
plt.text(1, -4.6, "Mean: {:.2f}".format(np.mean(not_adsorbed_gravy)), ha='center', va='top', color='black')

# Adjust plot limits
plt.ylim(-4, 4)

# Count the number of occurrences for each peptide length in adsorbed and not adsorbed peptides\
adsorbed_length_counts = peptide_lengths.loc[adsorbed_results.index].value_counts()
not_adsorbed_length_counts = peptide_lengths.loc[not_adsorbed_results.index].value_counts()

# Get all unique peptide lengths
unique_lengths = sorted(set(peptide_lengths).union(set(adsorbed_length_counts.index)).union(set(not_adsorbed_length_counts.index)))

# Fill missing peptide lengths with 0 count
adsorbed_length_counts = adsorbed_length_counts.reindex(unique_lengths, fill_value=0)
not_adsorbed_length_counts = not_adsorbed_length_counts.reindex(unique_lengths, fill_value=0)

# Calculate the percentage of peptide lengths within each group
adsorbed_length_percentages = adsorbed_length_counts / adsorbed_length_counts.sum() * 100
not_adsorbed_length_percentages = not_adsorbed_length_counts / not_adsorbed_length_counts.sum() * 100

# Create a bar plot for peptide lengths
plt.subplot(2, 2, 3)
plt.bar(np.arange(len(unique_lengths)), adsorbed_length_percentages, color='blue', label='Adsorbed')
plt.bar(np.arange(len(unique_lengths)) + 0.3, not_adsorbed_length_percentages, color='gray', label='Not Adsorbed', alpha=0.7)
plt.title("Peptide Length Occurrence")
plt.xlabel("Peptide Length")
plt.ylabel("Percentage of Peptides")
plt.xticks(np.arange(len(unique_lengths)), unique_lengths, fontsize=8)  # Adjust fontsize here
plt.legend()

# Count the number of occurrences for each peptide charge state in adsorbed and not adsorbed peptides
adsorbed_charge_counts = peptide_charges.loc[adsorbed_results.index].value_counts()
not_adsorbed_charge_counts = peptide_charges.loc[not_adsorbed_results.index].value_counts()

# Get all unique charge states
unique_charge_states = np.arange(2, 6)

# Fill missing charge states with 0 count
adsorbed_charge_counts = adsorbed_charge_counts.reindex(unique_charge_states, fill_value=0)
not_adsorbed_charge_counts = not_adsorbed_charge_counts.reindex(unique_charge_states, fill_value=0)

# Calculate the percentage of charge states within each group
adsorbed_charge_percentages = adsorbed_charge_counts / adsorbed_charge_counts.sum() * 100
not_adsorbed_charge_percentages = not_adsorbed_charge_counts / not_adsorbed_charge_counts.sum() * 100

# Set the width of each bar
bar_width = 0.4

# Create a bar plot for charge states
plt.subplot(2, 2, 4)
plt.bar(unique_charge_states + bar_width/2, adsorbed_charge_percentages, width=bar_width, color='blue', label='Adsorbed')
plt.bar(unique_charge_states - bar_width/2, not_adsorbed_charge_percentages, width=bar_width, color='gray', label='Not Adsorbed', alpha=0.7)
plt.title("Peptide Charge State Occurrence")
plt.xlabel("Charge State [H+]")
plt.ylabel("Percentage of Peptides")
plt.xticks(unique_charge_states)
plt.legend()
plt.tight_layout()
plt.show()

# Save the plot as a PDF in the same directory as results_df
output_file_path_pdf = os.path.join(directory, 'APS_Test_Results_Plot.pdf')
plt.savefig(output_file_path_pdf, format='pdf')

print(f"Plot saved as {output_file_path_pdf}")


