#%%
import os
from os.path import join as pjoin
import pandas as pd
import matplotlib.pyplot as plt
import re
import seaborn as sns

from es_utils.units import read_pint_df
from es_utils.plot import annotate_points, draw_arrows, prepare_fixed_texts
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
df['SM_type'] = df['SM_type'].replace('synfuel', 'Synthetic fuel')
df['SM_type'] = df['SM_type'].str.replace('_',' ').str.title()
df['sub_type'] = df['sub_type'].str.replace('_',' ').str.title()
df['mat_type'] = df['mat_type'].str.replace('_',' ').str.title()
df['mat_type'] = df['mat_type'].str.replace('Lohc','LOHC')

Ckwh_cutoff = 30
y_max = Ckwh_cutoff*1.3

#%%

df_ec_synfuel = df.where(df['SM_type'].isin([
'Synthetic Fuel'
])).dropna(subset=['SM_type'])


SM_type_display = []
for idx, row in df_ec_synfuel.iterrows():
    if row['sub_type'] == 'Chemical':
        t = row['SM_type'] + "\n(" + row['mat_type']+ ")"
    else:
        t = row['SM_type'] + "\n(" + row['sub_type'] + ")"

    SM_type_display.append(t)

df_ec_synfuel['SM_type'] = SM_type_display


df_ec_decoupled = df.where(df['SM_type'].isin([
'Flow Battery',
])).dropna(subset=['SM_type'])

df_ec_decoupled = pd.concat([
df_ec_synfuel,
df_ec_decoupled
])


df_ec_decoupled = df_ec_decoupled.where(df_ec_decoupled['C_kwh'] < Ckwh_cutoff).dropna(how='all')

df_ec_decoupled.dropna(axis=1, how='all').to_csv(pjoin(output_dir,'SM_decoupled_ds.csv'))



#%%

print("Decoupled")

xlim = (0.1, 60)

x_str='specific_energy'
y_str='C_kwh'

fig = plt.figure()

sns.scatterplot(data=df_ec_decoupled, y=y_str, x=x_str, hue='SM_type', style='SM_type', legend=True, s=marker_size)

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

ax.hlines(10,*xlim, linestyle='--', color='gray', alpha=0.5)

fix_positions = pd.read_csv('fix_positions_decoupled.csv', index_col=0)
fix_positions = {name : (row['x'],row['y']) for name, row in fix_positions.iterrows() if row['fix'] == 'y'}

texts, texts_fix, orig_xy, orig_xy_fixed = prepare_fixed_texts(texts, fix_positions, ax=ax)

arrows_fix = draw_arrows(texts_fix, arrowprops=dict(arrowstyle='->'), ax=ax, orig_xy=orig_xy_fixed)

adjust_text(texts, force_points=(5,2), lim=ADJUST_TEXT_LIM, add_objects=[*texts_fix, *arrows_fix], arrowprops=dict(arrowstyle='->'))


all_texts = [*texts_fix, *texts]
from es_utils.plot import adjust_text_after
adjust_text_after(fig, ax, "Na_{2}LiAlH_{6}", all_texts, 3,12)

plt.savefig(pjoin(output_dir,'ec_rhoE_decoupled.png'))

# %%



