#%%

import matplotlib.pyplot as plt
import pandas as pd
import os



input_folder = 'input_data/aus'

dfs = []

for fn in os.listdir(input_folder):
    if fn.endswith('xlsx'):
        df = pd.read_excel(os.path.join(input_folder, fn), engine='openpyxl')
    else:
        df = pd.read_csv(os.path.join(input_folder, fn))

    dfs.append(df)

df_aus = pd.concat(dfs)

#%%

input_folder = 'input_data/malaysia'

dfs = []

for fn in os.listdir(input_folder):
    if fn.endswith('xlsx'):
        df = pd.read_excel(os.path.join(input_folder, fn), engine='openpyxl')
    else:
        df = pd.read_csv(os.path.join(input_folder, fn))

    dfs.append(df)

df_mal = pd.concat(dfs)

#%%


df = pd.concat([df_aus, df_mal])





df = df.where(df['Country'].isin(['Australia', 'Malaysia']))

df['Country'].value_counts()

# df
#%%
plt.figure()

df.groupby('Country')['Head (m)'].hist(legend=True)
plt.ylabel('Head (m)')

plt.savefig('figures/head.png')

#%%

plt.figure()
df.groupby('Country')['Combined water to rock ratio'].hist()

print("Mean: {}".format(df['Combined water to rock ratio'].mean()))
print("median: {}".format(df['Combined water to rock ratio'].median()))

plt.savefig('figures/VtoR_all.png')

#%%


plt.figure()
df_sel = df.where(df['Combined water to rock ratio'] < 25)
df_sel.groupby('Country')['Combined water to rock ratio'].hist()


print("Mean: {}".format(df_sel['Combined water to rock ratio'].mean()))
print("median: {}".format(df_sel['Combined water to rock ratio'].median()))

plt.savefig('figures/VtoR_25.png')

#%%


plt.figure()
df_sel = df.where(df['Combined water to rock ratio'] < 10)
df_sel.groupby('Country')['Combined water to rock ratio'].hist()


print("Mean: {}".format(df_sel['Combined water to rock ratio'].mean()))
print("median: {}".format(df_sel['Combined water to rock ratio'].median()))

plt.savefig('figures/VtoR_10.png')

#%%


VR = df['Combined water to rock ratio'].median()
VR

Head = df['Head (m)'].median()

#%%

from es_utils.units import read_pint_df, prep_df_pint_out

df_SM = read_pint_df('SM_def.csv')

df_SM['VtoR'] = VR
df_SM['VtoR'] = df_SM['VtoR'].astype('pint[dimensionless]')


df_SM['delta_height'] = Head
df_SM['delta_height'] = df_SM['delta_height'].astype('pint[m]')

df_SM


if not os.path.exists('output'): os.mkdir('output')

df_SM = prep_df_pint_out(df_SM)

df_SM.to_csv('output/SM_data.csv')