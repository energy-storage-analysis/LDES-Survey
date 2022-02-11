import pandas as pd
import matplotlib.pyplot as plt
from os.path import join as pjoin

def load_tables(folder_path='.'):
    tables = {}

    #Table A1
    df_a1 = pd.read_csv(pjoin(folder_path,'table_a1.csv'), skiprows=[1])

    df_a1 = df_a1.rename({
        'Relative cost': 'cost',
        'Yield strength': 'yield_strength'
    },axis=1)

    df_a1['cost'] = df_a1['cost']*1 #assume relative cost to 1$/kg

    df_a1['specific_strength'] = df_a1['yield_strength']/df_a1['density']
    df_a1['specific_strength'] = df_a1['specific_strength']/3600  

    df_a1['C_kwh'] = df_a1['cost']/df_a1['specific_strength']

    tables['a1'] = df_a1

    #Table A2
    df_a2 = pd.read_csv(pjoin(folder_path,'table_a2.csv'), skiprows=[1])

    df_a2['cost'] = df_a2['relative cost']*1 #assume relative cost to 1$/kg

    #TODO: What is T and C? 
    df_a2['sigma_theta_avg'] = (df_a2['sigma_theta_T'].astype(float) + df_a2['sigma_theta_C'].astype(float))/2

    #TODO: from Kamf thesis it seems like the hoop stress is limiting on a simple approximation level. 
    df_a2['specific_strength'] = df_a2['sigma_theta_avg']/df_a2['density']
    df_a2['specific_strength'] = df_a2['specific_strength']/3600  

    df_a2['C_kwh'] = df_a2['cost']/df_a2['specific_strength']

    tables['a2'] = df_a2

    return tables

if __name__ == '__main__':

    tables = load_tables()

    tables['a1']['C_kwh'].hist(label='metals')
    tables['a2']['C_kwh'].hist(label='composite')

    plt.xlabel('$/kwh')

    plt.legend()
