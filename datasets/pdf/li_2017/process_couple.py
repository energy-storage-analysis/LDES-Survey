#%%
import pandas as pd
import os

from sympy import subsets

chem_lookup = pd.read_csv('output/chem_lookup.csv', index_col=0)
chem_lookup
# %%
df = pd.read_csv('tables/table_2.csv')

df = df.dropna(how='all')

df = df.drop('ref',axis=1)

df['type'] = df['type'].str.replace('\n','')

df = df.rename({'C_kwh': 'C_kwh_orig'}, axis=1)

df['ancat'] = df['ancat'].str.replace('\n','')
df['ancat'] = df['ancat'].str.replace('F-','Fe') #TODO: looks like regex to replace 'e' in table extraction accidentally gets Fe with charge \d+-, but don't want to change without testing other tables. 


df['ancat'] = df['ancat'].str.replace('Cu0','Cr')
df['ancat'] = df['ancat'].str.replace('Fe0','Fe')


df['ancat'] = df['ancat'].str.replace('9,10-Anthraquinone-2,7-disulphonic acid', 'C14H8O8S2') #AQDS
df['ancat'] = df['ancat'].str.replace('- S', 'S')
df['ancat'] = df['ancat'].str.replace('2-/Fe2+ Zn(OH)4', 'Zn(OH)4/Fe', regex=False)


df_1 = df.iloc[:29]
df_2 = df.iloc[29:]

df_1['ancat'] = df_1['ancat'].str.replace('\d[+-]','', regex=True)
df_2['ancat'] = df_2['ancat'].str.replace('-','', regex=False)
df_2['ancat'] = df_2['ancat'].str.replace(' ','', regex=False)

df_2['ancat'] = df_2['ancat'].str.replace('0.3Li2MnO30.7LiMn0.5Ni0.5O2','(Li2MnO3)0.3(LiMn0.5Ni0.5O2)0.7', regex=False)



df= pd.concat([df_1,df_2])


df[['anode', 'cathode']] = df['ancat'].str.split('/', expand=True)

#TODO: rexamine these manual substitutions
df['anode'] = df['anode'].str.replace("^S2$", "S", regex=True) # Sulfur air batteries have S2/O2. But price just uses 'S'
df['cathode'] = df['cathode'].str.replace("NiOOH", "Ni(OH)2") # Assume similar enough?
df['cathode'] = df['cathode'].str.replace("PbO2", "Pb") # Assume same cost (Pb cost is provided)
df['cathode'] = df['cathode'].str.replace("NiCl2", "NiCl2(H2O)6") # TODO: figure out how to handle hydrates in cost data.

df = df.drop(42) #TODO: PPY-AC formula is weird and not sure how to deal with price


# df['anode'].where(~df['anode'].isin(chem_lookup['molecular_formula'])).dropna()

# %%

df['anode'].where(~df['anode'].isin(chem_lookup['molecular_formula'])).dropna()
# %%

df['cathode'].where(~df['cathode'].isin(chem_lookup['molecular_formula'])).dropna()
# %%


df_prices = pd.read_csv('output/process.csv')
df_prices = df_prices.dropna(subset = ['molecular_formula']).set_index('molecular_formula')
s_prices = df_prices['specific_price']

#%%
import numpy as np
df['anode_price'] = [s_prices[f] if f in s_prices.index else np.nan for f in df['anode']]
df['cathode_price'] = [s_prices[f] if f in s_prices.index else np.nan for f in df['cathode']]
df
# %%
from pyvalem.formula import Formula
import chemparse

def get_molecular_mass(f):
    element_dict = chemparse.parse_formula(f)
    
    total_mm = 0
    for element, amount in element_dict.items():
        element_mm = Formula(element).rmm
        total_mm += element_mm*amount

    return total_mm

df['anode_mm'] = [get_molecular_mass(f) for f in df['anode']]
df['cathode_mm'] = [get_molecular_mass(f)for f in df['cathode']]

#%%

#TODO: chech this equation
#TODO: should we be including the O2 for the air price, artificially lowers as we are not actually buying those kg. 
df['specific_price'] = (df['anode_price']*df['anode_mm'] + df['cathode_price']*df['cathode_mm'])/(df['anode_mm']+df['cathode_mm'])

#%%
df['type'].value_counts().index

#%%

F = 96485 # C/mol

#TODO: revisit, numbers just made up

deltaV_lookup = {
'Li ion  (C6 anode)': 3, 
'Zn2+ based': 1, 
'Redox flow': 1, 
'Lithium metal': 3,
'Flow-air': 1, 
'High temperature': 1, 
'Li ion  (Si anode)': 3, 
'Pb acid': 1, 
'NiCd': 1 ,
'NiMH': 1, 
'Mg2+ based': 1, 
'Na ion (nonaqueous)': 3, 
'Na ion (aqueous)' : 1
}



df['deltaV'] = [deltaV_lookup[t] for t in df['type']]

#assume z = 1
df['specific_energy'] = (1/3600)*F*df['deltaV']/(df['anode_mm'] + df['cathode_mm'])

#%%

df['C_kwh'] = df['specific_price']/df['specific_energy']

#%%

df.to_csv('output/process_couples.csv')
# %%
