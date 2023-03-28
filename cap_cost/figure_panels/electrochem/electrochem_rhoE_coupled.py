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


# %%
df_ec_coupled = df.where(df['SM_type'].isin([
'Coupled Battery',
])).dropna(subset=['SM_type'])

df_ec_coupled = df_ec_coupled.where(df_ec_coupled['C_kwh'] < Ckwh_cutoff).dropna(how='all')

df_ec_coupled.dropna(axis=1, how='all').to_csv(pjoin(output_dir,'SM_coupled_ds.csv'))



# %%
print("Coupled")

fig = plt.figure()

xlim=(2e-2,2e1)

x_str='specific_energy'
y_str='C_kwh'

sns.scatterplot(data=df_ec_coupled, y=y_str, x=x_str, hue='sub_type', style='sub_type', legend=True, s=marker_size)

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


# Adjusting Texts 

fix_positions = pd.read_csv('fix_positions_coupled.csv', index_col=0)
fix_positions = {name : (row['x'],row['y']) for name, row in fix_positions.iterrows() if row['fix'] == 'y'}

texts, texts_fix, orig_xy, orig_xy_fixed = prepare_fixed_texts(texts, fix_positions, ax=ax)

arrows_fix = draw_arrows(texts_fix, arrowprops=dict(arrowstyle='->'), ax=ax, orig_xy=orig_xy_fixed)

adjust_text(texts, force_points=(5,2), lim=ADJUST_TEXT_LIM, add_objects=[*texts_fix, *arrows_fix], arrowprops=dict(arrowstyle='->'))

plt.savefig(pjoin(output_dir,'ec_rhoE_coupled.png'))