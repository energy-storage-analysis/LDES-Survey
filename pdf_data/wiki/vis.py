
#%%
import pandas as pd
import matplotlib.pyplot as plt
import sys
sys.path.append('..')
import pdf_utils
# %%

df = pd.read_csv('wiki_specific_strength.csv')

df = df.rename({
'Material': 'material', 
'Tensile strength  (MPa)': 'strength', 
'Density  (g/cm3)': 'density',
'Specific strength (kN·m/kg)': 'specific_strength', 
'Breaking length (km)': 'breaking_length', 
'Source': 'ref'    
}, axis=1)

df
df['specific_strength'] = df['specific_strength'].str.replace('–N/A','')
df['breaking_length'] = df['breaking_length'].str.replace('–N/A','')
df = df.drop(41)

from pdf_utils import average_range


# for column in df.columns:
#     df[column] = df[column].apply(average_range)

df = df.dropna(subset=['specific_strength'])

df['specific_strength'] = df['specific_strength'].apply(average_range)
df['specific_strength'] = df['specific_strength'].astype(float)
df
#
#%%

df['specific_strength'].hist(bins=100)
# %%
df_nocarbon = df.iloc[0:37]
df_nocarbon
df_nocarbon['specific_strength'].hist(bins=10)