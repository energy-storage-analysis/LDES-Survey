#%%
import matplotlib.pyplot as plt
import seaborn as sns
import os
import pandas as pd
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
df_latent = df.where(df['SM_type'] == 'latent_thermal').dropna(subset=['SM_type'])
df_latent = df_latent.dropna(axis=1, how='all')
df_latent_ds = df_latent.where(df_latent['C_kwh'] <Ckwh_cutoff).dropna(how='all')

#This drops Boron, with phase change > 2000
df_latent_ds = df_latent_ds.where(df_latent['phase_change_T'] < 2000).dropna(how='all')


display_text = [s.split(' ')[0] for s in df_latent_ds.index]
display_text = [format_chem_formula(s) for s in display_text]
df_latent_ds['display_text'] = display_text

# df_latent_ds.loc['Liquid Air','display_text'] = 'Liquid\ Air\ (LNG\ Tank)'

df_latent.dropna(axis=1, how='all').to_csv(pjoin(output_dir,'latent_ds.csv'))

#%%

fig, ax = plt.subplots(1,1,figsize=(7,8))

xlim=(-220,1600)

# df_latent_ds.plot.scatter(y='C_kwh', x='phase_change_T', c='sp_latent_heat', cmap='jet', sharex=False)
# df_latent_ds.plot.scatter(y='C_kwh', x='phase_change_T', sharex=False, ax=ax)

sns.scatterplot(data=df_latent_ds, y='C_kwh', x='phase_change_T', hue='mat_type',legend=True, s=MARKER_SIZE)

texts = annotate_points(df_latent_ds, 'phase_change_T', 'C_kwh', 'display_text')


plt.yscale('log')
plt.ylim(y_lim)
plt.xlim(*xlim)

ax.hlines(10,*xlim, linestyle='--', color='gray', alpha=0.5)

plt.xlabel('Phase Change Temperature (deg C)', fontsize=label_fontsize)

plt.ylabel("$C_{kWh,mat}$ (\$/kWh)", fontsize=label_fontsize)
plt.suptitle("Latent")


fix_positions = pd.read_csv('fix_positions_latent.csv', index_col=0)
fix_positions = {name : (row['x'],row['y']) for name, row in fix_positions.iterrows() if row['fix'] == 'y'}

texts, texts_fix, orig_xy = prepare_fixed_texts(texts, fix_positions, ax=ax)
all_texts = [*texts, *texts_fix]

adjust_text(
    texts, 
    force_points=(0.5,1), 
    expand_points=(1.5,1.5), 
    expand_text=(1.2,1.5),
    ax=ax,
    add_objects=texts_fix
    )

draw_arrows(all_texts, arrowprops=dict(arrowstyle='->'), ax=ax, orig_xy=orig_xy)


leg = ax.get_legend()
leg.set_title('')
leg.set_bbox_to_anchor([0,0,0.3,0.2])

plt.tight_layout()

plt.savefig(pjoin(output_dir,'latent.png'))
# %%
