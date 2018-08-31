
# create table
CREATE DATABASE cms_partb

# switch to database
\c cms_partb

# view tables
\d

# view table headers
\d+ table

# drop TABLE
DROP TABLE partb_util

# create table
CREATE TABLE partb_util
(
  NPI serial,
  NPPES_PROVIDER_LAST_ORG_NAME varchar,
  NPPES_PROVIDER_FIRST_NAME varchar,
  NPPES_PROVIDER_MI varchar,
  NPPES_CREDENTIALS varchar,
  NPPES_PROVIDER_GENDER varchar,
  NPPES_ENTITY_CODE varchar,
  NPPES_PROVIDER_STREET1 varchar,
  NPPES_PROVIDER_STREET2 varchar,
  NPPES_PROVIDER_CITY varchar,
  NPPES_PROVIDER_ZIP varchar,
  NPPES_PROVIDER_STATE varchar,
  NPPES_PROVIDER_COUNTRY varchar,
  PROVIDER_TYPE varchar,
  MEDICARE_PARTICIPATION_INDICATOR varchar,
  PLACE_OF_SERVICE varchar,
  HCPCS_CODE varchar,
  HCPCS_DESCRIPTION varchar,
  HCPCS_DRUG_INDICATOR varchar,
  LINE_SRVC_CNT float,
  BENE_UNIQUE_CNT int,
  BENE_DAY_SRVC_CNT int,
  AVERAGE_MEDICARE_ALLOWED_AMT float,
  AVERAGE_SUBMITTED_CHRG_AMT float,
  AVERAGE_MEDICARE_PAYMENT_AMT float,
  AVERAGE_MEDICARE_STANDARD_AMT float
);

# import text file into table
\copy partb_util_15 (NPI, NPPES_PROVIDER_LAST_ORG_NAME, NPPES_PROVIDER_FIRST_NAME,
  NPPES_PROVIDER_MI, NPPES_CREDENTIALS, NPPES_PROVIDER_GENDER, NPPES_ENTITY_CODE,
  NPPES_PROVIDER_STREET1, NPPES_PROVIDER_STREET2, NPPES_PROVIDER_CITY,
  NPPES_PROVIDER_ZIP, NPPES_PROVIDER_STATE, NPPES_PROVIDER_COUNTRY,PROVIDER_TYPE,
  MEDICARE_PARTICIPATION_INDICATOR, PLACE_OF_SERVICE, HCPCS_CODE,
  HCPCS_DESCRIPTION, HCPCS_DRUG_INDICATOR, LINE_SRVC_CNT, BENE_UNIQUE_CNT,
  BENE_DAY_SRVC_CNT, AVERAGE_MEDICARE_ALLOWED_AMT, AVERAGE_SUBMITTED_CHRG_AMT,
  AVERAGE_MEDICARE_PAYMENT_AMT, AVERAGE_MEDICARE_STANDARD_AMT)
FROM 'CMS_PartB_Provider_Util_Payment_15_noHeader.txt' WITH (FORMAT text);

# import text file into table
\copy partb_util_15 (NPI, NPPES_PROVIDER_LAST_ORG_NAME, NPPES_PROVIDER_FIRST_NAME,                                                                   NPPES_PROVIDER_MI, NPPES_CREDENTIALS, NPPES_PROVIDER_GENDER, NPPES_ENTITY_CODE,                                                                       NPPES_PROVIDER_STREET1, NPPES_PROVIDER_STREET2, NPPES_PROVIDER_CITY,                                                                                  NPPES_PROVIDER_ZIP, NPPES_PROVIDER_STATE, NPPES_PROVIDER_COUNTRY,                                                                                     PROVIDER_TYPE, MEDICARE_PARTICIPATION_INDICATOR, PLACE_OF_SERVICE, HCPCS_CODE,                                                                        HCPCS_DESCRIPTION, HCPCS_DRUG_INDICATOR, LINE_SRVC_CNT, BENE_UNIQUE_CNT,                                                                              BENE_DAY_SRVC_CNT, AVERAGE_MEDICARE_ALLOWED_AMT, AVERAGE_SUBMITTED_CHRG_AMT,                                                                          AVERAGE_MEDICARE_PAYMENT_AMT, AVERAGE_MEDICARE_STANDARD_AMT)                                                                                        FROM 'data/CMS_PartB_Provider_Util_Payment_15_noHeader.txt' WITH (FORMAT text);


CREATE TABLE partd_prescrib
(npi varchar,
  nppes_provider_last_org_name varchar,
  nppes_provider_first_name varchar,
  nppes_provider_city varchar,
  nppes_provider_state varchar,
  specialty_description varchar,
  description_flag varchar,
  drug_name varchar,
  generic_name varchar,
  bene_count varchar,
  total_claim_count varchar,
  total_30_day_fill_count varchar,
  total_day_supply varchar,
  total_drug_cost varchar,
  bene_count_ge65 varchar,
  bene_count_ge65_suppress_flag varchar,
  total_claim_count_ge65 varchar,
  ge65_suppress_flag varchar,
  total_30_day_fill_count_ge65 varchar,
  total_day_supply_ge65 varchar,
  total_drug_cost_ge65 varchar
);

\copy partd_prescrib_15 (npi,nppes_provider_last_org_name,nppes_provider_first_name,nppes_provider_city,nppes_provider_state,specialty_description,description_flag,drug_name,generic_name,bene_count,total_claim_count,total_30_day_fill_count,total_day_supply,total_drug_cost,bene_count_ge65,bene_count_ge65_suppress_flag,total_claim_count_ge65,ge65_suppress_flag,total_30_day_fill_count_ge65,total_day_supply_ge65,total_drug_cost_ge65) FROM 'data/CMS_PartD_Prescriber_NPI_Drug_15_noHeader.txt' WITH (FORMAT text);

CREATE TABLE partd_npi_summ_15 (npi varchar,
  nppes_provider_last_org_name varchar,
  nppes_provider_first_name varchar,
  nppes_provider_mi varchar,
  nppes_credentials varchar,
  nppes_provider_gender varchar,
  nppes_entity_code varchar,
  nppes_provider_street1 varchar,
  nppes_provider_street2 varchar,
  nppes_provider_city varchar,
  nppes_provider_zip5 varchar,
  nppes_provider_zip4 varchar,
  nppes_provider_state varchar,
  nppes_provider_country varchar,
  specialty_description varchar,
  description_flag varchar,
  medicare_prvdr_enroll_status varchar,
  total_claim_count varchar,
  total_30_day_fill_count varchar,
  total_drug_cost varchar,
  total_day_supply varchar,
  bene_count varchar,
  ge65_suppress_flag varchar,
  total_claim_count_ge65 varchar,
  total_30_day_fill_count_ge65 varchar,
  total_drug_cost_ge65 varchar,
  total_day_supply_ge65 varchar,
  bene_count_ge65_suppress_flag varchar,
  bene_count_ge65 varchar,
  brand_suppress_flag varchar,
  brand_claim_count varchar,
  brand_drug_cost varchar,
  generic_suppress_flag varchar,
  generic_claim_count varchar,
  generic_drug_cost varchar,
  other_suppress_flag varchar,
  other_claim_count varchar,
  other_drug_cost varchar,
  mapd_suppress_flag varchar,
  mapd_claim_count varchar,
  mapd_drug_cost varchar,
  pdp_suppress_flag varchar,
  pdp_claim_count varchar,
  pdp_drug_cost varchar,
  lis_suppress_flag varchar,
  lis_claim_count varchar,
  lis_drug_cost varchar,
  nonlis_suppress_flag varchar,
  nonlis_claim_count varchar,
  nonlis_drug_cost varchar,
  opioid_claim_count varchar,
  opioid_drug_cost varchar,
  opioid_day_supply varchar,
  opioid_bene_count varchar,
  opioid_prescriber_rate varchar,
  er_opioid_claim_count varchar,
  er_opioid_drug_cost varchar,
  er_opioid_day_supply varchar,
  er_opioid_bene_count varchar,
  er_opioid_prescriber_rate varchar,
  antibiotic_claim_count varchar,
  antibiotic_drug_cost varchar,
  antibiotic_bene_count varchar,
  antipsych_ge65_suppress_flag varchar,
  antipsych_claim_count_ge65 varchar,
  antipsych_drug_cost_ge65 varchar,
  antipsych_bene_ge65_suppress_flg varchar,
  antipsych_bene_count_ge65 varchar,
  average_age_of_beneficiaries varchar,
  beneficiary_age_less_65_count varchar,
  beneficiary_age_65_74_count varchar,
  beneficiary_age_75_84_count varchar,
  beneficiary_age_greater_84_count varchar,
  beneficiary_female_count varchar,
  beneficiary_male_count varchar,
  beneficiary_race_white_count varchar,
  beneficiary_race_black_count varchar,
  beneficiary_race_asian_pi_count varchar,
  beneficiary_race_hispanic_count varchar,
  beneficiary_race_nat_ind_count varchar,
  beneficiary_race_other_count varchar,
  beneficiary_nondual_count varchar,
  beneficiary_dual_count varchar,
  beneficiary_average_risk_score varchar
);

\copy partd_npi_summ_15 (npi, nppes_provider_last_org_name, nppes_provider_first_name, nppes_provider_mi, nppes_credentials, nppes_provider_gender, nppes_entity_code, nppes_provider_street1, nppes_provider_street2, nppes_provider_city, nppes_provider_zip5, nppes_provider_zip4, nppes_provider_state, nppes_provider_country, specialty_description, description_flag, medicare_prvdr_enroll_status, total_claim_count, total_30_day_fill_count, total_drug_cost, total_day_supply, bene_count, ge65_suppress_flag, total_claim_count_ge65, total_30_day_fill_count_ge65, total_drug_cost_ge65, total_day_supply_ge65, bene_count_ge65_suppress_flag, bene_count_ge65, brand_suppress_flag, brand_claim_count, brand_drug_cost, generic_suppress_flag, generic_claim_count, generic_drug_cost, other_suppress_flag, other_claim_count, other_drug_cost, mapd_suppress_flag, mapd_claim_count, mapd_drug_cost, pdp_suppress_flag, pdp_claim_count, pdp_drug_cost, lis_suppress_flag, lis_claim_count, lis_drug_cost, nonlis_suppress_flag, nonlis_claim_count, nonlis_drug_cost, opioid_claim_count, opioid_drug_cost, opioid_day_supply, opioid_bene_count, opioid_prescriber_rate, er_opioid_claim_count, er_opioid_drug_cost, er_opioid_day_supply, er_opioid_bene_count, er_opioid_prescriber_rate, antibiotic_claim_count, antibiotic_drug_cost, antibiotic_bene_count, antipsych_ge65_suppress_flag, antipsych_claim_count_ge65, antipsych_drug_cost_ge65, antipsych_bene_ge65_suppress_flg, antipsych_bene_count_ge65, average_age_of_beneficiaries, beneficiary_age_less_65_count, beneficiary_age_65_74_count, beneficiary_age_75_84_count, beneficiary_age_greater_84_count, beneficiary_female_count, beneficiary_male_count, beneficiary_race_white_count, beneficiary_race_black_count, beneficiary_race_asian_pi_count, beneficiary_race_hispanic_count, beneficiary_race_nat_ind_count, beneficiary_race_other_count, beneficiary_nondual_count, beneficiary_dual_count, beneficiary_average_risk_score) FROM 'data/CMS_PartD_Prescriber_NPI_Summ_15_noHeader.txt' WITH (FORMAT text);

# select imbruvica prescription information merged with NPI summary table
SELECT * FROM partd_prescrib JOIN partd_npi_summ ON partd_prescrib.npi=partd_npi_summ.npi WHERE drug_name='IMBRUVICA';

# copy selection to csv file
\copy (SELECT * FROM partd_prescrib LEFT JOIN partd_npi_summ ON partd_prescrib.npi=partd_npi_summ.npi WHERE drug_name='IMBRUVICA') TO 'imbruvica_prescrib_npi_summary.txt' DELIMITER E'\t';

\copy (SELECT * FROM partd_prescrib_16 LEFT JOIN partd_npi_summ_16 ON partd_prescrib_16.npi=partd_npi_summ_16.npi WHERE partd_prescrib_16.specialty_description='Hematology/Oncology' OR partd_prescrib_16.specialty_description='Medical Oncology' OR partd_prescrib_16.specialty_description='Hematology' OR partd_prescrib_16.specialty_description='Hematology-Oncology') TO 'data/heme-onc_d_16.csv' CSV HEADER DELIMITER E'\t';

# Alter table names
ALTER TABLE partd_prescrib
RENAME TO partd_prescrib_16;
