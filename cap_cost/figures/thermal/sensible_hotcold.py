
#%%
import re
import seaborn as sns
import os
from os.path import join as pjoin

from es_utils.units import read_pint_df
from es_utils.plot import annotate_points, adjust_text_after
from es_utils.chem import format_chem_formula

import matplotlib.pyplot as plt
import matplotlib as mpl
plt.rcParams.update({'font.size':12, 'savefig.dpi': 600})
label_fontsize = 14


from adjustText import adjust_text, get_bboxes, get_midpoint

from dotenv import load_dotenv
load_dotenv()
REPO_DIR = os.getenv('REPO_DIR')

output_dir = 'output'
if not os.path.exists(output_dir): os.makedirs(output_dir)

MARKER_SIZE=80
Ckwh_cutoff = 50
y_lim = (0.005, 100)


df = read_pint_df(pjoin(REPO_DIR,'cap_cost/data_consolidated/SM_data.csv'), index_col=[0,1], drop_units=True).reset_index('SM_type')



# %%
df_sens = df.where(df['SM_type'] == 'sensible_thermal').dropna(subset=['SM_type'])
df_sens = df_sens.dropna(axis=1, how='all')
df_sens = df_sens.rename({'Vegetable Oil': 'Veg. Oil'})

df_sens_ds = df_sens.where(df_sens['C_kwh'] < Ckwh_cutoff).dropna(how='all')


formula_strings = [format_chem_formula(s) for s in df_sens_ds.index]
df_sens_ds['display_text'] = formula_strings

df_sens_ds.dropna(axis=1, how='all').to_csv(pjoin(output_dir,'sens_ds.csv'))

#%%


df_cold = df_sens_ds[df_sens_ds['sub_type'] == 'cold']
df_hot = df_sens_ds[~(df_sens_ds['sub_type'] == 'cold')]

df_hot

#%%


#%%
# fig, axes = plt.subplots(1,2)
fig = plt.figure(figsize=(13.5,5), constrained_layout=True)
spec = fig.add_gridspec(1,4)

x_str='T_min'
y_str='C_kwh'

ax_cold = fig.add_subplot(spec[0,0])
sns.scatterplot(data=df_cold, y=y_str, x=x_str, color='gray',legend=True, ax=ax_cold, s=MARKER_SIZE)
texts_cold =annotate_points(df_cold, x_str,y_str,text_col='display_text',ax=ax_cold)

ax_cold.set_yscale('log')
ax_cold.set_ylim(y_lim)
ax_cold.set_xlim(-200,0)

ax_cold.set_xlabel('Min Temperature (deg C)', fontsize=label_fontsize)
ax_cold.set_ylabel("$C_{kWh,mat}$ (\$/kWh)", fontsize=label_fontsize)
ax_cold.set_title("Cold Sensible")


x_str='T_max'
y_str='C_kwh'


#https://stackoverflow.com/questions/225115MARKER_SIZE/gridspec-with-shared-axes-in-python
ax_hot = fig.add_subplot(spec[1:], sharey=ax_cold)
sns.scatterplot(data=df_hot, y=y_str, x=x_str, hue='mat_type',legend=True,ax=ax_hot, s=MARKER_SIZE)
texts_hot =annotate_points(df_hot, x_str,y_str,text_col='display_text',ax=ax_hot)


ax_hot.set_yscale('log')
# ax_hot.set_ylim(0.05,110)
ax_hot.set_xlim(0,2400)

ax_hot.set_xlabel('Maximum Temperature (deg C)', fontsize=label_fontsize)
# ax_hot.set_ylabel("$C_{kWh,mat}$ (\$/kWh)")
# ax_hot.xticks.remove()
ax_hot.set_title("Hot Sensible")

labs = plt.setp(ax_hot.get_yticklabels(), visible=False)
ax_hot.yaxis.label.set_visible(False)


adjust_text(texts_cold,  arrowprops = dict(arrowstyle='->'), 
force_points=(0,5),
force_text=(0,10),
force_objects=(0,5),
ax=ax_cold
)


alter_dict = {
    "Ethanol": (-80,5),
    "Isopentane": (-190,90),
    "N-propane": (-180,0.5),
    'Methanol': (-100,1),
    'N-pentane': (None,30),
    'N-hexane': (-80,30),
    'LN_{2}': (-190,30),
}


for alter_name, (x,y) in alter_dict.items():
    adjust_text_after(fig, ax_cold, alter_name, texts_cold, x,y)

ax_cold.hlines(10,-200,0, linestyle='--', color='gray', alpha=0.5)

adjust_text(texts_hot,  arrowprops = dict(arrowstyle='->'), force_points=(0.2,1), expand_points=(1.5,1.5), expand_text=(1.1,1.4))

alter_dict = {
# "NaKMgCl": (900, 2),
"Basalt": (1000, 0.02),
"LiNaKNO_{3}NO_{2}": (550, 60),
"Al": (800, 60),
"HITEC\ XL": (570, 20),
"Veg.\ Oil": (200, 20),
"NaKMgCl": (1100, 1),
# "KMgCl": (900, 5),
}

for alter_name, (x,y) in alter_dict.items():
    adjust_text_after(fig, ax_hot, alter_name, texts_hot, x,y)

ax_hot.get_legend().set_title('')

ax_hot.hlines(10,0,2400, linestyle='--', color='gray', alpha=0.5)
# fig.tight_layout()

plt.savefig('output/sensible_hotcold.png')
# %%
