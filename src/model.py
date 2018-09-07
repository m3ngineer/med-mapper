import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from src.dashboard import *
import pickle
from sklearn.ensemble import GradientBoostingClassifier

def clean_data(filename):
    '''
    Input: Takes in the name of a file to clean data on for modeling
    Output: Returns dataframe with relevant new features including total drug costs and total claim counts for select drugs, total costs of all drugs, and percent change in claims from 2014-2015 for select products, and income and population density data by zipcode.
    '''

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
    zip_data.drop(['agi', 'agi_stub', 'n_returns_wages', 'total_income_amt', 'n_return_total_inc', 'n_returns'], axis=1, inplace=True)

    # rename zipcode5 column to merge with zipcode data
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
    '''
    Input: Takes in dataframe of data to engineer
    Output: Returns dataframe with new features including total drug costs and total claim counts for select drugs, total costs of all drugs, and percent change in claims from 2014-2015 for select products
    '''

    #data.set_index('npi', inplace=True) #added this because index isn't npi when file read in

    npis = data.npi.values
    hp_features = pd.DataFrame(data=npis, columns=['npi']).set_index('npi')


    partd_drugs = ['REVLIMID', 'IMBRUVICA', 'IBRANCE', 'JAKAFI', 'XTANDI', 'GLEEVEC',
           'ZYTIGA', 'POMALYST', 'TASIGNA', 'SPRYCEL', 'IMATINIB MESYLATE',
           'TARCEVA', 'AFINITOR', 'PROMACTA', 'PROCRIT', 'JADENU', 'NEXAVAR',
           'NINLARO', 'SUTENT', 'XARELTO']

    for drug in partd_drugs:
        features = data.loc[data['drug_name'] == drug, ['npi', 'total_drug_cost', 'total_claim_count']].set_index('npi')

        '''
        # Create high prescriber feature per drug
        drug_hp = drug + '_HP'
        features[drug_hp] = 0
        features.loc[features['total_drug_cost'] >= features['total_drug_cost'].quantile(0.75), drug_hp] = 1
        '''

        # rename columns
        drug_costs = drug + '_costs'
        drug_claims = drug + '_claims'
        features.rename(columns={'total_drug_cost': drug_costs, 'total_claim_count': drug_claims}, inplace=True)

        hp_features = hp_features.join(features)

    # add feature for all drug costs
    total_costs_all_drugs = pd.DataFrame(data=data.groupby('npi').sum()['total_drug_cost']).rename(columns={'total_drug_cost': 'total_costs_all_drugs'})
    hp_features = hp_features.join(total_costs_all_drugs)

    '''
    # add feature for high prescriber overall
    hp_features['overall_hp'] = 0
    hp_features.loc[hp_features['total_costs_all_drugs'] >= hp_features['total_costs_all_drugs'].quantile(0.75), 'overall_hp'] = 1
    '''

    # ADD IN NEW features
    # Load in 2014 and 2015 data
    data15 = pd.read_csv('data/heme-onc_d_15.csv', delimiter='\t')
    data14 = pd.read_csv('data/heme-onc_d_14.csv', delimiter='\t')

    # Create pivot tables of NPI x Drug claim counts
    data14_claims = data14.loc[:, ['npi', 'total_claim_count', 'drug_name']]
    data14_claims_drugs = pd.pivot_table(data14_claims, index='npi', columns='drug_name', values='total_claim_count', fill_value=0)
    data15_claims = data15.loc[:, ['npi', 'total_claim_count', 'drug_name']]
    data15_claims_drugs = pd.pivot_table(data15_claims, index='npi', columns='drug_name', values='total_claim_count', fill_value=0)

    # Create transformed table with difference in claims from 2014 to 2015
    claims_1514_diff = (((data15_claims_drugs + 1) - (data14_claims_drugs + 1)) / (data14_claims_drugs + 1))
    claims_1514_diff.fillna(0, inplace=True)

    # Identify drugs that saw the greatest percentage change across all heme-oncs from 2014 - 2015
    drugs_greatest_change = claims_1514_diff.sum().sort_values(ascending=False)[:40].index.values

    # Create dataframe with percent changes in claims for these drugs
    perc_delta_claims_1415 = claims_1514_diff[drugs_greatest_change]

    # Update column names before merging with other features
    drugs_greatest_change_cols = [drug + '_PCC' for drug in drugs_greatest_change]
    perc_delta_claims_1415.columns = drugs_greatest_change_cols

    # Add in new claims percentage drug features
    hp_features = hp_features.join(perc_delta_claims_1415, how='left')

    #Clean hp_features before return
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
        data = data[data['drug_name'] == drug]
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

def drop_duplicate_SQL_cols(data_filename, write_to_filename):
    '''
    Drop duplicate columns generated by merging Medicare PartD presciption information with NPI Summary Statistics table
    Outputs tab-delimited csv file with dropped columns
    '''

    df = pd.read_csv(data_filename, delimiter='\t')

    drop_cols = ['nppes_provider_last_org_name.1',
            'npi.1',
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
            'bene_count_ge65.1',
            'bene_count_ge65_suppress_flag.1'
            ]

    df.drop(drop_cols, axis=1, inplace=True)
    df.to_csv(write_to_filename, sep='\t')

class NewDrugModel:
    '''
    Input:
        Provide drug name as 'str'

    Output:
        Export model and dashboard data to 'src/model' and 'src/dashboard/'
    '''

    def __init__(self, drug_name):
        self.drug = drug_name.upper()
        self.NPI_dict = pickle.load(open('src/dashboard/npi_2016.pkl', 'rb'))
        self.X_train = pickle.load(open('src/dashboard/data_heme-onc_d_15_clean.pkl', 'rb'))
        self.X_test = pickle.load(open('src/dashboard/data_heme-onc_d_16_clean.pkl', 'rb'))
        self.labels = get_high_prescribers('data/heme-onc_d_16.csv', drug_name.upper())
        self.y_train = None
        self.model = GradientBoostingClassifier()
        self.clf = None
        self.high_prob_npis = None
        self.high_prescriber_dict = None

    def fit(self):
        self.X_train, self.y_train = get_Xy(self.X_train, self.labels)
        self.clf = self.model.fit(self.X_train, self.y_train)

        return self.clf

    def export_model(self):
        filename = 'src/models/model_' + self.drug.lower() + '.pkl'
        pkl_model = open(filename, 'wb')
        pickle.dump(self.clf, pkl_model)
        pkl_model.close()

    def export_dashboard_data(self, cutoff=0.75):
        predictions = self.clf.predict(self.X_test)
        prob_hp = self.clf.predict_proba(self.X_test)[:, 1]

        # get npis that are high confidence high prescribers
        self.high_prob_npis = self.X_test[prob_hp > cutoff].index.values

        # Create dictionary of predicted high prescribers
        self.high_prescriber_dict = {k: self.NPI_dict[k] for k in self.high_prob_npis}

        # Include probabilities of high prescriber in dictionary
        prob_hp_arr = np.concatenate([self.X_test.index.values.reshape(-1,1), prob_hp.reshape(-1,1)], axis=1)
        prob_hp_dict = {npi_prob[0]: npi_prob[1] for npi_prob in prob_hp_arr}

        for npi in self.high_prob_npis:
            if npi in prob_hp_dict:
                self.high_prescriber_dict[npi]['prob'] = "{:.2f}%".format(prob_hp_dict[npi] * 100)

        # Export cohort stats and graphJSON in order to make app more efficient
        print('Generating JSON data for graph...')
        self.graphJSON = show_map(self.high_prescriber_dict)
        print('Generating cohort statistics...')
        self.cohort_stats = get_cohort_stats(self.high_prob_npis, 'https://s3.amazonaws.com/medmappr-data/heme-onc_d_16.csv', self.drug)

        print('Exporting files...')
        filename_cs = 'src/dashboard/dashboard_cohort_stats_17_' + self.drug.lower() + '.pkl'
        filename_gj = 'src/dashboard/dashboard_graphJSON_17_' + self.drug.lower() + '.pkl'
        pickle.dump(self.cohort_stats, open(filename_cs, 'wb'))
        pickle.dump(self.graphJSON, open(filename_gj, 'wb'))
        print('Complete.')
