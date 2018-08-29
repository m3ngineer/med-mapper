import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def clean_data(filename):

    data = pd.read_csv(filename, delimiter='\t')

    # Drop duplicate columns
    duplicate_cols = ['npi.1',
                  'nppes_provider_last_org_name.1',
                  'nppes_provider_first_name.1',
                  'nppes_provider_city.1',
                  'nppes_provider_state.1',
                  'specialty_description.1',
                  'description_flag.1',
                  'total_claim_count.1',
                  'total_30_day_fill_count.1',
                  'total_drug_cost.1',
                  'total_day_supply.1',
                  'bene_count.1',
                  'ge65_suppress_flag.1',
                  'total_claim_count_ge65.1',
                  'total_30_day_fill_count_ge65.1',
                  'total_drug_cost_ge65.1',
                  'total_day_supply_ge65.1',
                  'bene_count_ge65_suppress_flag.1',
                  'bene_count_ge65.1']

    data.drop(duplicate_cols, axis=1, inplace=True)

    # Add additional data from IRS and 2010 Census on zipcode demographics
    # Data processed in zipcode_data.ipynb
    zip_data = pd.read_csv('data/zip_data.csv', delimiter='\t')
    zip_data = zip_data.iloc[:,1:]  # drop unnamed column
    zip_data.drop(['agi', 'agi_stub'], axis=1, inplace=True)

    # rename Imbruvica zipcode5 column to merge with zipcode data
    data.rename(columns={'nppes_provider_zip5': 'zip'}, inplace=True)

    # merge zipcode demographic data with Imbruvica data
    data = pd.merge(data, zip_data, on='zip')

    # Make null bene_count, bene_count_ge65, total_claim_count_ge65, total_30_day_fill_count_ge65, brand_claim_count, other_claim_count, mapd_claim_count, pdp_claim_count, lis_claim_count, nonlis_claim_count, beneficiary_age_less_65_count, beneficiary_age_65_74_count, beneficiary_age_75_84_count, beneficiary_age_greater_84_count, beneficiary_female_count, beneficiary_male_count, beneficiary_race_white_count, beneficiary_race_black_count, beneficiary_race_asian_pi_count, beneficiary_race_hispanic_count, beneficiary_race_nat_ind_count, beneficiary_race_other_count, beneficiary_nondual_count, beneficiary_dual_count, beneficiary_average_risk_score with a random number between 1 and 10
    cols_fillna = ['bene_count', 'bene_count_ge65', 'total_claim_count_ge65', 'total_30_day_fill_count_ge65', 'brand_claim_count', 'generic_claim_count', 'other_claim_count', 'mapd_claim_count', 'pdp_claim_count', 'lis_claim_count', 'nonlis_claim_count', 'beneficiary_age_less_65_count', 'beneficiary_age_65_74_count', 'beneficiary_age_75_84_count', 'beneficiary_age_greater_84_count', 'beneficiary_female_count', 'beneficiary_male_count', 'beneficiary_race_white_count', 'beneficiary_race_black_count', 'beneficiary_race_asian_pi_count', 'beneficiary_race_hispanic_count', 'beneficiary_race_nat_ind_count', 'beneficiary_race_other_count', 'beneficiary_nondual_count', 'beneficiary_dual_count', 'beneficiary_average_risk_score', 'opioid_claim_count', 'opioid_day_supply', 'opioid_bene_count', 'er_opioid_claim_count', 'er_opioid_day_supply', 'er_opioid_bene_count', 'antibiotic_claim_count', 'antibiotic_bene_count', 'antipsych_claim_count_ge65', 'antipsych_bene_count_ge65']
    for col in cols_fillna:
        mask = data[col].isnull()
        data.loc[mask, col] = data.loc[mask, col].apply(lambda v: np.random.choice(range(1,11)))

    # Fill null values with average for total_drug_cost_ge65, total_day_supply_ge65, brand_drug_cost, other_drug_cost, mapd_drug_cost, pdp_drug_cost, lis_drug_cost, nonlis_drug_cost, average_age_of_beneficiaries, beneficiary_age_less_65_count
    cols_fillna = ['total_drug_cost_ge65', 'total_day_supply_ge65', 'brand_drug_cost', 'generic_drug_cost', 'other_drug_cost', 'mapd_drug_cost', 'pdp_drug_cost', 'lis_drug_cost', 'nonlis_drug_cost', 'average_age_of_beneficiaries', 'opioid_drug_cost', 'opioid_prescriber_rate', 'er_opioid_drug_cost', 'er_opioid_prescriber_rate' , 'antibiotic_drug_cost', 'antipsych_drug_cost_ge65']
    for col in cols_fillna:
        data[col].fillna(data[col].mean(), inplace=True)

    # Create new binary label based off of total_claim_count
    data['high_prescrib'] = 0
    data.loc[data['total_claim_count'] >= data['total_claim_count'].quantile(0.75), 'high_prescrib'] = 1

    # Drop columns unimportant for model performance and redundant to label
    drop_cols = ['bene_count', 'bene_count_ge65',
             'total_drug_cost', 'total_drug_cost_ge65', 'total_claim_count_ge65',
             'total_day_supply_ge65', 'total_30_day_fill_count_ge65',
             'total_30_day_fill_count', 'total_day_supply',
             'nppes_provider_street1', 'nppes_provider_country',
             'nppes_entity_code', 'nppes_provider_gender',
             'medicare_prvdr_enroll_status', 'n_returns',
             'beneficiary_race_nat_ind_count', 'average_age_of_beneficiaries',
             'other_drug_cost', 'beneficiary_race_other_count',
             'n_return_total_inc', 'n_returns_wages',
             'wages_amt', 'other_claim_count',
             'beneficiary_race_asian_pi_count', 'brand_claim_count',
             'beneficiary_race_black_count', 'total_income_amt',
             'generic_claim_count', 'total_wages_per_return',
             'brand_drug_cost', 'mapd_claim_count',
             'beneficiary_age_greater_84_count', 'nppes_credentials',
             'beneficiary_age_less_65_count', 'beneficiary_dual_count',
             'nonlis_claim_count', 'beneficiary_age_75_84_count',
             'eld_returns', '2010pop',
             'pdp_claim_count', 'lis_claim_count',
             'beneficiary_race_hispanic_count','nppes_provider_last_org_name',
             'nppes_provider_first_name', 'nppes_provider_city',
             'nppes_provider_state', 'zip', 'specialty_description',
             'drug_name', 'generic_name', 'description_flag',
             'ge65_suppress_flag', 'bene_count_ge65_suppress_flag',
             'ge65_suppress_flag', 'nppes_provider_mi',
             'nppes_provider_street2', 'nppes_provider_zip4',
             'brand_suppress_flag', 'generic_suppress_flag',
             'other_suppress_flag', 'mapd_suppress_flag',
             'pdp_suppress_flag', 'lis_suppress_flag',
             'nonlis_suppress_flag', 'antipsych_ge65_suppress_flag',
             'antipsych_bene_ge65_suppress_flg', 'total_claim_count',
             'antipsych_drug_cost_ge65', 'er_opioid_claim_count',
             'antipsych_bene_count_ge65', 'antipsych_claim_count_ge65',
             'er_opioid_day_supply', 'er_opioid_bene_count',
             'opioid_day_supply', 'opioid_bene_count',
             'opioid_prescriber_rate', 'beneficiary_age_65_74_count',
             'land_sq_mi'
            ]

    data.drop(drop_cols, axis=1, inplace=True)

    return data


def make_slim_model():
    pass


def transform_dat():
    pass

def get_Xy(dataframe, target_col, dummy_vars = []):

    data = dataframe.copy()
    data.set_index('npi', inplace=True)

    # Get y labels
    labels = data[target_col]
    data.drop(target_col, axis=1, inplace=True)

    # Create dummy variables
    if dummy_vars != []:
        for col in dummy_vars:
            data = data.join(pd.get_dummies(data[col], drop_first=True))
        data.drop(dummy_vars, axis=1, inplace=True)

    return data, labels

def plot_feature_importances(model, data):

    feature_matrix = pd.DataFrame(data=model.feature_importances_.reshape(1,-1), columns=data.columns)

    feature_matrixT = feature_matrix.T.sort_values(0, ascending=False)

    plt.figure(figsize=(12,9))
    plt.barh(feature_matrixT.index[::-1], feature_matrixT[0].values[::-1]);

def plot_prescribing_characteristics():
    pass
