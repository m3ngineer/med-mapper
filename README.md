# Med Mapper

## Translating claims data into pharmaceutical sales intelligence to improve physician education
As new cancer therapies are approved by the FDA, patients have better therapies which available for treatment. Some of these treatments can significantly improve patient survival and quality of life over traditional therapies. However, busy, overworked doctors may be strained to find time to research the latest drugs and find the best drug for their patient.

Pharmaceutical companies assist in this manner by using their field medical and sales teams to engage with physicians and provide the latest clinical information. However, with greater than 14,000 hematologist and oncologists in the U.S., sales and marketing executives are tasked with determining how to best utilize their sales and marketing resources quickly and effectively.

Med Mappr is a data product that provides intelligence to help patients get the best care possible by helping pharmaceutical companies determine how to disperse their field medical teams to educate physicians. This product identifies doctors who are likely to be early adopters of new therapies and are located in underserved areas. By pinpointing physicians who may be receptive to learning about new medications and targeting underserved areas, Med mappr's mission is to democratize education about therapeutics and ensure doctors have the latest information to treat their patients.

## Unlocking physician prescribing patterns in oncology
Currently, this project focuses on predicting physicians who are early adopters of new oncology treatments. Focusing on Imbruvica, an oral inhibitor of Bruton's tyrosine kinase indicated for the treatment of mantel cell lymphoma and chronic lymphocytic leukemia, I analyzed Medicare claims data to build a gradient boosted classifier model that predicts whether a physician will be a top prescriber in the following year.

This model uses the latest release of Medicare claims data (2016) to recommend physicians that pharmaceutical sales forces should prioritize engagement with.

In order to identify physicians who may be more amenable to changing prescriptions, the prescribing patterns from recommended physicians were further analyzed by clustering.

## About this App
This app was was created using Python and is also hosted via and AWS EC2 instance and S3 bucket. To view the online version of the web app please click [here](http://35.153.218.187/).

The app can also be run locally after installing dependencies and running the following:

<code>
python app.py
</code>

### Product demonstration
Users are able to select their drug of interest.

<img src="/static/img/med-mappr_landing.png" alt="Med Mappr landing page" width="600"/>

Med Mappr returns a list of recommended physicians who have been identified as likely to be high prescribers for the current year. These can be sorted and prioritized by different traits, including name, location, and specialty. Physicians have also been tagged as practicing in rural counties, and can be sorted accordingly.

<img src="/static/img/med-mappr_recommendations.png" alt="Med Mappr recommended physicians for Imbruvica" width="600"/>

Users can survey overall statistics for recommended physicians compared to the all physicians who prescribe Imbruvica. Physicians are also visualized and segmented by location.

<img src="/static/img/med-mappr_results_stats.png" alt="Med Mappr cohort statistics" width="600"/>

<img src="/static/img/med-mappr_results_map.png" alt="Med Mappr cohort statistics" width="600"/>

Users can view additional information about the breakdown of this cohort, including prescriptions based on specialty and claims for drugs that are co-prescribed and competitors of Imbruvica.

<img src="/static/img/med-mappr_results_specialty.png" alt="Med Mappr cohort statistics" width="600"/>

<img src="/static/img/med-mappr_results_claims.png" alt="Med Mappr cohort statistics" width="600"/>

To understand more granular patterns of physician prescribing habits, a heat map visualizes recommended providers based on their change in claims from the previous year. Certain providers have show patterns of possible co-prescription with agents used to reduce side effects known to caused by Imbruvica or with competitor agents.    

<img src="/static/img/med-mappr_results_heatmap.png" alt="Med Mappr cohort statistics" width="600"/>


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
Physician data from 2014 and 2015 processed using pandas and numpy and used to create variables for predictive model. Altogether there were 104 unique variables from Medicare data, and an additional 13 income and population density variables sorted geographically by zipcode.

As data from physicians prescribing with 1-10 counts of a drug were suppressed in the Medicare Part D claims dataset, these empty values were substituted with random integers between 1-10. Non-numerical variables (eg, address, state), with the exception of NPPES specialty, and suppression flags (denoting Medicare suppression of data from physicians with less than 10 counts of a drug) were excluded for modeling purposes. NPPES specialty was collapsed into categorical variables consisting of 'MD', 'MD plus' for physicians with additional advanced degrees beyond an MD, 'NP', 'RN', 'PA', and 'Other'. Zip codes were replaced with income and population density data.

The percentage changes in number of claims for drugs that showed the greatest absolute percent change in prescriptions across all physicians were calculated and included as new variables.

Total claim count data from 2016 was used as the metric for identifying high-prescribing physicians. Providers were classified as a high prescriber if they were in the top quantile of providers.

### Modeling
Modeling was performed using logistic regression, random forest, and gradient boosted classifier using scikit-learn. F1 score, recall, and precision were used as metrics to evaluate and optimize models. Gradient boosted classification model was chosen based on superior scores with 5 K-fold cross validation.

Features were iteratively dropped based on sci-kit learn's feature importances and cross-validating scores without the least important features.

### Deployment
Med Mappr algorithm and web app were deployed with a Flask microframework. App is running on an AWS EC2 instance.

## Results
A gradient boosting model was selected as a top-scoring model based on F1, recall and precision. Variables from 2015 and 2014 data were used to predict whether physicians were in the top quartile of drug claims. Using 2016 test data, 509 physicians were predicted with at least 75% confidence for the year 2017.

Providers were also characterized by whether they served in rural areas. Providers were tagged as serving rural areas if the zipcode they worked in had a density of less than or equal to 1000 people per sq mi. 114 out of 509 prescribers were classified as serving rural populations.

### Feature importances
Using scikit-learn's feature importances algorithm, physicians past prescribing behavior, including spending, number of claims, and percentage change in number of claims from 2014-2015 were the greatest indicators for whether a provider who predicted to be an early adopter. Other factors such as the total costs of drugs prescribed to beneficiaries who are not categorized as eligible for low-income subsidy, total generic drug costs, and ER opioid prescriber rates (the percent of opioids precribed in the ER), and number of beneficiaries who were qualified to only receive Medicare benefits (and not Medicaid) were also indicators.

 - The average total costs of spending for non-low income subsidy beneficiaries was $1.9 million for recommended providers of Imbruvica compared to $0.72 million for all Imbruvica-prescribing physicians. The average number of beneficiaries qualified for only Medicare (and not Medicaid) was 177 for recommended providers of Imbruvica compared to 100 for all Imbruvica-prescribing physicians. These variable may reflect the socioeconomic difference between doctors. For example, physicians serving a greater proportion of low-income households likely have less access to the latest research and educational resources on new drugs.

 High levels of prescriptions overall have been found to be an influential factor in determining early adoption of drugs in [previous studies](https://bmchealthservres.biomedcentral.com/articles/10.1186/1472-6963-14-469). This may be due to these physicians having a diverse patient population, and large number of prescriptions in general.  

 - The average total costs of spending on generic medications was $115,009 for recommended providers of Imbruvica compared to $59,937 for all Imbruvica-prescribing physicians. Total costs of spending for all drugs also showed stark differences, with recommended providers having an average of $2.1 million on Medicare spending, compared to $0.72 million for all Imbruvica-prescribing providers. This may reflect that doctors who prescribe more drugs over all are more likely to prescribe Imbruvica.
 - The average ER opioid prescriber rate was 11.837 for recommended doctors compared to 11.506 for all Imbruvica-prescribing physicians. The reason for this difference is unknown.

The percentage change in other drugs, such as Zytiga, and Jakafi were also scored as important features. Zytiga is a hormone-based chemotherapy indicated for prostate cancer and Jakafi is a medicine used to treat a condition of the bone marrow known as myelofibrosis.  Similar to prescriptions for all drugs, spending and claims for these drugs may be representative of physician prescribing habits over all.

### Overview of characteristics of early adopting physicians
These physicians represented 95.7% more claims for Imbruvica, 99.8% greater Medicare spending, and 95.7% greater spending on all brand drugs, compared to the all physicians who prescribed Imbruvica. Of 3316 physicians who prescribed Imbruvica, these 509 physicians (16.3%) prescribed 35.0% of all claims for Imbruvica, and 35.7% of all spending for the drug.

Physicians were also ordered using hierachical clustering of their percent change in prescribing behavior for Imbruvica and several drugs that are either competitors or commonly prescribed.

Interestingly, a subset of providers who showed increased claims of Imbruvica also showed increased rates of allopurinol claims. Providers often prescribe allopurinol before treatment with Imbruvica to prevent gout, which Imbruvica can increase risk of. Zydelig is also approved for use with chronic lymphocytic leukemia. Clustering analysis depicted several subsets of doctors who showed higher claim rates for Zydelig compared to Imbruvica, and may have opted for this treatment. Rituxan is approved for combination therapy with Imbruvica, however corresponding changes in claims were not observed with Rituxan. This may be because Rituxan is already commonly prescribed by oncologists.

## Conclusion
Med Mappr represents a proof of concept for how prescribing behavior can be inferred from Medicare claims data, while complying with HIPAA patient privacy regulations.

## Future work
Additional features are in progress to improve this project.
 - **Expanding models to encompass other cancer drugs:** Models have been created for Imbruvica, Xarelto, Ibrance, and Revlimid. Creating additional models will improve the utility and applicability of this product to additional markets.
 - **Adding additional data:** This study primarily used Medicare claims data from 2014-2016. Using future releases of claims data from CMS, integrating Medicare Part B data, and adding more granular prescribing data from other data sets would help increase the predictive power of these models.
 - **Physician early adopter score:** Currently, this model provides a list of recommended physicians who are early adopters and are in rural areas. A composite score taking in other information could be useful in prioritizing physicians to engage with.
 - **Physician network:** Physicians can find out about new therapeutics from other doctors. Connections between provider organizations as inferred from research databases can be used to provide recommendations on influencer physicians.
