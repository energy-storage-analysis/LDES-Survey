#%%
from os.path import join as pjoin
import os
import pandas as pd
import numpy as np

from es_utils.units import convert_units, prep_df_pint_out, ureg

if not os.path.exists('output'): os.mkdir('output')


#%%

# Obtian the price of steel from the main dataset to use for the basis of the relative prices. 

from os.path import join as pjoin
from es_utils.units import read_pint_df

from dotenv import load_dotenv
load_dotenv()
REPO_DIR = os.getenv('REPO_DIR')

df_mat_data = read_pint_df(pjoin(REPO_DIR, 'cap_cost/data_consolidated/mat_data.csv'), index_col=0, drop_units=True)

steel_price = df_mat_data.loc['Steel', 'specific_price']


#%%

#Table A1
df_a1 = pd.read_csv(pjoin('tables','table_a1.csv'), skiprows=[1])

df_a1 = df_a1.rename({
    'Material': 'original_name',
    'Relative cost': 'relative_cost',
    'Yield strength': 'yield_strength'
},axis=1)

df_a1['specific_price'] = df_a1['relative_cost']*steel_price



df_a1 = df_a1.astype({
    'specific_price': 'pint[USD/kg]',
    'yield_strength': 'pint[MPa]',
    'density': 'pint[g/cm**3]'
    })

# df_a1['density'] = df_a1['density'].pint.to('kg/m**3')


df_a1['specific_strength'] = df_a1['yield_strength']/df_a1['density']


#Table A2
df_a2 = pd.read_csv(pjoin('tables','table_a2.csv'), skiprows=[1])

df_a2 = df_a2.rename({
    'Material': 'original_name',
    'relative cost': 'relative_cost',
},axis=1)

df_a2['specific_price'] = df_a2['relative_cost']*steel_price 

df_a2 = df_a2.astype({
    'specific_price': 'pint[USD/kg]',
    'sigma_theta_C': 'pint[MPa]',
    'sigma_theta_T': 'pint[MPa]',
    'density': 'pint[g/cm**3]'
    })

#from Kamf thesis it seems like the hoop stress is limiting on a simple approximation level. 1. Kamf, T. (2012). High speed flywheel design
df_a2['specific_strength'] = df_a2['sigma_theta_T']/df_a2['density']

col_select = ['original_name', 'specific_strength','specific_price']

df = pd.concat([
    df_a1[col_select],
    df_a2[col_select],
])
#%%
mat_lookup = pd.read_csv('mat_lookup.csv', index_col=0)

from es_utils.chem import process_mat_lookup
mat_lookup = process_mat_lookup(mat_lookup)

df_mat = pd.merge(df, mat_lookup, on='original_name')

#For the mat data, we group by price index

df_mat = df_mat.set_index('index')

df_mat_grouped = df_mat.groupby('index')[['specific_strength', 'specific_price']].mean() #TODO: can't think of another way to handle multiple entries for given class of material (i.e. steel)

from es_utils import join_col_vals
df_mat_grouped['original_name']= df_mat.groupby('index')['original_name'].apply(join_col_vals)
df_mat_grouped['molecular_formula']= df_mat.groupby('index')['molecular_formula'].apply(join_col_vals)

#We remove the price of steel as it is relative to the database
df_mat_grouped.loc['Steel','specific_price'] = np.nan

df_mat_grouped = convert_units(df_mat_grouped)
df_mat_grouped = prep_df_pint_out(df_mat_grouped)
df_mat_grouped.to_csv('output/mat_data.csv')

#%%

SM_lookup = pd.read_csv('SM_lookup.csv', index_col=0)

df_SMs = df[['original_name', 'specific_strength']]#.set_index('original_name')

#No SM lookup needed as SM are just just the materials
df_SMs = pd.merge(
    SM_lookup,
    df_SMs,
    on='original_name'
)

df_SMs = df_SMs.set_index('SM_name')

#From Nomura (pressure tank from Laughlin assuming thin wall)
Qmaxs = {
    'pressure_tank': 1,
    'flywheel': 1.2,
    'smes': 1.5 #Solenoid average
}

dfs = []

for SM_type, Qmax in Qmaxs.items():
    df_temp = df_SMs.copy()
    df_temp['Qmax'] = Qmax
    df_temp['SM_type'] = SM_type
    dfs.append(df_temp)

# df_temp['Qmax'] = df_temp['Qmax'].astype('pint[dimensionless]')

df_temp = df_temp.astype({'Qmax': 'pint[dimensionless]'})

df_SMs = pd.concat(dfs)
#%%

df_SMs.index.name = 'SM_name'


df_SMs = convert_units(df_SMs)
df_SMs = prep_df_pint_out(df_SMs)
df_SMs.to_csv('output/SM_data.csv')

# %%
