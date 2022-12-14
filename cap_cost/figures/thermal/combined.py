
#%%
import re
import pandas as pd
import seaborn as sns
from es_utils.units import read_pint_df
import os
from os.path import join as pjoin

import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams.update({'font.size':12})
from adjustText import adjust_text

from dotenv import load_dotenv
load_dotenv()
REPO_DIR = os.getenv('REPO_DIR')

output_dir = 'output'
if not os.path.exists(output_dir): os.makedirs(output_dir)

df = read_pint_df(pjoin(REPO_DIR,'cap_cost/data_consolidated/SM_data.csv'), index_col=[0,1], drop_units=True).reset_index('SM_type')

df.index = [re.sub('(\D)(\d)(\D|$)',r'\1_\2\3', s) for s in df.index] #Simple way to format chemical equations as latex. Assumes only time numbers are showing up. 

#%%

df_latent = df.where(df['SM_type'] == 'latent_thermal').dropna(subset=['SM_type'])
df_latent = df_latent.dropna(axis=1, how='all')
df_latent_ds = df_latent.where(df_latent['C_kwh'] < 10).dropna(how='all')

#This drops Boron, with phase change > 2000
df_latent_ds = df_latent_ds.where(df_latent['phase_change_T'] < 2000).dropna(how='all')


df_sens = df.where(df['SM_type'] == 'sensible_thermal').dropna(subset=['SM_type'])
df_sens = df_sens.dropna(axis=1, how='all')
df_sens = df_sens.rename({'Vegetable Oil': 'Veg. Oil'})

df_sens_ds = df_sens.where(df_sens['C_kwh'] < 10).dropna(how='all')


df_tc = df.where(df['SM_type'] == 'thermochemical').dropna(subset=['SM_type'])
df_tc = df_tc.dropna(axis=1,how='all')
df_tc = df_tc.where(df_tc['C_kwh'] < 10).dropna(how='all')
#%%

plt.figure(figsize=(10,8))
x_str='T_oper'
y_str='C_kwh'

df_all = pd.concat([
    df_latent.rename({'phase_change_T': 'T_oper'}, axis=1),
    df_sens.rename({'T_max': 'T_oper'}, axis=1),
    df_tc.rename({'temperature': 'T_oper'}, axis=1),
])

df_all = df_all.dropna(axis=1,how='all')
df_all = df_all.where(df_all['C_kwh'] < 10).dropna(how='all')

sns.scatterplot(data=df_all, y=y_str, x=x_str, hue='SM_type', legend=True)

ax = plt.gca()
texts = []
for name, row in df_all.iterrows():
    x = row[x_str]
    y = row[y_str]
    # name = row['materials']

    txt = ax.text(x,y,"${}$".format(name))
    texts.append(txt)

plt.xlim(0,3500)
# plt.gca().get_legend().set_bbox_to_anchor([0,0,1.3,1])

plt.yscale('log')
plt.ylim(0.05,20)
# plt.ylim(0,10)

plt.xlabel('Reaction Temperature (C)')
plt.ylabel("$C_{kWh,mat}$ (\$/kWh)")
# plt.tight_layout()

# adjust_text(texts, arrowprops = dict(arrowstyle='->'))
plt.savefig(pjoin(output_dir,'all_heat.png'))