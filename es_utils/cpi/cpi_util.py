"""
Module for interfacing with cpi package. The package takes forever to load according as outlined in https://github.com/palewire/cpi/issues/37
This module can be run as a script to generate a csv file of the default CPI-U data
"""
#%%
import pandas as pd
import os

folder_path = os.path.dirname(os.path.abspath(__file__))
cpi_data_path = os.path.join(folder_path, 'cpi_factors.csv')

cpi_data = pd.read_csv(cpi_data_path, index_col=0)['factor']

def inf_factor(year):
    return cpi_data[year]


#%%

if __name__ == '__main__':

    df = pd.read_excel('input_data/SeriesReport-20230530190222_1c21f2.xlsx', skiprows=11, index_col=0)

    df.index  = df.index.astype(int)

    cpi_factors = df['Jan'][2023]/df['Jan']


    cpi_factors.index.name = 'year'
    cpi_factors.name = 'factor'

    cpi_factors.to_csv('cpi_factors.csv')
    