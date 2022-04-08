#%%
import pandas as pd
import os

if not os.path.exists('output'): os.mkdir('output')
tables = {fn.strip('.csv') : pd.read_csv(os.path.join('tables',fn), encoding='utf-8', index_col=0) for fn in os.listdir('tables')}

df = pd.concat(tables.values(), axis=1)

#TODO: Not including phase change T to not include in latent thermal calcs, because some pahse change T are below 200C. Should have latent T downselection happen after this. 
df = df[['type','decomposition_T','mass_density','Cp','C_kwh_orig']]
df

df.index.name = 'SM_name'

SM_lookup = pd.read_csv('SM_lookup.csv', index_col=0)

df = pd.merge(df, SM_lookup, on='SM_name')

df['SM_type'] ='sensible_thermal'


df.loc['NaMgCaCl', 'Cp'] = '1117.2' #TODO: This has a quadratic temp dependence which messes things up, calculating by hand for 500K

df

# %%
df_Cp = df['Cp'].str.split("([+-])", expand=True)
df_Cp[0] = df_Cp[0].astype(float)
df_Cp[1] = df_Cp[1].fillna('+')
df_Cp[2] = df_Cp[2].str.strip('T').astype(float).fillna(0)

Cps = []
for idx, row in df_Cp.iterrows():
    sign = row[1]
    if sign == '+':
        Cp = row[0] + row[2]
    if sign == '-':
        Cp = row[0] - row[2]

    Cps.append(Cp)

s_Cps = pd.Series(Cps, index=df_Cp.index)
s_Cps

#%%

df_dens = df['mass_density'].str.split("([+-])", expand=True)
df_dens[0] = df_dens[0].astype(float)
df_dens[1] = df_dens[1].fillna('+')
df_dens[2] = df_dens[2].str.strip('T').astype(float).fillna(0)

densities = []
for idx, row in df_dens.iterrows():
    sign = row[1]
    if sign == '+':
        dens = row[0] + row[2]
    if sign == '-':
        dens = row[0] - row[2]

    densities.append(dens)

s_densities = pd.Series(densities, index=df_dens.index)
s_densities
# df_Cp[0].astype(float) +df_Cp[1].str.strip('T').astype(float)*500
# %%

df['Cp'] = s_Cps
df['mass_density'] = s_densities

df['Cp'] = df['Cp']/3600000

#%%

df['decomposition_T'] = df['decomposition_T'].str.strip('>').astype(float)

# %%
df.to_csv('output/SM_data.csv')