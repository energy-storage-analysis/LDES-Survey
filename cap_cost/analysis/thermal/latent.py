#%%
import matplotlib.pyplot as plt
import seaborn as sns
from es_utils.units import read_pint_df
import os
from os.path import join as pjoin

import matplotlib as mpl
mpl.rcParams.update({'font.size':12})
from adjustText import adjust_text

from dotenv import load_dotenv
load_dotenv()
REPO_DIR = os.getenv('REPO_DIR')

output_dir = 'output'
if not os.path.exists(output_dir): os.makedirs(output_dir)

df = read_pint_df(pjoin(REPO_DIR,'cap_cost/data_consolidated/SM_data.csv'), index_col=[0,1], drop_units=True).reset_index('SM_type')
# %%
df_latent = df.where(df['SM_type'] == 'latent_thermal').dropna(subset=['SM_type'])
df_latent = df_latent.dropna(axis=1, how='all')
df_latent_ds = df_latent.where(df_latent['C_kwh'] < 100).dropna(how='all')

#This drops Boron, with phase change > 2000
df_latent_ds = df_latent_ds.where(df_latent['phase_change_T'] < 2000).dropna(how='all')

#%%

fig, ax = plt.subplots(1,1,figsize=(7,8))


# df_latent_ds.plot.scatter(y='C_kwh', x='phase_change_T', c='sp_latent_heat', cmap='jet', sharex=False)
df_latent_ds.plot.scatter(y='C_kwh', x='phase_change_T', sharex=False, ax=ax)



texts = []
for name, row in df_latent_ds.iterrows():
    x = row['phase_change_T']
    y = row['C_kwh']
    name = name.split(' ')[0]

    txt = ax.text(x, y, "${}$".format(name))
    texts.append(txt)


plt.yscale('log')
plt.ylim(0.1,200)
plt.xlim(0,1600)

ax.hlines(10,0,1600, linestyle='--', color='gray')

plt.xlabel('Phase Change Temperature (deg C)')

plt.ylabel("$C_{kWh,mat}$ (\$/kWh)")
plt.suptitle("Latent")

adjust_text(texts,  arrowprops = dict(arrowstyle='->'), force_points=(5,10))


plt.tight_layout()

plt.savefig(pjoin(output_dir,'latent.png'))
# %%
