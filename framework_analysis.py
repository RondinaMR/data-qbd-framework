import os
from utilities import modify_latex_table
import pandas as pd
import matplotlib.pyplot as plt
from extended_data_briefs import create_extended_data_briefs
from ethical_challenge_risk_labels import compute_ethical_challenge_risks_labels

# Set the maximum number of rows and columns to display
pd.set_option('display.max_rows', None)  # Display all rows
pd.set_option('display.max_columns', None)  # Display all columns
min_color = "#fc9272"  # dark red 50%
max_color = "#ffffff"  # white

def dq_analysis(min_color, max_color):
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
    f = open("analysis/latex/tab_dataquality.tex", "w")
    f.write(s.to_latex(column_format="|p{2cm}|r|r|r|r|r|r|", position="t", label="tab:dataquality",
                    caption="Data quality measurements"))
    f.close()

    # Add colors to the latex table
    input_tex_file = 'analysis/latex/tab_dataquality.tex'
    modify_latex_table(input_tex_file, min_color, max_color, dataquality_rule=True)
    print("Colors successfully added to the latex table!")

    # Calculate the average for each column (excluding 'Dataset-Name')
    average_values = dq_df.iloc[:, :].mean()
    medians = dq_df.iloc[:, :].median()
    q1_values = dq_df.iloc[:, :].quantile(0.25)
    q3_values = dq_df.iloc[:, :].quantile(0.75)
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
    print("dqsummary_df")
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
    plt.savefig('analysis/images/quality_measures_plot.pdf', format="pdf")
    # plt.show()
    return dq_df, dataset_names, dataset_dict

def dd_analysis(min_color, max_color):
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
    f = open("analysis/latex/tab_dts.tex", "w")
    f.write(s.to_latex(column_format="|p{2cm}|r|r|r|r|r|r|", position="t", label="tab:dts_all",
                    caption="Documentation measurements"))
    f.close()
    input_tex_file = 'analysis/latex/tab_dts.tex'
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
    f = open("analysis/latex/tab_dts_average.tex", "w")
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
    plt.savefig('analysis/images/presence_average_plot.pdf', format="pdf")
    # plt.show()
    return dd_df

def db_analysis():
    # Find all _DB.csv files in the analysis directory
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
    s = db_df.style.format(precision=3, decimal=',').hide(level=0, axis=0)
    s.set_table_styles([
        {'selector': 'toprule', 'props': ':hline;'},
        {'selector': 'bottomrule', 'props': ':hline;'},
        {'selector': 'midrule', 'props': ':hline;'},
    ], overwrite=True)
    f = open("analysis/latex/tab_databalance.tex", "w")
    f.write(s.to_latex(column_format="|l|r|", position="t", label="tab:dts-average",
                    caption="Data balance measurements"))
    f.close()
    return db_df

def analyse():
    # ***********DATA QUALITY (DQ) **********
    dq_df, dataset_names, dataset_dict = dq_analysis(min_color=min_color, max_color=max_color)

    # ********** Data documentation (DD) *************
    dd_df = dd_analysis(min_color=min_color, max_color=max_color)

    # ********** Data balance (DB) *************
    db_df = db_analysis()

    # ********** Extended Data Briefs *************
    create_extended_data_briefs()

    # ********** Ethical Challenge Risk Labels *************
    compute_ethical_challenge_risks_labels(dq_df, db_df, dd_df, dataset_names, dataset_dict, max_color, min_color)

    return


if __name__ == "__main__":
    analyse()
    
