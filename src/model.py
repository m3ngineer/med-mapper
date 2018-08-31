import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def clean_data(filename):

    print('Reading file...')
    data = pd.read_csv(filename, delimiter='\t')

    # add new features before columns are dropped
    print('Creating new features...')
    new_features = add_new_features(data)

    print('Collapsing unecessary features...')
    data = data[['npi', 'nppes_provider_zip5', 'generic_drug_cost', 'mapd_drug_cost', 'pdp_drug_cost', 'lis_drug_cost',
       'nonlis_drug_cost', 'opioid_claim_count', 'opioid_drug_cost',
       'er_opioid_drug_cost', 'er_opioid_prescriber_rate',
       'beneficiary_female_count', 'beneficiary_male_count',
       'beneficiary_average_risk_score',
       'antibiotic_claim_count',
       'antibiotic_bene_count', 'beneficiary_race_white_count','beneficiary_nondual_count']]
    data = data.drop_duplicates()

    # Fill null values from cost columns with median cost
    cols_fillna = ['generic_drug_cost', 'mapd_drug_cost', 'pdp_drug_cost', 'lis_drug_cost',
                  'nonlis_drug_cost', 'opioid_drug_cost', 'er_opioid_drug_cost', 'er_opioid_prescriber_rate']
    for col in cols_fillna:
        data[col].fillna(data[col].median(), inplace=True)

    # Fill null values from count columns with random numbers between 0-10
    cols_fillna = ['opioid_claim_count', 'beneficiary_female_count', 'beneficiary_average_risk_score',
                  'beneficiary_male_count', 'antibiotic_claim_count', 'antibiotic_bene_count',
                  'beneficiary_race_white_count', 'beneficiary_nondual_count']
    for col in cols_fillna:
        mask = data[col].isnull()
        data.loc[mask, col] = data.loc[mask, col].apply(lambda v: np.random.choice(range(1,11)))


    # Add additional data from IRS and 2010 Census on zipcode demographics
    # Data processed in zipcode_data.ipynb
    zip_data = pd.read_csv('data/zip_data.csv', delimiter='\t')
    zip_data = zip_data.iloc[:,1:]  # drop unnamed column
    zip_data.drop(['agi', 'agi_stub'], axis=1, inplace=True)

    # rename Imbruvica zipcode5 column to merge with zipcode data
    data.rename(columns={'nppes_provider_zip5': 'zip'}, inplace=True)

    # merge zipcode demographic data and new features data into Medicare data
    data = pd.merge(data, zip_data, on='zip')
    data.drop('zip', axis=1, inplace=True)

    data = pd.merge(data, new_features, how='left')
    data.fillna(0, inplace=True) #fillna created from new_features join

    data.set_index('npi', inplace=True)
    print('Complete.')

    return data

def add_new_features(data):

    #data.set_index('npi', inplace=True) #added this because index isn't npi when file read in

    npis = data.npi.values
    hp_features = pd.DataFrame(data=npis, columns=['npi']).set_index('npi')

    partd_drugs = ['REVLIMID', 'IMBRUVICA', 'IBRANCE', 'JAKAFI', 'XTANDI', 'GLEEVEC',
           'ZYTIGA', 'POMALYST', 'TASIGNA', 'SPRYCEL', 'IMATINIB MESYLATE',
           'TARCEVA', 'AFINITOR', 'PROMACTA', 'PROCRIT', 'JADENU', 'NEXAVAR',
           'NINLARO', 'SUTENT', 'XARELTO']

    for drug in partd_drugs:
        features = data.loc[data['drug_name'] == 'REVLIMID', ['npi', 'total_drug_cost', 'total_claim_count']].set_index('npi')

        # Create high prescriber feature per drug
        drug_hp = drug + '_HP'
        features[drug_hp] = 0
        features.loc[features['total_drug_cost'] >= features['total_drug_cost'].quantile(0.75), drug_hp] = 1

        # rename columns
        drug_costs = drug + '_costs'
        drug_claims = drug + '_claims'
        features.rename(columns={'total_drug_cost': drug_costs, 'total_claim_count': drug_claims}, inplace=True)

        hp_features = hp_features.join(features)

    # add feature for all drug costs
    total_costs_all_drugs = pd.DataFrame(data=data.groupby('npi').sum()['total_drug_cost']).rename(columns={'total_drug_cost': 'total_costs_all_drugs'})
    hp_features = hp_features.join(total_costs_all_drugs)

    # add feature for high prescriber overall
    hp_features['overall_hp'] = 0
    hp_features.loc[hp_features['total_costs_all_drugs'] >= hp_features['total_costs_all_drugs'].quantile(0.75), 'overall_hp'] = 1

    hp_features.fillna(0, inplace=True)
    hp_features.drop_duplicates(inplace=True)
    hp_features.reset_index(inplace=True)

    return hp_features


def get_Xy(dataframe, labels, dummy_vars = []):
    '''
    Input: Takes in clean dataframe with index as 'npi' and merges labels (high_prescrib, 'npi' as index) from future data

    Output: Returns X dataframe and y labels
    '''

    data = dataframe.copy()

    # Merge labels into data and fill na values from prescribers who did not prescribe target drug with 0
    data = data.join(labels, how='left')
    data.fillna({'high_prescrib': 0}, inplace=True)
    y = data.high_prescrib
    data.drop('high_prescrib', axis=1, inplace=True)

    # Create dummy variables
    if dummy_vars != []:
        for col in dummy_vars:
            data = data.join(pd.get_dummies(data[col], drop_first=True))
        data.drop(dummy_vars, axis=1, inplace=True)

    X = data

    return X, y

def get_high_prescribers(filename, drug, partb_d='d', cutoff=0.75):
    data = pd.read_csv(filename, delimiter='\t')

    if partb_d == 'd':
        data = data[['npi', 'total_drug_cost', 'drug_name']]
        data = data[data['drug_name'] == 'IMBRUVICA']
    elif partb_d == 'b':
        pass

    data['high_prescrib'] = 0
    quant = data.loc[:, 'total_drug_cost'].quantile(cutoff)
    npi_hp = data[data['total_drug_cost'] > quant].index.values
    data.loc[npi_hp, 'high_prescrib'] = 1

    labels = data.drop(['total_drug_cost', 'drug_name'], axis=1).set_index('npi')

    return labels


def plot_feature_importances(model, data):

    feature_matrix = pd.DataFrame(data=model.feature_importances_.reshape(1,-1), columns=data.columns)

    feature_matrixT = feature_matrix.T.sort_values(0, ascending=False)

    plt.figure(figsize=(12,20))
    plt.barh(feature_matrixT.index[::-1], feature_matrixT[0].values[::-1]);

def plot_prescribing_characteristics():
    pass

def create_dictionary_npis(filename):
    '''
    Input: Takes in raw csv file of providers ('data/heme-onc_d_15.csv')

    Ouptut: Returns a dictionary of npi, provider information, zipcode and
    '''

    df = pd.read_csv(filename, delimiter='\t')
    df = df[['npi', 'nppes_provider_last_org_name', 'nppes_provider_first_name',
       'nppes_provider_city', 'nppes_provider_state', 'specialty_description', 'nppes_provider_zip5']]
    df.rename(columns={'nppes_provider_city': 'city', 'nppes_provider_first_name': 'first_name', 'nppes_provider_last_org_name': 'last_name', 'nppes_provider_state': 'state', 'nppes_provider_zip5': 'zip', 'specialty_description': 'speciality'}, inplace=True)
    df.drop_duplicates(inplace=True)
    df.set_index('npi', inplace=True)

    npi_dict = df.to_dict('index')

    return npi_dict
