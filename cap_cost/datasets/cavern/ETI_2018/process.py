#%%
import pandas as pd
import os

from es_utils.units import ureg, prep_df_pint_out

if not os.path.exists('output'): os.mkdir('output')
tables = {fn.strip('.csv') : pd.read_csv(os.path.join('tables',fn), encoding='utf-8', index_col=0) for fn in os.listdir('tables')}
#%%

df_1 = tables['table_1'].reset_index(drop=True)
df_1['location'] = 'Yorkshire'
df_1['volume'] = 275000

df_2 = tables['table_2'].reset_index(drop=True)
df_2['location'] = 'Cheshire'
df_2['volume'] = 300000

df_3 = tables['table_3'].reset_index(drop=True)
df_3['location'] = 'Teeside'
df_3['volume'] = 50000
#%%

#Don't include Teeside, as it is not a pressurized cavern

df = pd.concat([df_1,df_2])

df = df.rename({
' PHASE ': 'component', 
'Estimated times per  well / cavern':'time',
' Quantity ': 'quantity',
'Cost (£) per well /  cavern': 'cost_per_well', 
' Totals ':'cost'
}, axis=1)

df = df.set_index('component')

df['cost'] = df['cost'].str.replace("£","").str.replace(",","").astype(int)

df['vol_cost'] = df['cost']/df['volume']

df

#%%


df_leach = df.loc[[c for c in df.index if 'Leach' in c]]



leech_cost = df_leach['vol_cost'].mean()



df_out = pd.DataFrame(columns=['vol_cost'])
df_out.index.name = 'index'

df_out.loc['Salt', 'vol_cost'] = leech_cost

# df_out = df_out.pint.quantify({"vol_cost": "GDP/m**3"}) 
df_out['vol_cost'] = df_out['vol_cost'].astype("pint[GBP/m**3]")

df_out['vol_cost'] = df_out['vol_cost'].pint.to("USD/m**3")

df_out


df_out = prep_df_pint_out(df_out)

df_out.to_csv('output/vol_cost.csv')


# df.to_csv('SM_lookup.csv')
#%%

# df = df.rename({}, axis=1)

# SM_lookup = pd.read_csv('SM_lookup.csv')
# df = pd.merge(df_t3, SM_lookup, on='original_name')
# df = df.dropna(subset=['SM_name'])
# df = df.set_index('SM_name')


# %%

# df.to_csv('output/SM_data.csv')