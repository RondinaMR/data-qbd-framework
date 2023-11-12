from imbalance import Imbalance
from quality import Quality
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib.sankey import Sankey
import re
import plotly.graph_objects as go
from reportlab.lib import colors
from reportlab.graphics.shapes import *
from reportlab.graphics import renderPDF
from reportlab.lib.colors import HexColor

# Set the maximum number of rows and columns to display
pd.set_option('display.max_rows', None)  # Display all rows
pd.set_option('display.max_columns', None)  # Display all columns


# Functions
def hex_to_rgb(hex_color):
    # Remove the '#' character if it's present
    hex_color = hex_color.lstrip('#')
    # Convert the hex color to RGB
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return r, g, b


def rgb_to_hex(rgb):
    # Convert RGB values to a hex color
    r, g, b = rgb
    return f"{r:02X}{g:02X}{b:02X}"


def interpolate_color(min_color, max_color, value):
    # Convert hex colors to RGB
    min_rgb = hex_to_rgb(min_color)
    max_rgb = hex_to_rgb(max_color)

    # Interpolate the RGB values
    interpolated_rgb = tuple(
        int(min_rgb[i] + (max_rgb[i] - min_rgb[i]) * value) for i in range(3)
    )

    # Convert the interpolated RGB values back to hex
    interpolated_color = rgb_to_hex(interpolated_rgb)
    return interpolated_color


def modify_latex_table(input_tex_file, min_color, max_color, dataquality_rule=False):
    # Read the LaTeX file
    with open(input_tex_file, 'r') as f:
        tex_content = f.read()
    position = 0
    # Define a regular expression pattern to match table cells
    cell_pattern = r'\d,\d{3}\s'
    # Find all matches of the pattern
    matches = re.findall(cell_pattern, tex_content)
    # Loop through the matches and update the table cells
    # Dataset-Name & Com-I-1-DevA & Com-I-5 & Acc-I-4 & Con-I-3 & Con-I-2-DevB & Con-I-4-DevC
    for match in matches:
        value = float(match.replace(',', '.'))
        if value > 1.0:
            value = 1.0
        if dataquality_rule and (((position % 6) == 0) or ((position % 6) == 4)):  # Acc-I-4 & Con-I-3
            value = 1 - value
        color = interpolate_color(min_color, max_color, value)
        replacement = f'{match.strip()}\cellcolor[HTML]{{{color}}}'
        tex_content = tex_content.replace(match, replacement, 1)
        position += 1
    # Write the modified content back to the file
    with open(input_tex_file, 'w') as f:
        f.write(tex_content)


def create_sankey_figure(dataset_name, dq_sum, db_sum, dd_sum, version="unit_flows"):
    d_sum = (dq_sum + db_sum + dd_sum)
    source_labels = ['data quality', 'data balance', 'data documentation']
    sink_labels = ['inconclusive evidence', 'inscrutable evidence', 'misguided evidence', 'unfair outcomes',
                   'transformative effects', 'traceability']
    sankey_versions = {
        "unit_flows": {
            "dq_flows": [1, 1, 1, 1],
            "db_flows": [1, 1, 1],
            "dd_flows": [1, 1, 1],
            "dataset_flows": [dq_sum * 4, db_sum * 3, dd_sum * 3]
        },
        "unit_challenges": {
            "dq_flows": [1, 0.5, 0.25, 0.333],
            "db_flows": [0.75, 1, 0.333],
            "dd_flows": [0.5, 1, 0.333],
            "dataset_flows": [dq_sum * 2.083, db_sum * 2.083, dd_sum * 2.083]
        },
        "dimensional_flows": {
            "dq_flows": [dq_sum / 4, dq_sum / 4, dq_sum / 4, dq_sum / 4],
            "db_flows": [db_sum / 3, db_sum / 3, db_sum / 3],
            "dd_flows": [dd_sum / 3, dd_sum / 3, dd_sum / 3],
            "dataset_flows": [dq_sum, db_sum, dd_sum]
        }
    }

    fig = go.Figure(go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=[dataset_name] + source_labels + sink_labels,
        ),
        link=dict(
            source=[0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 3, 3, 3],
            target=[1, 2, 3, 4, 5, 7, 9, 7, 8, 9, 5, 6, 9],
            value=sankey_versions[version]["dataset_flows"] + sankey_versions[version]["dq_flows"] +
                  sankey_versions[version]["db_flows"] +
                  sankey_versions[version]["dd_flows"],
        )
    ))
    # fig.update_layout(title_text=f"{dataset}")
    # fig.show()
    fig.write_image(f'analysis/images/{dataset}_sankey_{version}.pdf')


def create_labels(dataset_name, dq_risk, db_risk, dd_risk, min_color, max_color):
    ethical_challenges = {
        "1_inconclusive_evidence": {
            "risk": dq_risk,
            "dim": 1,
            "line1": "Inconclusive",
            "line2": "evidence"
        },
        "2_inscrutable_evidence": {
            "risk": dq_risk + dd_risk,
            "dim": 2,
            "line1": "Inscrutable",
            "line2": "evidence"
        },
        "3_misguided_evidence": {
            "risk": dd_risk,
            "dim": 1,
            "line1": "Misguided",
            "line2": "evidence"
        },
        "4_unfair_outcomes": {
            "risk": dq_risk + db_risk,
            "dim": 2,
            "line1": "Unfair",
            "line2": "outcomes"
        },
        "5_transformative_effects": {
            "risk": db_risk,
            "dim": 1,
            "line1": "Transformative",
            "line2": "effects"
        },
        "6_traceability": {
            "risk": dq_risk + db_risk + dd_risk,
            "dim": 3,
            "line1": "Traceability",
            "line2": "evidence"
        },
    }
    font_properties = {
        "fontSize": 40,
        "fontName": "Courier",
        "fillColor": colors.black
    }

    for ethical_challenge in ethical_challenges:
        ratio = ethical_challenges[ethical_challenge]["risk"] / ethical_challenges[ethical_challenge]["dim"]
        print(dataset_name, ethical_challenge, f'{ratio*100:.2f}%')
        d = Drawing(400, 400)
        d.add(Rect(0, 0, 400, 400, fillColor=HexColor(f"#{interpolate_color(min_color, max_color, ratio)}")))
        d.add(Rect(375, 0, 25, 400, fillColor=colors.white))
        d.add(Rect(375, 0, 25, ratio * 400, fillColor=colors.darkred))
        d.add(String(18, 250, ethical_challenges[ethical_challenge]["line1"], fontSize=font_properties["fontSize"],
                     fontName=font_properties["fontName"], fillColor=font_properties["fillColor"]))
        if ethical_challenges[ethical_challenge]["line2"] != "":
            d.add(String(18, 150, ethical_challenges[ethical_challenge]["line2"], fontSize=font_properties["fontSize"],
                         fontName=font_properties["fontName"], fillColor=font_properties["fillColor"]))

        renderPDF.drawToFile(d, f'analysis/images/labels/{dataset}_label_{ethical_challenge}.pdf',
                             f'{dataset}_label_{ethical_challenge}')


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
#                              'income': str}, na_values='?', encoding='utf-8')
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
                         names=["Dataset-Name", "Can-Open", "Com-I-1-DevA", "Com-I-5", "Acc-I-4", "Con-I-3-DevC",
                                "Con-I-2-DevB", "Con-I-4-DevD", "Error"])
# Concatenate all the DataFrames into a single DataFrame
all_df = pd.concat(dfs.values(), axis=0)
dq_df = all_df[["Dataset-Name", "Acc-I-4", "Com-I-1-DevA", "Com-I-5", "Con-I-2-DevB", "Con-I-3-DevC", "Con-I-4-DevD"]]
datasets_spaced_names = dq_df["Dataset-Name"].tolist()
dq_df["Dataset-Name"] = dq_df["Dataset-Name"].str.replace(' ', '')
dataset_names = dq_df["Dataset-Name"].tolist()
dq_df.sort_values(by=['Dataset-Name'], inplace=True)
dq_df = dq_df.rename(columns={"Dataset-Name": "Dataset"}).set_index("Dataset")
dataset_dict = dict(zip(dataset_names, datasets_spaced_names))
# "Dataset-Name", "Com-I-1-DevA(↑)", "Com-I-5(↑)", "Acc-I-4(↓)", "Con-I-3(↑)", "Con-I-2-DevB(↑)", "Con-I-4-DevC(↑)"
print("DQ_DF", dq_df)

s = dq_df.style.format(precision=3, decimal=',').hide(level=0, axis=0)
s.set_table_styles([
    {'selector': 'toprule', 'props': ':hline;'},
    {'selector': 'bottomrule', 'props': ':hline;'},
    {'selector': 'midrule', 'props': ':hline;'},
], overwrite=True)
# s.background_gradient(axis=0)
f = open("tab_dataquality.tex", "w")
f.write(s.to_latex(column_format="|p{2cm}|r|r|r|r|r|r|", position="t", label="tab:dataquality",
                   caption="Data quality measurements"))
f.close()

# Add colors to the latex table
# # blue
# min_color = "#deebf7"
# max_color = "#3182bd"
# reds
min_color = "#fc9272"  # dark red 50% / dark red : "#de2d26"
max_color = "#ffffff"  # light red
input_tex_file = 'tab_dataquality.tex'
modify_latex_table(input_tex_file, min_color, max_color, dataquality_rule=True)
print("Colors successfully added to the latex table!")

# Calculate the average for each column (excluding 'Dataset-Name')
average_values = dq_df.iloc[:, 1:].mean()
medians = dq_df.iloc[:, 1:].median()
q1_values = dq_df.iloc[:, 1:].quantile(0.25)
q3_values = dq_df.iloc[:, 1:].quantile(0.75)
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
dqsummary_df['Metric'] = dqsummary_df['Metric'].apply(
    lambda x: f"{x}(↓)" if (x == "Acc-I-4" or x == "Con-I-3-DevC") else f"{x}(↑)")
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
plt.xlim(0, 1)  # Set the x-axis limits from 0 to 1
# plt.title('Quality Measures Average and Error')
# Show the plot
plt.grid(axis='x', linestyle='--', alpha=0.6)  # Add grid lines for reference
plt.tight_layout()
plt.gca().invert_yaxis()  # Invert the y-axis to display from top to bottom
# plt.savefig('analysis/images/quality_measures_plot.svg', format="svg")
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
dd_df = all_df[["Dataset", "Metric", "Value"]]
print(dd_df)
s = dd_df.style.format(precision=3, decimal=',').hide(level=0, axis=0)
s.set_table_styles([
    {'selector': 'toprule', 'props': ':hline;'},
    {'selector': 'bottomrule', 'props': ':hline;'},
    {'selector': 'midrule', 'props': ':hline;'},
], overwrite=True)
f = open("tab_dts.tex", "w")
f.write(s.to_latex(column_format="|p{2cm}|r|r|r|r|r|r|", position="t", label="tab:dts_all",
                   caption="Documentation measurements"))
f.close()
input_tex_file = 'tab_dts.tex'
modify_latex_table(input_tex_file, min_color, max_color)
print("Colors successfully added to the latex table!")
# Group by 'Metric' and calculate the average, median, 1st quartile, and 3rd quartile of 'Value'
dd_result_df = all_df.groupby('Metric')['Value'].agg(
    ['mean', 'median', lambda x: x.quantile(0.25), lambda x: x.quantile(0.75)]).reset_index()
# Rename the columns
dd_result_df = dd_result_df.rename(
    columns={'mean': 'Presence Average', 'median': 'Median', '<lambda_0>': '1st Quartile (Q1)',
             '<lambda_1>': '3rd Quartile (Q3)'})
dd_result_df['Metric'] = dd_result_df['Metric'].str.replace(' Presence Average', '')
print(dd_result_df)
dd_tocsv_df = dd_result_df[['Metric', 'Presence Average']]
# Save the DataFrame to a CSV file
dd_tocsv_df.to_csv("analysis/dts_average.csv",
                   index=False)  # Use index=False to exclude the index column in the CSV file
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
dd_result_df['Metric'] = dd_result_df['Metric'].apply(lambda x: f"{x}(↑)")
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
# plt.savefig('analysis/images/presence_average_plot.svg', format="svg")
plt.savefig('analysis/images/presence_average_plot.pdf', format="pdf")
plt.show()
plt.show()
# ********** Data balance (DB)*************
# Find all _DQ.csv files in the analysis directory
filenames_DTS = [f for f in os.listdir("analysis/") if f.endswith("_DB.csv")]
# Read each file into a separate DataFrame
dfs = []
for i, filename in enumerate(sorted(filenames_DTS)):
    df = pd.read_csv(os.path.join("analysis", filename), header=0)
    df['Dataset'] = filename.split("_")[1]
    dfs.append(df)
# Concatenate all the DataFrames into a single DataFrame
all_df = pd.concat(dfs, axis=0, ignore_index=True)
db_df = all_df[["Dataset", "Feature", "Gini", "Shannon", "Simpson", "I.I.R."]]
print(db_df)
# ********** Sankey flow plot*************
# Computation of the data quality risks sum
dq_df_cols = ["Acc-I-4", "Com-I-1-DevA", "Com-I-5", "Con-I-2-DevB", "Con-I-3-DevC", "Con-I-4-DevD"]
dq_df["risks_sum"] = dq_df[dq_df_cols].apply(
    lambda row: row["Acc-I-4"] + (1 - row["Com-I-1-DevA"]) + (1 - row["Com-I-5"]) + (1 - row["Con-I-2-DevB"]) + row[
        "Con-I-3-DevC"] + (1 - row["Con-I""-4-DevD"]), axis=1)
# Data quality risks ratio (sum divided by the maximum risk possible)
dq_df["risk_ratio"] = dq_df["risks_sum"].apply(lambda row: row / 6)
print("Data Quality\n", dq_df)

# Computation of the data balance risks sum
# Group by "Dataset" and compute sum for each group
db_aggregate_df = db_df.groupby('Dataset').agg(
    {'Gini': lambda x: (1 - x).sum(), 'Shannon': lambda x: (1 - x).sum(), 'Simpson': lambda x: (1 - x).sum(),
     'I.I.R.': lambda x: (1 - x).sum(), 'Feature': 'count'})
# Calculate "risk_ratio"
db_aggregate_df['simpson_risk_ratio'] = db_aggregate_df['Simpson'] / db_aggregate_df['Feature']
print("Data Balance\n", db_aggregate_df)

# Computation of the data documentation risks sum
# Exclude "Overall Presence Average" metric
dd_aggregate_df = dd_df[dd_df["Metric"] != "Overall Presence Average"]
# Group by "Dataset" and compute sum for each group
dd_aggregate_df = dd_aggregate_df.groupby('Dataset').agg({'Value': lambda x: (1 - x).sum()})
# Calculate "risk_ratio"
dd_aggregate_df['risk_ratio'] = dd_aggregate_df['Value'] / 6
print("Data Documentation\n", dd_aggregate_df)

for dataset in dataset_names:
    if dataset in ["MovieLensMovies", "MovieLensUsers", "MovieLensRatings", "CommunitiesAndCrime"]:
        continue
    dq_risk = dq_df.at[dataset, 'risk_ratio']
    # if dataset not in ["CommunitiesAndCrime", "MovieLensMovies", "MovieLensUsers", "MovieLensRatings"]:
    db_risk = db_aggregate_df.at[dataset, 'simpson_risk_ratio']
    dd_risk = dd_aggregate_df.at[dataset, 'risk_ratio']
    create_sankey_figure(dataset_dict[dataset], dq_risk, db_risk, dd_risk, "unit_flows")
    create_sankey_figure(dataset_dict[dataset], dq_risk, db_risk, dd_risk, "unit_challenges")
    create_sankey_figure(dataset_dict[dataset], dq_risk, db_risk, dd_risk, "dimensional_flows")
    create_labels(dataset_dict[dataset], dq_risk, db_risk, dd_risk, max_color, min_color)

# for index, row in dq_df.iterrows():
#     # Extract dataset name and relevant columns for dq_sum
#     dataset_name = row["Dataset-Name"].replace(" ", "")
#     dq_cols = ["Acc-I-4", "Com-I-1-DevA", "Com-I-5", "Con-I-2-DevB", "Con-I-3-DevC", "Con-I-4-DevD"]
#     # Calculate dq_sum for the current dataset
#     dq_sum = row[dq_cols].sum()
#     # Extract db_sum from db_df
#     db_sum = db_df.loc[db_df['Dataset'] == dataset_name, 'Simpson'].sum()
#     # Extract dd_sum from dd_df
#     dd_sum = dd_df.loc[dd_df['Dataset'] == dataset_name, 'Value'].sum()
#
#     # Create the text for the Sankey diagram
#     text = f"{dataset_name} [{dq_sum:.3f}] Data Quality ISO\n"
#     text += f"{dataset_name} [{db_sum:.3f}] Data Balance\n"
#     text += f"{dataset_name} [{dd_sum:.3f}] Data Documentation\n"
#     text += f"Data Quality ISO [{dq_sum / 4:.3f}] Inconclusive Evidence\n"
#     text += f"Data Documentation [{dd_sum / 3:.3f}] Inscrutable Evidence\n"
#     text += f"Data Quality ISO [{dq_sum / 4:.3f}] Misguided Evidence\n"
#     text += f"Data Documentation [{dd_sum / 3:.3f}] Misguided Evidence\n"
#     text += f"Data Quality ISO [{dq_sum / 4:.3f}] Unfair Outcomes\n"
#     text += f"Data Balance [{db_sum / 3:.3f}] Unfair Outcomes\n"
#     text += f"Data Balance [{db_sum / 3:.3f}] Transformative Effects\n"
#     text += f"Data Quality ISO [{dq_sum / 4:.3f}] Traceability\n"
#     text += f"Data Balance [{db_sum / 3:.3f}] Traceability\n"
#     text += f"Data Documentation [{dd_sum / 3:.3f}] Traceability\n"
#
#     # Save the text to a file
#     with open(f"analysis/sankey/{dataset_name}_sankey.txt", "w") as file:
#         file.write(text)
