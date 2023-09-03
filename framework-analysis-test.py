from imbalance import Imbalance
from quality import Quality
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
# Set the maximum number of rows and columns to display
pd.set_option('display.max_rows', None)  # Display all rows
pd.set_option('display.max_columns', None)  # Display all columns

# data_source = 'data/1_adult.data'
# output_name = '1_Adult'
# pretty_name = 'Adult'
# dataset = pd.read_csv(data_source, sep=',',
#                       names=['age', 'workclass', 'fnlwgt', 'education', 'education-num', 'marital-status',
#                              'occupation', 'relationship', 'race', 'sex', 'capital-gain', 'capital-loss',
#                              'hours-per-week', 'native-country', 'income'],
#                       dtype={'age': np.int64, 'workclass': str, 'fnlwgt': np.int64, 'education': str,
#                              'education-num': np.int64, 'marital-status': str, 'occupation': str,
#                              'relationship': str, 'race': str, 'sex': str, 'capital-gain': np.int64,
#                              'capital-loss': np.int64, 'hours-per-week': np.int64, 'native-country': str,
#                              'income': str}, na_values='?', encoding='utf-8')  #
# sensitive_features = ['sex', 'race', 'education', 'marital-status', 'native-country', 'income']
# Imbalance(f'{output_name}_DB', dataset, sensitive_features, output_path="analysis/")
# Quality(f'{output_name}_DQ', data_source, "analysis/", isurl=False, pretty_name=pretty_name)
#
# data_source = 'data/2_compas-scores-raw.csv'
# output_name = '2_COMPAS'
# pretty_name = 'COMPAS'
# sensitive_features = ['Sex_Code_Text', 'Ethnic_Code_Text', 'Language', 'MaritalStatus', 'DecileScore']
# dataset = pd.read_csv(data_source, header=0, sep=',')
# Imbalance(f'{output_name}_DB', dataset, sensitive_features, output_path="analysis/")
# Quality(f'{output_name}_DQ', data_source, "analysis/", isurl=False, pretty_name=pretty_name)
#
# data_source = "data/3_SouthGermanCredit.asc"
# output_name = '3_SouthGermanCredit'
# pretty_name = 'South German Credit'
# sensitive_features = ['gastarb', 'laufkont', 'famges', 'beruf', 'verm', 'kredit']
# dataset = pd.read_csv(data_source, header=0, sep=" ")
# Imbalance(f'{output_name}_DB', dataset, sensitive_features, output_path="analysis/")
# Quality(f'{output_name}_DQ', data_source, "analysis/", isurl=False, pretty_name=pretty_name)
#
# data_source = 'data/4_communities.data'
# output_name = '4_CommunitiesAndCrime'
# pretty_name = 'Communities And Crime'
# Quality(f'{output_name}_DQ', data_source, "analysis/", isurl=False, pretty_name=pretty_name)
#
# data_source = "data/5_bank-additional-full.csv"
# output_name = '5_BankMarketing'
# pretty_name = 'Bank Marketing'
# sensitive_features = ['job', 'education', 'marital', 'y']
# dataset = pd.read_csv(data_source, sep=";", na_values=['unknown'])
# Imbalance(f'{output_name}_DB', dataset, sensitive_features, output_path="analysis/")
# Quality(f'{output_name}_DQ', data_source, "analysis/", isurl=False, pretty_name=pretty_name)
#
# data_source = "data/6_LawSchool_bar_pass_prediction.csv"
# output_name = '6_LawSchool'
# pretty_name = 'Law School'
# sensitive_features = ['gender', 'race1', 'lsat', 'ugpa', 'pass_bar']
# dataset = pd.read_csv(data_source, header=0)
# Imbalance(f'{output_name}_DB', dataset, sensitive_features, output_path="analysis/")
# Quality(f'{output_name}_DQ', data_source, "analysis/", isurl=False, pretty_name=pretty_name)
#
# output_name = '8_MovieLens'
# pretty_name = 'MovieLens'
# sensitive_features = ['Gender', 'Occupation', 'Zip-code']
# datasetRatings = pd.read_csv("data/8_ratings.dat", header=None,
#                              names=['UserID', 'MovieID', 'Rating', 'Timestamp'], sep='::', engine='python',
#                              encoding='latin-1')
# datasetUser = pd.read_csv("data/8_users.dat", header=None,
#                           names=['UserID', 'Gender', 'Age', 'Occupation', 'Zip-code'], sep='::', engine='python',
#                           encoding='latin-1')
# datasetMovies = pd.read_csv("data/8_movies.dat", header=None,
#                             names=['MovieID', 'Title', 'Genres'], sep='::', engine='python',
#                             encoding='latin-1')
# dataset = pd.merge(datasetRatings, datasetUser, on='UserID', how='left')
# dataset = pd.merge(dataset, datasetMovies, on='MovieID', how='left')
# Imbalance(f'{output_name}_DB', dataset, sensitive_features, output_path="analysis/")
# Quality(f'{output_name}-users_DQ', "data/8_users.dat", "analysis/", isurl=False, symbol="::",
#         pretty_name=f'{pretty_name} Users')
# Quality(f'{output_name}-movies_DQ', "data/8_movies.dat", "analysis/", isurl=False, symbol="::",
#         pretty_name=f'{pretty_name} Movies')
# Quality(f'{output_name}-ratings_DQ', "data/8_ratings.dat", "analysis/", isurl=False, symbol="::", pretty_name=f'{pretty_name} Ratings')
#
# data_source = "data/9_default-of-credit-card-clients.csv"
# output_name = '9_CreditCardDefault'
# pretty_name = 'Credit Card Default'
# sensitive_features = ['SEX', 'EDUCATION', 'MARRIAGE', 'default payment next month']  # age
# dataset = pd.read_csv(data_source, header=1)
# Imbalance(f'{output_name}_DB', dataset, sensitive_features, output_path="analysis/")
# Quality(f'{output_name}_DQ', data_source, "analysis/", isurl=False, pretty_name=pretty_name)

# ***********DATA QUALITY**********
# Find all _DQ.csv files in the analysis directory
filenames_DQ = [f for f in os.listdir("analysis/") if f.endswith("_DQ.csv")]
# Read each file into a separate DataFrame
dfs = {}
for i, filename in enumerate(sorted(filenames_DQ)):
    dfs[i] = pd.read_csv(os.path.join("analysis", filename), header=0, sep=",",
                         names=["Dataset-Name", "Can-Open", "Com-I-1-DevA", "Com-I-5", "Acc-I-4", "Con-I-3",
                                "Con-I-2-DevB", "Con-I-4-DevC", "Error"])
# Concatenate all the DataFrames into a single DataFrame
all_df = pd.concat(dfs.values(), axis=0)
df = all_df[["Dataset-Name", "Com-I-1-DevA", "Com-I-5", "Acc-I-4", "Con-I-3", "Con-I-2-DevB", "Con-I-4-DevC"]]
print(df)
s = df.style.format(precision=3, decimal=',').hide(level=0, axis=0)
s.set_table_styles([
    {'selector': 'toprule', 'props': ':hline;'},
    {'selector': 'bottomrule', 'props': ':hline;'},
    {'selector': 'midrule', 'props': ':hline;'},
], overwrite=True)
f = open("tab_dataquality.tex", "w")
f.write(s.to_latex(column_format="|p{2cm}|r|r|r|r|r|r|", position="t", label="tab:dataquality",
                   caption="Data quality measurements"))
f.close()

# Calculate the average for each column (excluding 'Dataset-Name')
average_values = df.iloc[:, 1:].mean()
medians = df.iloc[:, 1:].median()
q1_values = df.iloc[:, 1:].quantile(0.25)
q3_values = df.iloc[:, 1:].quantile(0.75)
# Create a new DataFrame with the averages
dqsummary_df = pd.DataFrame({
    # 'Metric': metrics,
    'Average': average_values,
    'Median (Q2)': medians,
    '1st Quartile (Q1)': q1_values,
    '3rd Quartile (Q3)': q3_values
})
# Reset the index to have a single row DataFrame
dqsummary_df.reset_index(inplace=True)
# Rename the "index" column to "Metric"
dqsummary_df.rename(columns={'index': 'Metric'}, inplace=True)
# Sort the DataFrame by the "Metric" column in alphabetical order
dqsummary_df = dqsummary_df.sort_values(by='Metric', ascending=True)
# Print the resulting DataFrame
print(dqsummary_df)
# Select only the "Metric" and "Average" columns
dqsummary_tocsv_df = dqsummary_df[['Metric', 'Average']]
# Save the selected columns to a CSV file
dqsummary_tocsv_df.to_csv('analysis/dq_average.csv', index=False)
# Calculate positive error values
lower_error = abs(dqsummary_df['Average'] - dqsummary_df['1st Quartile (Q1)'])
upper_error = abs(dqsummary_df['3rd Quartile (Q3)'] - dqsummary_df['Average'])
# Create a horizontal bar plot with error bars (IQR whiskers)
plt.figure(figsize=(10, 6))
# Plot bars
plt.barh(dqsummary_df['Metric'], dqsummary_df['Average'], color='skyblue', xerr=[lower_error, upper_error], capsize=5)
plt.xlabel('Average', fontsize=22)
plt.ylabel('Quality Measure', fontsize=22)
plt.xticks(fontsize=22)
plt.yticks(fontsize=22)
# plt.title('Quality Measures Average and Error')
# Show the plot
plt.grid(axis='x', linestyle='--', alpha=0.6)  # Add grid lines for reference
plt.tight_layout()
plt.gca().invert_yaxis()  # Invert the y-axis to display from top to bottom
plt.savefig('analysis/images/quality_measures_plot.svg', format="svg")
plt.savefig('analysis/images/quality_measures_plot.pdf', format="pdf")
plt.show()

# ********** Data documentation (DD)*************
# Find all _DQ.csv files in the analysis directory
filenames_DTS = [f for f in os.listdir("analysis/") if f.endswith("_DTS.ods")]
# Read each file into a separate DataFrame
dfs = []
for i, filename in enumerate(sorted(filenames_DTS)):
    df = pd.read_excel(os.path.join("analysis", filename), header=0, sheet_name="metrics", engine="odf")
    df['Dataset'] = filename.split("_")[1]
    dfs.append(df)
# Concatenate all the DataFrames into a single DataFrame
all_df = pd.concat(dfs, axis=0, ignore_index=True)
print(all_df)
# Group by 'Metric' and calculate the average, median, 1st quartile, and 3rd quartile of 'Value'
dd_result_df = all_df.groupby('Metric')['Value'].agg(['mean', 'median', lambda x: x.quantile(0.25), lambda x: x.quantile(0.75)]).reset_index()
# Rename the columns
dd_result_df = dd_result_df.rename(columns={'mean': 'Presence Average', 'median': 'Median', '<lambda_0>': '1st Quartile (Q1)', '<lambda_1>': '3rd Quartile (Q3)'})
dd_result_df['Metric'] = dd_result_df['Metric'].str.replace(' Presence Average', '')
print(dd_result_df)
dd_tocsv_df = dd_result_df[['Metric', 'Presence Average']]
# Save the DataFrame to a CSV file
dd_tocsv_df.to_csv("analysis/dts_average.csv", index=False)  # Use index=False to exclude the index column in the CSV file
s = dd_tocsv_df.style.format(precision=2, decimal=',').hide(level=0, axis=0)
s.set_table_styles([
    {'selector': 'toprule', 'props': ':hline;'},
    {'selector': 'bottomrule', 'props': ':hline;'},
    {'selector': 'midrule', 'props': ':hline;'},
], overwrite=True)
f = open("tab_dts_average.tex", "w")
f.write(s.to_latex(column_format="|l|r|", position="t", label="tab:dts-average",
                   caption="Data documentation measurements"))
f.close()
# Sort the DataFrame by the "Metric" column in alphabetical order
dd_result_df = dd_result_df.sort_values(by='Metric', ascending=True)
# Calculate positive error values
lower_error = abs(dd_result_df['Presence Average'] - dd_result_df['1st Quartile (Q1)'])
upper_error = abs(dd_result_df['3rd Quartile (Q3)'] - dd_result_df['Presence Average'])
# Extract the metric names and presence averages
metrics = dd_result_df['Metric']
presence_averages = dd_result_df['Presence Average']
# Create a bar plot
plt.figure(figsize=(10, 6))
plt.barh(metrics, presence_averages, color='skyblue', xerr=[lower_error, upper_error], capsize=5)
plt.xlim(0, 1)  # Set the x-axis limits from 0 to 1
plt.xlabel('Presence Average', fontsize=22)
plt.ylabel('Documentation Section', fontsize=22)
# plt.title('Presence Average by Metric')
plt.grid(axis='x', linestyle='--', alpha=0.6)  # Add grid lines for reference
plt.xticks(fontsize=22)
plt.yticks(fontsize=22)
# Display the plot
plt.tight_layout()
plt.gca().invert_yaxis()  # Invert the y-axis to display from top to bottom
plt.savefig('analysis/images/presence_average_plot.svg', format="svg")
plt.savefig('analysis/images/presence_average_plot.pdf', format="pdf")
plt.show()
plt.show()

