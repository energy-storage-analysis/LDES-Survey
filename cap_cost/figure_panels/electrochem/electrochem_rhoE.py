#%%
import os
from os.path import join as pjoin
import pandas as pd
import matplotlib.pyplot as plt
import re
import seaborn as sns

from es_utils.units import read_pint_df
from es_utils.plot import annotate_points, adjust_text_after
from es_utils.chem import format_chem_formula

import matplotlib as mpl
plt.rcParams.update({
    "savefig.facecolor": 'white',
    "font.size": 12, 
    'savefig.dpi': 600, 
    'font.sans-serif': 'arial', 
    'figure.figsize': (7, 10)
})


label_fontsize = 14
marker_size = 50
ADJUST_TEXT_LIM = 5

from adjustText import adjust_text

from dotenv import load_dotenv
load_dotenv()
REPO_DIR = os.getenv('REPO_DIR')

output_dir = 'output'
if not os.path.exists(output_dir): os.makedirs(output_dir)

df = read_pint_df(pjoin(REPO_DIR,'cap_cost/data_consolidated/SM_data.csv'), index_col=[0,1], drop_units=True).reset_index('SM_type')


formula_strings = [format_chem_formula(s) for s in df.index]
df['display_text'] = formula_strings


df['SM_type'] = df['SM_type'].replace('liquid_metal_battery', 'liquid_metal')

Ckwh_cutoff = 30
y_max = Ckwh_cutoff*1.3

#%%

df_ec_synfuel = df.where(df['SM_type'].isin([
'synfuel'
])).dropna(subset=['SM_type'])


SM_type_display = []
for idx, row in df_ec_synfuel.iterrows():
    if row['sub_type'] == 'chemical':
        t = row['SM_type'] + "\n(" + row['sub_type'] + ',\n' + row['mat_type']+ ")"
    else:
        t = row['SM_type'] + "\n(" + row['sub_type'] + ")"

    SM_type_display.append(t)

df_ec_synfuel['SM_type'] = SM_type_display


df_ec_decoupled = df.where(df['SM_type'].isin([
'flow_battery',
])).dropna(subset=['SM_type'])

df_ec_decoupled = pd.concat([
df_ec_synfuel,
df_ec_decoupled
])


# %%
df_ec_coupled = df.where(df['SM_type'].isin([
'coupled_battery',
])).dropna(subset=['SM_type'])

df_ec_coupled = df_ec_coupled.where(df_ec_coupled['C_kwh'] < Ckwh_cutoff).dropna(how='all')
df_ec_decoupled = df_ec_decoupled.where(df_ec_decoupled['C_kwh'] < Ckwh_cutoff).dropna(how='all')

df_ec_coupled.dropna(axis=1, how='all').to_csv(pjoin(output_dir,'SM_coupled_ds.csv'))
df_ec_decoupled.dropna(axis=1, how='all').to_csv(pjoin(output_dir,'SM_decoupled_ds.csv'))



# %%
print("Coupled")

fig = plt.figure()

xlim=(2e-2,2e1)

x_str='specific_energy'
y_str='C_kwh'

sns.scatterplot(data=df_ec_coupled, y=y_str, x=x_str, hue='sub_type', legend=True, s=marker_size)

ax = plt.gca()
ax.hlines(10,*xlim, linestyle='--', color='gray', alpha=0.5)

texts = annotate_points(df_ec_coupled, x_str, y_str, text_col='display_text', ax=ax)

ax.set_title('Coupled')
plt.xlabel('Specific Energy (kWh/kg)', fontsize=label_fontsize)
plt.ylabel("$C_{kWh,mat}$ (\$/kWh)", fontsize=label_fontsize)

plt.yscale('log')
plt.xscale('log')
plt.ylim(top=y_max)
plt.xlim(*xlim)


leg = ax.get_legend()
leg.set_title('Sub Type')
leg.set_bbox_to_anchor([0,0.3,0.5,0])

adjust_text(texts, arrowprops = dict(arrowstyle='->'), force_points=(5,2), lim=ADJUST_TEXT_LIM)

alter_dict = {
    # "Na/NiCl_{2}": (3,14),
    "C_{6}/LMP": (2,20),
    "Ce_{4}/Zn": (0.2,5),
    "Mg/Al": (0.1,8),
    "Mg/Sb": (0.3,18),
    "Mg/Zn": (0.05,15),
}

for alter_name, (x,y) in alter_dict.items():
    adjust_text_after(fig, ax, alter_name, texts, x,y)


plt.savefig(pjoin(output_dir,'ec_rhoE_coupled.png'))


#%%

print("Decoupled")

xlim = (0.1, 60)

fig = plt.figure()

sns.scatterplot(data=df_ec_decoupled, y=y_str, x=x_str, hue='SM_type', legend=True, s=marker_size)

ax = plt.gca()

plt.yscale('log')
plt.xscale('log')
plt.ylim(bottom=9e-3, top=y_max)
plt.xlim(*xlim)

texts = annotate_points(df_ec_decoupled, x_str, y_str, 'display_text', ax=ax)


# plt.gca().get_legend().set_bbox_to_anchor([0,0.6,0.5,0])

ax.set_title('Decoupled')
plt.xlabel('Specific Energy (kWh/kg)', fontsize=label_fontsize)
plt.ylabel("$C_{kWh,mat}$ (\$/kWh)", fontsize=label_fontsize)

leg = ax.get_legend()
leg.set_title('Sub Type')
leg.set_bbox_to_anchor([0,0,1,0.52])

adjust_text(texts, arrowprops = dict(arrowstyle='->'), force_points=(2,1), lim=ADJUST_TEXT_LIM)

ax.hlines(10,*xlim, linestyle='--', color='gray', alpha=0.5)

alter_dict = {
    "CH_{4}\ (Feedstock)": (5,5e-2),
    "Methanol\ (Feedstock)": (40,3e-2),
    "H_{2}\ (Feedstock)": (2,1e-2),
    "CH_{4}\ Spherical\ Pressure": (15,15),

    # "LiBH_{4}": (10,5),
    "Zr(BH_{4})_{4}": (8,5),
    "NaBH_{4}": (8,2),
    "Zn(BH_{4})_{2}": (4,3.5),
    "Mg(BH_{4})_{2}": (15,3),
    "Ca(BH_{4})_{2}": (20,4),
    "Al(BH_{4})_{3}": (20,3),

    "S/Air(Li,\ Acid)": (1.5,3.8),
    "Na_{2}LiAlH_{3}": (1,5),
    "Na_{3}AlH_{3}": (0.5,2),
    "NaAlH_{2}": (1,1.8),
    # "Ti_{12}Mn_{18}H_{30}": (0.5,7),

}


for alter_name, (x,y) in alter_dict.items():
    adjust_text_after(fig, ax, alter_name, texts, x,y)


plt.savefig(pjoin(output_dir,'ec_rhoE_decoupled.png'))

# %%
