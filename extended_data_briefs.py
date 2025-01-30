import pandas as pd
from utilities import interpolate_color, value_to_str, risk_color_or_nothing, tex_sanitizer


def tex_extended_data_brief(tex_template, input_dq, input_dd, input_db, input_dbf, output_tex):
    with open(tex_template, 'r') as f:
        tex_content = f.read()
    # Read the Data Quality DataFrame
    dq_df = pd.read_csv(input_dq, header=0, sep=",")
    # Read the Data Documentation DataFrame
    dd_metadata_df = pd.read_excel(input_dd, header=0, sheet_name="metadata", engine="odf")
    dd_metrics_df = pd.read_excel(input_dd, header=0, sheet_name="metrics", engine="odf")
    # Read the Data Balance DataFrame
    if not input_db is None:
        db_df = pd.read_csv(input_db, header=0, sep=",")
    else:
        db_df = None
    # Read the Data Brief DataFrame
    dbf_df = pd.read_csv(input_dbf, header=0, sep=",", quotechar='"')
    
    
    # %%%%%DATASET_NAME%%%%%
    tex_content = tex_content.replace('%%%%%DATASET_NAME%%%%%', dd_metadata_df.loc[dd_metadata_df["Name"]=='dataset-name', "Value"].values[0])

    # %%%%%DATASET_LABEL_NAME%%%%%
    tex_content = tex_content.replace('%%%%%DATASET_LABEL_NAME%%%%%', dd_metadata_df.loc[dd_metadata_df["Name"]=='dataset-name', "Value"].values[0].replace(' ', ''))

    # %%%%%DATASET_ANALYSIS%%%%%
    tex_content = tex_content.replace('%%%%%DATE_ANALYSIS%%%%%', dd_metadata_df.loc[dd_metadata_df["Name"]=='read-date', "Value"].values[0].to_pydatetime().strftime('%m/%d/%Y'))

    # %%%%%DESCRIPTION%%%%%
    tex_content = tex_content.replace('%%%%%DESCRIPTION%%%%%', tex_sanitizer(dbf_df.loc[dbf_df["key"]=='description', "value"].values[0]))

    # %%%%%LANDING_PAGE%%%%%
    tex_content = tex_content.replace('%%%%%LANDING_PAGE%%%%%', f'\href{{{dbf_df.loc[dbf_df["key"]=="link_url", "value"].values[0]}}}{{{tex_sanitizer(dbf_df.loc[dbf_df["key"]=="link_show", "value"].values[0])}}}')

    # %%%%%SAMPLE_SIZE%%%%%
    tex_content = tex_content.replace('%%%%%SAMPLE_SIZE%%%%%', tex_sanitizer(dbf_df.loc[dbf_df["key"]=='sample_size', "value"].values[0]))

    # %%%%%DOMAIN%%%%%
    tex_content = tex_content.replace('%%%%%DOMAIN%%%%%', dbf_df.loc[dbf_df["key"]=='domain', "value"].values[0])

    # %%%%%LAST_UPDATE%%%%%
    tex_content = tex_content.replace('%%%%%LAST_UPDATE%%%%%', str(dd_metadata_df.loc[dd_metadata_df["Name"]=='year', "Value"].values[0]))

    
    # %%%%%DATA_SPECIFICATION%%%%%
    tex_content = tex_content.replace('%%%%%DATA_SPECIFICATION%%%%%', dbf_df.loc[dbf_df["key"]=='data_specification', "value"].values[0])
    
    
    # %%%%%CREATOR_AFFILIATION%%%%%
    tex_content = tex_content.replace('%%%%%CREATOR_AFFILIATION%%%%%', dbf_df.loc[dbf_df["key"]=='affiliation_of_creators', "value"].values[0])

    # %%%%%DQ_ACCI4%%%%%
    min_color = "#ffffff"  # white
    max_color = "#fc9272"  # dark red 50%
    value = dq_df["Acc-I-4"].values[0]
    color = interpolate_color(min_color, max_color, value)
    tex_content = tex_content.replace('%%%%%DQ_ACCI4%%%%%', f'{value_to_str(value)}\cellcolor[HTML]{{{color}}}')

    # %%%%%DQ_CONI3DEVC%%%%%
    value = dq_df["Con-I-3-DevC"].values[0]
    color = interpolate_color(min_color, max_color, value)
    tex_content = tex_content.replace('%%%%%DQ_CONI3DEVC%%%%%', f'{value_to_str(value)}\cellcolor[HTML]{{{color}}}')

    # %%%%%DQ_COMI1DEVA%%%%%
    min_color = "#fc9272"  # dark red 50%
    max_color = "#ffffff"  # white
    value = dq_df["Com-I-1-DevA"].values[0]
    color = interpolate_color(min_color, max_color, value)
    tex_content = tex_content.replace('%%%%%DQ_COMI1DEVA%%%%%', f'{value_to_str(value)}\cellcolor[HTML]{{{color}}}')

    # %%%%%DQ_COMI5%%%%%
    value = dq_df["Com-I-5"].values[0]
    color = interpolate_color(min_color, max_color, value)
    tex_content = tex_content.replace('%%%%%DQ_COMI5%%%%%', f'{value_to_str(value)}\cellcolor[HTML]{{{color}}}')

    # %%%%%DQ_CONI2DEVB%%%%%
    value = dq_df["Con-I-2-DevB"].values[0]
    color = interpolate_color(min_color, max_color, value)
    tex_content = tex_content.replace('%%%%%DQ_CONI2DEVB%%%%%', f'{value_to_str(value)}\cellcolor[HTML]{{{color}}}')

    # %%%%%DQ_CONI4DEVD%%%%%
    value = dq_df["Con-I-4-DevD"].values[0]
    color = interpolate_color(min_color, max_color, value)
    tex_content = tex_content.replace('%%%%%DQ_CONI4DEVD%%%%%', f'{value_to_str(value)}\cellcolor[HTML]{{{color}}}')
    
    # %%%%%DD_OVERALL%%%%%
    value = dd_metrics_df.loc[dd_metrics_df["Metric"]=="Overall Presence Average", "Value"].values[0]
    color = interpolate_color(min_color, max_color, value)
    tex_content = tex_content.replace('%%%%%DD_OVERALL%%%%%', f'{value_to_str(value)}\cellcolor[HTML]{{{color}}}')
    
    # %%%%%DD_1MOTIVATION%%%%%
    value = dd_metrics_df.loc[dd_metrics_df["Metric"]=="1 Motivation Presence Average", "Value"].values[0]
    color = interpolate_color(min_color, max_color, value)
    tex_content = tex_content.replace('%%%%%DD_1MOTIVATION%%%%%', f'{value_to_str(value)}\cellcolor[HTML]{{{color}}}')
    
    # %%%%%DD_2COMPOSITION%%%%%
    value = dd_metrics_df.loc[dd_metrics_df["Metric"]=="2 Composition Presence Average", "Value"].values[0]
    color = interpolate_color(min_color, max_color, value)
    tex_content = tex_content.replace('%%%%%DD_2COMPOSITION%%%%%', f'{value_to_str(value)}\cellcolor[HTML]{{{color}}}')
    
    # %%%%%DD_3COLLECTIONPROCESSES%%%%%
    value = dd_metrics_df.loc[dd_metrics_df["Metric"]=="3 Collection processes Presence Average", "Value"].values[0]
    color = interpolate_color(min_color, max_color, value)
    tex_content = tex_content.replace('%%%%%DD_3COLLECTIONPROCESSES%%%%%', f'{value_to_str(value)}\cellcolor[HTML]{{{color}}}')
    
    # %%%%%DD_4DATAPROCESSINGPROCEDURES%%%%%
    value = dd_metrics_df.loc[dd_metrics_df["Metric"]=="4 Data processing procedures Presence Average", "Value"].values[0]
    color = interpolate_color(min_color, max_color, value)
    tex_content = tex_content.replace('%%%%%DD_4DATAPROCESSINGPROCEDURES%%%%%', f'{value_to_str(value)}\cellcolor[HTML]{{{color}}}')
    
    # %%%%%DD_5USES%%%%%
    value = dd_metrics_df.loc[dd_metrics_df["Metric"]=="5 Uses Presence Average", "Value"].values[0]
    color = interpolate_color(min_color, max_color, value)
    tex_content = tex_content.replace('%%%%%DD_5USES%%%%%', f'{value_to_str(value)}\cellcolor[HTML]{{{color}}}')
    # %%%%%DD_6MAINTENANCE%%%%%
    value = dd_metrics_df.loc[dd_metrics_df["Metric"]=="6 Maintenance Presence Average", "Value"].values[0]
    color = interpolate_color(min_color, max_color, value)
    tex_content = tex_content.replace('%%%%%DD_6MAINTENANCE%%%%%', f'{value_to_str(value)}\cellcolor[HTML]{{{color}}}')
    
    # %%%%%DATA_BALANCE%%%%%
    if not db_df is None:
        tex_content = tex_content.replace('%%%%%DATA_BALANCE_HEADER%%%%%', ''.join('\multicolumn{5}{|l|}{\\textbf{Data balance} (\\textsc{db})} \\\\ \\hline \n \t\tSensitive Feature & Gini ($\\uparrow$) & Shannon ($\\uparrow$) & Simpson ($\\uparrow$) & I.I.R. ($\\uparrow$) \\\\ \\hline'))

        f = lambda feature, gini, shannon, simpson, iir: f"{tex_sanitizer(feature.replace('_',' '))} & {value_to_str(gini)}{risk_color_or_nothing(gini,'gini')} & {value_to_str(shannon)}{risk_color_or_nothing(shannon,'shannon')} & {value_to_str(simpson)}{risk_color_or_nothing(simpson,'simpson')} & {value_to_str(iir)}{risk_color_or_nothing(iir,'iir')} \\\\\n\t\t"
        db_tex = [f(row[0],row[1],row[2],row[3],row[4]) for row in zip(db_df['Feature'],db_df['Gini'],db_df['Shannon'],db_df['Simpson'],db_df['I.I.R.'])]
        tex_content = tex_content.replace('%%%%%DATA_BALANCE%%%%%', ''.join(db_tex))
    else:
        tex_content = tex_content.replace('%%%%%DATA_BALANCE_HEADER%%%%%', '')
        tex_content = tex_content.replace('%%%%%DATA_BALANCE%%%%%', '')

    with open(output_tex, 'w') as f:
        f.write(tex_content)
    return

def create_extended_data_briefs():
    tex_template = 'analysis/latex/templates/extended_data_brief.tex'
    
    tex_extended_data_brief(tex_template=tex_template, input_dq='analysis/1_Adult_DQ.csv', input_dd='analysis/1_Adult_DTS.ods', input_db='analysis/1_Adult_DB.csv', input_dbf='data/1_adult_databrief.csv', output_tex='analysis/latex/extended_data_briefs/1_Adult_EDB.tex')
    
    tex_extended_data_brief(tex_template=tex_template, input_dq='analysis/2_COMPAS_DQ.csv', input_dd='analysis/2_COMPAS_DTS.ods', input_db='analysis/2_COMPAS_DB.csv', input_dbf='data/2_compas_databrief.csv', output_tex='analysis/latex/extended_data_briefs/2_COMPAS_EDB.tex')
    
    tex_extended_data_brief(tex_template=tex_template, input_dq='analysis/3_SouthGermanCredit_DQ.csv', input_dd='analysis/3_SouthGermanCredit_DTS.ods', input_db='analysis/3_SouthGermanCredit_DB.csv', input_dbf='data/3_southgermancredit_databrief.csv', output_tex='analysis/latex/extended_data_briefs/3_SouthGermanCredit_EDB.tex')

    tex_extended_data_brief(tex_template=tex_template, input_dq='analysis/4_CommunitiesAndCrime_DQ.csv', input_dd='analysis/4_CommunitiesAndCrime_DTS.ods', input_db=None, input_dbf='data/4_communities_databrief.csv', output_tex='analysis/latex/extended_data_briefs/4_CommunitiesAndCrime_EDB.tex')
    
    tex_extended_data_brief(tex_template=tex_template, input_dq='analysis/5_BankMarketing_DQ.csv', input_dd='analysis/5_BankMarketing_DTS.ods', input_db='analysis/5_BankMarketing_DB.csv', input_dbf='data/5_bank_databrief.csv', output_tex='analysis/latex/extended_data_briefs/5_BankMarketing_EDB.tex')
    
    tex_extended_data_brief(tex_template=tex_template, input_dq='analysis/6_LawSchool_DQ.csv', input_dd='analysis/6_LawSchool_DTS.ods', input_db='analysis/6_LawSchool_DB.csv', input_dbf='data/6_lawschool_databrief.csv', output_tex='analysis/latex/extended_data_briefs/6_LawSchool_EDB.tex')
    
    tex_extended_data_brief(tex_template=tex_template, input_dq='analysis/8_MovieLens_DQ.csv', input_dd='analysis/8_MovieLens_DTS.ods', input_db='analysis/8_MovieLens_DB.csv', input_dbf='data/8_movielens_databrief.csv', output_tex='analysis/latex/extended_data_briefs/8_MovieLens_EDB.tex')
    
    tex_extended_data_brief(tex_template=tex_template, input_dq='analysis/9_CreditCardDefault_DQ.csv', input_dd='analysis/9_CreditCardDefault_DTS.ods', input_db='analysis/9_CreditCardDefault_DB.csv', input_dbf='data/9_defaultcreditcard_databrief.csv', output_tex='analysis/latex/extended_data_briefs/9_CreditCardDefault_EDB.tex')

    return

if __name__ == "__main__":
    create_extended_data_briefs()
