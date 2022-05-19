#%%
import pandas as pd
import os

import es_utils

from es_utils.units import convert_units, prep_df_pint_out, ureg

tables = {fn.strip('.csv') : pd.read_csv(os.path.join('tables',fn), encoding='utf-8') for fn in os.listdir('tables')}



df = pd.concat(tables.values())

df = df.rename({
    'Materials': 'original_name',
    'Electrode System (1,2)': 'num_electrodes',
    'Specific Capacitance (F·g-1)': 'specific_capacitance',
    'Potential Range (V)': 'deltaV_electrolyte'
}, axis=1)

df = df.dropna(subset=['specific_capacitance'])

df = df.set_index('original_name')

# %%
from es_utils.pdf import average_range

df['specific_capacitance'] = df['specific_capacitance'].astype(str).apply(average_range)

#%%


if not os.path.exists('output'): os.mkdir('output')

df.to_csv('output/processed.csv')

#%%

SM_lookup = pd.read_csv('SM_lookup.csv', index_col=0)

df_SMs = df[['specific_capacitance', 'deltaV_electrolyte']]

df_SMs = pd.merge(
    SM_lookup,
    df_SMs,
    on='original_name'
    
)

df_SMs = df_SMs.reset_index(drop=True).set_index('SM_name') #Dropping original name as so similar to SM name


df_SMs['specific_capacitance'] = df_SMs['specific_capacitance'].astype(float)

df_out = pd.concat([
df_SMs.groupby(level=0)['specific_capacitance'].mean(),
df_SMs.groupby(level=0)['deltaV_electrolyte'].mean(),
df_SMs.groupby(level=0)['SM_type'].apply(es_utils.join_col_vals),
df_SMs.groupby(level=0)['mat_basis'].apply(es_utils.join_col_vals),
df_SMs.groupby(level=0)['materials'].apply(es_utils.join_col_vals),
], axis=1)


df_out = df_out.astype({
    'specific_capacitance': 'pint[F/g]',
    'deltaV_electrolyte': 'pint[V]'
    })


df_out = convert_units(df_out)
df_out = prep_df_pint_out(df_out)


df_out.to_csv('output/SM_data.csv')