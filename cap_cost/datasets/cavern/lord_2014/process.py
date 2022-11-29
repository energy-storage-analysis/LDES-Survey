#%%

import pandas as pd

df_table1 = pd.read_csv('tables/table_1.csv', index_col=0).T
df_table2 = pd.read_csv('tables/table_2.csv', index_col=0).T
# %%
df_table1 = df_table1.loc[['Salt Cavern','Hard Rock']]
df_table2 = df_table2.loc[['Salt Cavern','Hard Rock']]
# %%


df = pd.concat([
df_table1[['Void Volume (m3) ']],
df_table2[['Mining costs ($/m3)', 'Leaching Plant Costs (M$)']]
], axis=1)

df = df.rename({
'Void Volume (m3) ': 'volume',
'Mining costs ($/m3)': 'mining_costs', 
'Leaching Plant Costs (M$)': 'leaching_plant'
}, axis=1)

df = df.rename({
'Salt Cavern': 'Salt',
'Hard Rock': 'LRC', 
}, axis=0)

df.index.name = 'index'

for col in df.columns:
    df[col] = df[col].str.replace(',','')
    df[col] = df[col].astype(float)


df['leaching_plant'] = df['leaching_plant']*1e6 #Price was in millions of dollars
df['leaching_plant'] = df['leaching_plant'].fillna(0)

df['leaching_plant_vol'] = df['leaching_plant']/df['volume']

df['vol_cost'] = df['mining_costs'] #+ df['leaching_plant_vol']

#%%

frac_mining = df['mining_costs']/(df['mining_costs'] + df['leaching_plant_vol'])

with open('output/frac_mining.txt', 'w') as f:

    f.write('Fraction of mining costs: {}'.format(frac_mining.loc['Salt']))


#%%

df.columns.name = ''
# %%

from es_utils.units import prep_df_pint_out

df_out = df[['vol_cost']]
df_out['vol_cost'] = df_out['vol_cost'].astype('pint[USD/m**3]')
df_out

df_out = prep_df_pint_out(df_out)

df_out.to_csv('output/vol_cost.csv')