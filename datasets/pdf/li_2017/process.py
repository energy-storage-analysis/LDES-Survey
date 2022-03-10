#%%
import numpy as np
import pandas as pd
import os

from sympy import subsets

chem_lookup = pd.read_csv('chem_lookup.csv', index_col=0)
chem_lookup
# %%
table_3 = pd.read_csv('tables/table_3.csv', index_col=0)
table_3

#%%

present_chemicals = [name for name in table_3.index if name in chem_lookup.index]

table_3['molecular_formula'] = chem_lookup.loc[present_chemicals]['molecular_formula']
table_3['material_name'] = chem_lookup.loc[present_chemicals]['material_name']

added_rows = pd.DataFrame({
    'molecular_formula': ['O2'],
    'ref': [np.nan],
    'specific_price': [0]
}, index = ['Air'])

table_3 = table_3.append(added_rows)

table_3.index.name = 'original_name'

table_3

# %%
table_3.to_csv('output/prices.csv')

#%%
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

df = df.rename({'label':'couple_name'}, axis=1).set_index('couple_name')

#Just calling the two parts of the couple A and B like in Kim 2013. Not even sure if I have anode/cathode correct above. 
df = df.rename({'anode':'A', 'cathode':'B'}, axis=1)

# df['anode'].where(~df['anode'].isin(chem_lookup['molecular_formula'])).dropna()

# %%

df['A'].where(~df['A'].isin(chem_lookup['molecular_formula'])).dropna()
# %%

df['B'].where(~df['B'].isin(chem_lookup['molecular_formula'])).dropna()
# %%


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

df['mu_A'] = [get_molecular_mass(f) for f in df['A']]
df['mu_B'] = [get_molecular_mass(f)for f in df['B']]

#%%

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
df['specific_energy'] = (1/3600)*F*df['deltaV']/(df['mu_A'] + df['mu_B'])

#%%

df.to_csv('output/couples.csv')
# %%
