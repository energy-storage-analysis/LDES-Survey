# EIA data

Data taken from: https://www.eia.gov/electricity/data/eia860/

Accessed on 06-02-2023

We utilize two datasets: 

* 3_1_GeneratorYyyyy: Contains power capacity data for all U.S. Generation systems (including PHES, CAES, Batteries, and Flywheels) 
* 3_4_Energy_StorageYyyyy: Contains energy capacity data for Batteries and Flyhweels. 

The Duration data from the Global Energy Storage Database (See GESDB folder) is used for PHES and CAES. 

The 2021 dataset was downloaded, and placed in the folder `input_data\eia8602021` relative to `process.py`