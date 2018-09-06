# Med Mapper

## Translating claims data into pharmaceutical sales intelligence
The product marketplace is consistently in flux. Med Mappr is a data product that provides intelligence to help pharmaceutical companies stay ahead of competition. This product supports early product adoption by helping to identify physician engagement opportunities and prioritize use of sales forces.

## Unlocking physician prescribing patterns in oncology
Currently, this project focuses on predicting top-prescribing physicians for oncology drugs. Focusing on Imbruvica, an oral inhibitor of Bruton's tyrosine kinase indicated for the treatment of mantel cell lymphoma and chronic lymphocytic leukemia, I analyzed Medicare claims data to build a gradient boosted classifier model that predicts whether a physician will be a top prescriber in the following year.

This model is then used on the latest release of Medicare claims data to recommend physicians that pharmaceutical sales forces should prioritize engagement with.

In order to identify physicians who may be more amenable to changing prescriptions, the prescribing patterns from recommended physicians were further analyzed by clustering.

Live app can be found [here](http://35.153.218.187/).

## About the data
This project utilizes [Medicare Part D claims data](https://www.cms.gov/Research-Statistics-Data-and-Systems/Statistics-Trends-and-Reports/Medicare-Provider-Charge-Data/Part-D-Prescriber.html) released by the Center for Medicare and Medicaid Services. In order to protect patient privacy of Medicare patients, only claims data was aggregated by physician and only information concerning claims greater than ten were included in the data.
