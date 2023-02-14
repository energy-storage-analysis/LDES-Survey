#%%
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
from os.path import join as pjoin

from es_utils.units import read_pint_df
from es_utils.plot import annotate_points, draw_arrows, prepare_fixed_texts
from es_utils.chem import format_chem_formula

import matplotlib as mpl
plt.rcParams.update({'font.size':12, 'savefig.dpi': 600})
label_fontsize = 14

from adjustText import adjust_text
from dotenv import load_dotenv
load_dotenv()
REPO_DIR = os.getenv('REPO_DIR')

output_dir = 'output'
if not os.path.exists(output_dir): os.makedirs(output_dir)

MARKER_SIZE=80
Ckwh_cutoff = 50
y_lim = (0.1, 100)

df = read_pint_df(pjoin(REPO_DIR,'cap_cost/data_consolidated/SM_data.csv'), index_col=[0,1], drop_units=True).reset_index('SM_type')


# %%


df_tc = df.where(df['SM_type'] == 'thermochemical').dropna(subset=['SM_type'])
df_tc = df_tc.dropna(axis=1,how='all')
df_tc = df_tc.where(df_tc['C_kwh'] < Ckwh_cutoff).dropna(how='all')


formula_strings = [format_chem_formula(s) for s in df_tc.index]
df_tc['display_text'] = formula_strings


df_tc.dropna(axis=1, how='all').to_csv(pjoin(output_dir,'tc_ds.csv'))

#%%

fig = plt.figure(figsize=(7,8))
x_str='T_turning'
y_str='C_kwh'

xlim = (0,2000)

sns.scatterplot(data=df_tc, y=y_str, x=x_str, hue='mat_type', legend=True, s=MARKER_SIZE)

# df_tc.plot.scatter(y='C_kwh', x=x_str, sharex=False)


ax = plt.gca()

texts = annotate_points(df_tc, x_str,y_str,text_col='display_text', ax=ax)

plt.xlim(*xlim)
leg = plt.gca().get_legend()
leg.set_bbox_to_anchor([0,0,0.3,0.2])
leg.set_title('')

plt.yscale('log')
plt.ylim(y_lim)
# plt.ylim(0,10)

ax.hlines(10,*xlim, linestyle='--', color='gray', alpha=0.5)

plt.xlabel('Turning Temperature (deg C)', fontsize=label_fontsize)
plt.ylabel("$C_{kWh,mat}$ (\$/kWh)", fontsize=label_fontsize)
plt.suptitle("Thermochemcial")
plt.tight_layout()


fix_positions = pd.read_csv('fix_positions_thermochemical.csv', index_col=0)
fix_positions = {name : (row['x'],row['y']) for name, row in fix_positions.iterrows()}

texts, texts_fix, orig_xy = prepare_fixed_texts(texts, fix_positions, ax=ax)
all_texts = [*texts, *texts_fix]

adjust_text(
    texts, 
    force_points=(0.5,3),
    ax=ax,
    add_objects=texts_fix
    )

draw_arrows(all_texts, arrowprops=dict(arrowstyle='->'), ax=ax, orig_xy=orig_xy)

plt.savefig(pjoin(output_dir,'thermochem.png'))
# %%