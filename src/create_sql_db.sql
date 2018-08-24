
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
\copy partb_util (NPI, NPPES_PROVIDER_LAST_ORG_NAME, NPPES_PROVIDER_FIRST_NAME,
  NPPES_PROVIDER_MI, NPPES_CREDENTIALS, NPPES_PROVIDER_GENDER, NPPES_ENTITY_CODE,
  NPPES_PROVIDER_STREET1, NPPES_PROVIDER_STREET2, NPPES_PROVIDER_CITY,
  NPPES_PROVIDER_ZIP, NPPES_PROVIDER_STATE, NPPES_PROVIDER_COUNTRY,PROVIDER_TYPE,
  MEDICARE_PARTICIPATION_INDICATOR, PLACE_OF_SERVICE, HCPCS_CODE,
  HCPCS_DESCRIPTION, HCPCS_DRUG_INDICATOR, LINE_SRVC_CNT, BENE_UNIQUE_CNT,
  BENE_DAY_SRVC_CNT, AVERAGE_MEDICARE_ALLOWED_AMT, AVERAGE_SUBMITTED_CHRG_AMT,
  AVERAGE_MEDICARE_PAYMENT_AMT, AVERAGE_MEDICARE_STANDARD_AMT)
FROM 'CMS_PartB_Provider_Util_Payment_CY2016_noHeader.txt' WITH (FORMAT text);

# import text file into table
\copy partb_util (NPI, NPPES_PROVIDER_LAST_ORG_NAME, NPPES_PROVIDER_FIRST_NAME,                                                                   NPPES_PROVIDER_MI, NPPES_CREDENTIALS, NPPES_PROVIDER_GENDER, NPPES_ENTITY_CODE,                                                                       NPPES_PROVIDER_STREET1, NPPES_PROVIDER_STREET2, NPPES_PROVIDER_CITY,                                                                                  NPPES_PROVIDER_ZIP, NPPES_PROVIDER_STATE, NPPES_PROVIDER_COUNTRY,                                                                                     PROVIDER_TYPE, MEDICARE_PARTICIPATION_INDICATOR, PLACE_OF_SERVICE, HCPCS_CODE,                                                                        HCPCS_DESCRIPTION, HCPCS_DRUG_INDICATOR, LINE_SRVC_CNT, BENE_UNIQUE_CNT,                                                                              BENE_DAY_SRVC_CNT, AVERAGE_MEDICARE_ALLOWED_AMT, AVERAGE_SUBMITTED_CHRG_AMT,                                                                          AVERAGE_MEDICARE_PAYMENT_AMT, AVERAGE_MEDICARE_STANDARD_AMT)                                                                                        FROM 'CMS_PartB_Provider_Util_Payment_CY2016_noHeader.txt' WITH (FORMAT text);


CREATE TABLE partd_prescrib
(npi serial,
  nppes_provider_last_org_name varchar,
  nppes_provider_first_name varchar,
  nppes_provider_city varchar,
  nppes_provider_state varchar,
  specialty_description varchar,
  description_flag varchar,
  drug_name varchar,
  generic_name varchar,
  bene_count float,
  total_claim_count float,
  total_30_day_fill_count, float
  total_day_supply float,
  total_drug_cost float,
  bene_count_ge65 float,
  bene_count_ge65_suppress_flag varchar,
  total_claim_count_ge65 int,
  ge65_suppress_flag varchar,
  total_30_day_fill_count_ge65 float,
  total_day_supply_ge65 float,
  total_drug_cost_ge65 float
);

\copy partd_prescrib (npi,
  nppes_provider_last_org_name,
  nppes_provider_first_name,
  nppes_provider_city,
  nppes_provider_state,
  specialty_description,
  description_flag,
  drug_name,
  generic_name,
  bene_count,
  total_claim_count,
  total_30_day_fill_count,
  total_day_supply,
  total_drug_cost,
  bene_count_ge65,
  bene_count_ge65_suppress_flag,
  total_claim_count_ge65,
  ge65_suppress_flag,
  total_30_day_fill_count_ge65,
  total_day_supply_ge65,
  total_drug_cost_ge65)
  FROM 'CMS_PartD_Prescriber_NPI_Drug_CY2016.txt' WITH (FORMAT text);
