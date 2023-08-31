from imbalance import Imbalance
from quality import Quality
import pandas as pd
import numpy as np
import os

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
s = df.style.format(precision=3).hide(level=0, axis=0)
s.set_table_styles([
    {'selector': 'toprule', 'props': ':hline;'},
    {'selector': 'bottomrule', 'props': ':hline;'},
    {'selector': 'midrule', 'props': ':hline;'},
], overwrite=True)
f = open("tab_dataquality.tex", "w")
f.write(s.to_latex(column_format="|p{2cm}|r|r|r|r|r|r|", position="t", label="tab:dataquality",
                   caption="Data quality measurements"))
f.close()
