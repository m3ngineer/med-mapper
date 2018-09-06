# Med Mapper

## Translating claims data into pharmaceutical sales intelligence
The product marketplace is consistently in flux. Med Mappr is a data product that provides intelligence to help pharmaceutical companies stay ahead of competition. This product supports early product adoption by helping to identify physician engagement opportunities and prioritize use of sales forces.

## Unlocking physician prescribing patterns in oncology
Currently, this project focuses on predicting top-prescribing physicians for oncology drugs. Focusing on Imbruvica, an oral inhibitor of Bruton's tyrosine kinase indicated for the treatment of mantel cell lymphoma and chronic lymphocytic leukemia, I analyzed Medicare claims data to build a gradient boosted classifier model that predicts whether a physician will be a top prescriber in the following year.

This model is then used on the latest release of Medicare claims data to recommend physicians that pharmaceutical sales forces should prioritize engagement with.

In order to identify physicians who may be more amenable to changing prescriptions, the prescribing patterns from recommended physicians were further analyzed by clustering.

## Solution
Users are able to select their drug of interest.

<img src="/static/img/med-mappr_landing.png" alt="Med Mappr landing page" width="600"/>

Med Mappr returns a list of recommended physicians who have been identified as likely to be high prescribers for the current year.

<img src="/static/img/med-mappr_recommendations.png" alt="Med Mappr recommended physicians for Imbruvica" width="600"/>

Users can survey overall statistics for recommended physicians compared to the all physicians who prescribe Imbruvica. Physicians are also visualized and segmented by location.

<img src="/static/img/med-mappr_stats.png" alt="Med Mappr cohort statistics" width="600"/>

Live app can be found [here](http://35.153.218.187/).

## About the data
This project utilizes [Medicare Part D claims data](https://www.cms.gov/Research-Statistics-Data-and-Systems/Statistics-Trends-and-Reports/Medicare-Provider-Charge-Data/Part-D-Prescriber.html) released by the Center for Medicare and Medicaid Services. Detailed data and accompanying provider summary tables from years 2014 - 2016 were used for analysis.

Additional income and population density data for geographic zipcodes were obtained from the [Internal Revenue Service](https://www.irs.gov/statistics/soi-tax-stats-individual-income-tax-statistics-2015-zip-code-data-soi) and U.S. Census data compiled by [Jon Bitter](https://blog.splitwise.com/2014/01/06/free-us-population-density-and-unemployment-rate-by-zip-code/).

### Limitations of dataset
As this data represents only beneficiaries with Medicare Part D coverage, this information does not encompass physician prescribing information for beneficiaries with alternative coverage. Therefore, the analyses and models presented by this project may not represent the overall prescribing patterns of physicians and likely underestimate the use overall use of products in the national population.

Additionally, claims may be submitted under multiple NPIs, such as organizational NPIs. In these cases, a provider's true prescribing totals cannot be accurately identified.

### Data suppression and redaction
In order to protect patient privacy of Medicare patients, only claims data was aggregated by physician and only information concerning claims greater than ten were included in the data.

## Methods

### Data storage
Data was downloaded from the Center for Medicare and Medicaid Services public-access files [Medicare Part D Provider Utilization and Payment Dataset](https://www.cms.gov/Research-Statistics-Data-and-Systems/Statistics-Trends-and-Reports/Medicare-Provider-Charge-Data/Part-D-Prescriber.html). Detailed data and accompanying provider summary tables from years 2014 - 2016 were used for analysis. Data was stored in SQL database and queried.

This project focused specifically on hematology and oncology drugs. Data was subsetted by selecting providers with a `specialty_description` of 'Hematology', 'Hematology-Oncology', or 'Medical Oncology', representing about ~246k rows.

Medicare detailed provider data consisted of 21 variables organized by a unique identifying ID for each provider known as a National Provider Identifier (NPI). Data from these tables included zipcode and institution, specialty, drug name, total claims, number of beneficiaries, and total costs for each drug.

Medicare NPI summary tables consisted of 89 variables overall drug utilization information organized by NPI. Data from these tables included total claims, brand and generic drug costs, and beneficiary demographic statistics.

### Data processing and feature selection
Data was processed using pandas and numpy.

### Modeling

### Data Analysis

### Deployment

## Results

## Future work
