from imbalance import Imbalance
from quality import Quality
import numpy as np
import pandas as pd

def adult():
        data_source = 'data/1_adult.data'
        output_name = '1_Adult'
        pretty_name = 'Adult'
        dataset = pd.read_csv(data_source, sep=',',
                                names=['age', 'workclass', 'fnlwgt', 'education', 'education-num', 'marital-status',
                                        'occupation', 'relationship', 'race', 'sex', 'capital-gain', 'capital-loss',
                                        'hours-per-week', 'native-country', 'income'],
                                dtype={'age': np.int64, 'workclass': str, 'fnlwgt': np.int64, 'education': str,
                                        'education-num': np.int64, 'marital-status': str, 'occupation': str,
                                        'relationship': str, 'race': str, 'sex': str, 'capital-gain': np.int64,
                                        'capital-loss': np.int64, 'hours-per-week': np.int64, 'native-country': str,
                                        'income': str}, na_values='?', encoding='utf-8')
        sensitive_features = ['sex', 'race', 'education', 'marital-status', 'native-country', 'income']
        Imbalance(f'{output_name}_DB', dataset, sensitive_features, output_path="analysis/")
        Quality(f'{output_name}_DQ', data_source, "analysis/", isurl=False, pretty_name=pretty_name)
        return

def compas():
        # data_source = 'data/2_compas-scores-raw.csv'
        data_source = 'data/2_compas-scores-two-years.csv'
        output_name = '2_COMPAS'
        pretty_name = 'COMPAS'
        # sensitive_features = ['Sex_Code_Text', 'Ethnic_Code_Text', 'Language', 'MaritalStatus', 'DecileScore']
        sensitive_features = ['sex', 'race', 'age_cat', 'v_score_text']
        dataset = pd.read_csv(data_source, header=0, sep=',')
        Imbalance(f'{output_name}_DB', dataset, sensitive_features, output_path="analysis/")
        Quality(f'{output_name}_DQ', data_source, "analysis/", isurl=False, pretty_name=pretty_name)
        return

def south_german_credit():
        data_source = "data/3_SouthGermanCredit.asc"
        output_name = '3_SouthGermanCredit'
        pretty_name = 'South German Credit'
        sensitive_features = ['gastarb', 'laufkont', 'famges', 'beruf', 'verm', 'kredit']
        dataset = pd.read_csv(data_source, header=0, sep=" ")
        Imbalance(f'{output_name}_DB', dataset, sensitive_features, output_path="analysis/")
        Quality(f'{output_name}_DQ', data_source, "analysis/", isurl=False, pretty_name=pretty_name)
        return     

def communities_and_crime():
        data_source = 'data/4_communities.data'
        output_name = '4_CommunitiesAndCrime'
        pretty_name = 'Communities And Crime'
        attribute_names = [
                "state", "county", "community", "communityname", "fold", "population", "householdsize",
                "racepctblack", "racePctWhite", "racePctAsian", "racePctHisp", "agePct12t21", "agePct12t29",
                "agePct16t24", "agePct65up", "numbUrban", "pctUrban", "medIncome", "pctWWage", "pctWFarmSelf",
                "pctWInvInc", "pctWSocSec", "pctWPubAsst", "pctWRetire", "medFamInc", "perCapInc", "whitePerCap",
                "blackPerCap", "indianPerCap", "AsianPerCap", "OtherPerCap", "HispPerCap", "NumUnderPov",
                "PctPopUnderPov", "PctLess9thGrade", "PctNotHSGrad", "PctBSorMore", "PctUnemployed",
                "PctEmploy", "PctEmplManu", "PctEmplProfServ", "PctOccupManu", "PctOccupMgmtProf",
                "MalePctDivorce", "MalePctNevMarr", "FemalePctDiv", "TotalPctDiv", "PersPerFam",
                "PctFam2Par", "PctKids2Par", "PctYoungKids2Par", "PctTeen2Par", "PctWorkMomYoungKids",
                "PctWorkMom", "NumIlleg", "PctIlleg", "NumImmig", "PctImmigRecent", "PctImmigRec5",
                "PctImmigRec8", "PctImmigRec10", "PctRecentImmig", "PctRecImmig5", "PctRecImmig8",
                "PctRecImmig10", "PctSpeakEnglOnly", "PctNotSpeakEnglWell", "PctLargHouseFam",
                "PctLargHouseOccup", "PersPerOccupHous", "PersPerOwnOccHous", "PersPerRentOccHous",
                "PctPersOwnOccup", "PctPersDenseHous", "PctHousLess3BR", "MedNumBR", "HousVacant",
                "PctHousOccup", "PctHousOwnOcc", "PctVacantBoarded", "PctVacMore6Mos", "MedYrHousBuilt",
                "PctHousNoPhone", "PctWOFullPlumb", "OwnOccLowQuart", "OwnOccMedVal", "OwnOccHiQuart",
                "RentLowQ", "RentMedian", "RentHighQ", "MedRent", "MedRentPctHousInc", "MedOwnCostPctInc",
                "MedOwnCostPctIncNoMtg", "NumInShelters", "NumStreet", "PctForeignBorn", "PctBornSameState",
                "PctSameHouse85", "PctSameCity85", "PctSameState85", "LemasSwornFT", "LemasSwFTPerPop",
                "LemasSwFTFieldOps", "LemasSwFTFieldPerPop", "LemasTotalReq", "LemasTotReqPerPop",
                "PolicReqPerOffic", "PolicPerPop", "RacialMatchCommPol", "PctPolicWhite", "PctPolicBlack",
                "PctPolicHisp", "PctPolicAsian", "PctPolicMinor", "OfficAssgnDrugUnits", "NumKindsDrugsSeiz",
                "PolicAveOTWorked", "LandArea", "PopDens", "PctUsePubTrans", "PolicCars", "PolicOperBudg",
                "LemasPctPolicOnPatr", "LemasGangUnitDeploy", "LemasPctOfficDrugUn", "PolicBudgPerPop",
                "ViolentCrimesPerPop"
        ]
        dataset = pd.read_csv('data/4_communities.data', sep=',', header=None, names=attribute_names)
        dataset['ViolentCrimesPerPop_discretized'] = pd.cut(dataset['ViolentCrimesPerPop'], bins=3, labels=['low','medium','high'])
        sensitive_features = ['state', 'ViolentCrimesPerPop_discretized']
        Imbalance(f'{output_name}_DB', dataset, sensitive_features, output_path="analysis/")
        Quality(f'{output_name}_DQ', data_source, "analysis/", isurl=False, pretty_name=pretty_name)
        return

def bank_marketing():
        data_source = "data/5_bank-additional-full.csv"
        output_name = '5_BankMarketing'
        pretty_name = 'Bank Marketing'
        sensitive_features = ['job', 'education', 'marital', 'y']
        dataset = pd.read_csv(data_source, sep=";", na_values=['unknown'])
        Imbalance(f'{output_name}_DB', dataset, sensitive_features, output_path="analysis/")
        Quality(f'{output_name}_DQ', data_source, "analysis/", isurl=False, pretty_name=pretty_name)
        return

def law_school():
        data_source = "data/6_LawSchool_bar_pass_prediction.csv"
        output_name = '6_LawSchool'
        pretty_name = 'Law School'
        sensitive_features = ['gender', 'race1', 'lsat', 'ugpa', 'pass_bar']
        dataset = pd.read_csv(data_source, header=0)
        Imbalance(f'{output_name}_DB', dataset, sensitive_features, output_path="analysis/")
        Quality(f'{output_name}_DQ', data_source, "analysis/", isurl=False, pretty_name=pretty_name)
        return

def movielens():
        output_name = '8_MovieLens'
        pretty_name = 'MovieLens'
        sensitive_features = ['Gender', 'Occupation', 'Zip-code']
        #     datasetRatings = pd.read_csv("data/8_ratings.dat", header=None,
        #                                 names=['UserID', 'MovieID', 'Rating', 'Timestamp'], sep='::', engine='python',
        #                                 encoding='latin-1')
        #     datasetUser = pd.read_csv("data/8_users.dat", header=None,
        #                             names=['UserID', 'Gender', 'Age', 'Occupation', 'Zip-code'], sep='::', engine='python',
        #                             encoding='latin-1')
        #     datasetMovies = pd.read_csv("data/8_movies.dat", header=None,
        #                                 names=['MovieID', 'Title', 'Genres'], sep='::', engine='python',
        #                                 encoding='latin-1')
        #     dataset = pd.merge(datasetRatings, datasetUser, on='UserID', how='left')
        #     dataset = pd.merge(dataset, datasetMovies, on='MovieID', how='left')
        dataset = pd.read_csv("data/8_users.dat", header=None,
                                names=['UserID', 'Gender', 'Age', 'Occupation', 'Zip-code'], sep='::', engine='python', encoding='latin-1')
        Imbalance(f'{output_name}_DB', dataset, sensitive_features, output_path="analysis/")
        # Quality(f'{output_name}-users_DQ', "data/8_users.dat", "analysis/", isurl=False, symbol="::", pretty_name=f'{pretty_name} Users')
        #     Quality(f'{output_name}-movies_DQ', "data/8_movies.dat", "analysis/", isurl=False, symbol="::",
        #             pretty_name=f'{pretty_name} Movies')
        #     Quality(f'{output_name}-ratings_DQ', "data/8_ratings.dat", "analysis/", isurl=False, symbol="::", pretty_name=f'{pretty_name} Ratings')
        Quality(f'{output_name}_DQ', "data/8_users.dat", "analysis/", isurl=False, symbol="::", pretty_name=f'{pretty_name}')
        return

def default_credit_card():
        data_source = "data/9_default-of-credit-card-clients.csv"
        output_name = '9_CreditCardDefault'
        pretty_name = 'Credit Card Default'
        sensitive_features = ['SEX', 'EDUCATION', 'MARRIAGE', 'default payment next month']  # age
        dataset = pd.read_csv(data_source, header=1)
        Imbalance(f'{output_name}_DB', dataset, sensitive_features, output_path="analysis/")
        Quality(f'{output_name}_DQ', data_source, "analysis/", isurl=False, pretty_name=pretty_name)
        return

def compute():
        adult()
        compas()
        south_german_credit()
        communities_and_crime()
        bank_marketing()        
        law_school()
        movielens()
        default_credit_card()
        return

if __name__ == "__main__":
    compute()