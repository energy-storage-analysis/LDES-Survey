"""
Module for interfacing with cpi package. The package takes forever to load according as outlined in https://github.com/palewire/cpi/issues/37
This module can be run as a script to generate a csv file of the default CPI-U data
"""
#%%
import pandas as pd
import os

from dotenv import load_dotenv
load_dotenv()
REPO_DIR = os.getenv('REPO_DIR')

DISABLE_CPI = False

def get_cpi_data(base_year = 2023):

    fp_cpi_input = os.path.join(REPO_DIR,'es_utils', 'cpi','input_data','SeriesReport-20230530190222_1c21f2.xlsx' )
    df = pd.read_excel(fp_cpi_input, skiprows=11, parse_dates=True, index_col=0)

    cpi_factors = df['Jan'][base_year]/df['Jan']

    cpi_factors.index = pd.to_datetime(cpi_factors.index.astype(int), format = "%Y") 
    cpi_factors.index = cpi_factors.index.year

    cpi_factors.index.name = 'year'

    cpi_factors.name = 'cpi_factor'

    if DISABLE_CPI:
        cpi_factors.loc[:] = 1

    return cpi_factors