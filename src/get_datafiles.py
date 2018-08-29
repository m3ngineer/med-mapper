from subprocess import call
import os
import pandas as pd
import numpy as np

def get_datafiles(drug_names, filename, partb_d='d'):
    '''
    partb_d: 'b' if dataset is from Medicare Part B or 'd' if dataset is from Medicare Part D
    '''

    print('Initiating...')

    for drug in drug_names:
        if partb_d == 'b':
            filename_for_drug = 'data/drugs/part' + partb_d + '/' + drug.replace(' ', '') + '_16.txt'
        elif partb_d == 'd':
            filename_for_drug = 'data/drugs/part' + partb_d + '/' + drug.lower() + '_16.txt'
        command = "ack {} {} > {}".format(drug, filename, filename_for_drug)
        print('Processing {}...'.format(filename_for_drug))
        os.system(command)

    print('Complete.')

def get_totals(files, columns, output_filename, partb_d='d'):
    '''
    Input: Takes in files for drugs of interest

    Output: Outputs CSV with identification of physician as a high prescriber for each drug
    '''

    print('Initiating...')
    final_df = pd.DataFrame(columns=['npi'])
    for file in files:
        if partb_d == 'd':
            filename = 'data/drugs/partd/' + file
        elif partb_d == 'b':
            filename = 'data/drugs/partb/' + file
        df = pd.read_csv(filename, delimiter='\t')

        #Add columns
        if partb_d == 'd':
            df2 = pd.read_csv('data/CMS_PartD_Prescriber_NPI_Drug_CY2016_100.txt', delimiter='\t')
            col_names=df2.columns
            df.columns = col_names
        elif partb_d == 'b':
            col_names = pd.read_csv('data/CMS_PartB_Provider_Util_Payment_CY2016_100.txt', delimiter='\t').columns
            df.columns = col_names

        if 'NPI' in df.columns:
            df.rename(columns={'NPI': 'npi'}, inplace=True)

        if len(columns) == 1:
            cols = ['npi'] + columns
        elif len(columns) > 1:
            cols = ['npi'] + columns


        df = df[cols]
        if partb_d == 'b':
            df['total_drug_cost'] = df['LINE_SRVC_CNT'] * df['AVERAGE_SUBMITTED_CHRG_AMT']
            df = df[['npi', 'total_drug_cost']]
            df.rename(columns={'total_drug_cost': file[:-3]}, inplace=True)
        if partb_d == 'd':
            df.rename(columns={column: file[:-3]}, inplace=True)
        final_df = pd.merge(final_df, df, on='npi', how='outer')

    final_df.to_csv(output_filename, sep='\t')

    print('Complete.')

if __name__ == '__main__':
    filename_b = 'data/CMS_PartB_Provider_Util_Payment_CY2016.txt'
    filename_d = 'data/CMS_PartD_Prescriber_NPI_Drug_CY2016.txt'
    partd_drug_names = ['REVLIMID', 'IMBRUVICA', 'IBRANCE', 'JAKAFI', 'XTANDI', 'GLEEVEC',
       'ZYTIGA', 'POMALYST', 'TASIGNA', 'SPRYCEL', 'IMATINIB MESYLATE',
       'TARCEVA', 'AFINITOR', 'PROMACTA', 'PROCRIT', 'JADENU', 'NEXAVAR',
       'NINLARO', 'SUTENT', 'XARELTO']

    partb_drug_names = ['J2505', 'J9310', '99214', 'J9299', 'J0897', '96413', 'J9035',
       'J0881', '99213', 'J0885', 'J2469', 'J1568', '78815', 'J9041',
       '99215', 'J9263', 'J9999', 'J1439', '85025', '96367']

    #get_datafiles(partd_drug_names, filename_d)
    #get_datafiles(partb_drug_names, filename_b, 'b')

    files_b = os.listdir('data/drugs/partb')
    files_d = os.listdir('data/drugs/partd')

    #get_totals(files_d, ['total_drug_cost'], 'data/drugs/partd_totals.txt')
    get_totals(files_b, ['LINE_SRVC_CNT', 'AVERAGE_SUBMITTED_CHRG_AMT'], 'data/drugs/partb_totals.txt', partb_d='b')
