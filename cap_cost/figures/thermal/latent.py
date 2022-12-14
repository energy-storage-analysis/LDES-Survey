#%%
import matplotlib.pyplot as plt
import seaborn as sns
import os
from os.path import join as pjoin

from es_utils.units import read_pint_df
from es_utils.plot import annotate_points
from es_utils.chem import format_chem_formula

import matplotlib as mpl
mpl.rcParams.update({'font.size':12})
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

df_latent.dropna(axis=1, how='all').to_csv(pjoin(output_dir,'latent_ds.csv'))

#%%

fig, ax = plt.subplots(1,1,figsize=(7,8))


# df_latent_ds.plot.scatter(y='C_kwh', x='phase_change_T', c='sp_latent_heat', cmap='jet', sharex=False)
# df_latent_ds.plot.scatter(y='C_kwh', x='phase_change_T', sharex=False, ax=ax)

sns.scatterplot(data=df_latent_ds, y='C_kwh', x='phase_change_T', hue='mat_type',legend=True, s=MARKER_SIZE)

texts = annotate_points(df_latent_ds, 'phase_change_T', 'C_kwh', 'display_text')


plt.yscale('log')
plt.ylim(y_lim)
plt.xlim(0,1600)

ax.hlines(10,0,1600, linestyle='--', color='gray')

plt.xlabel('Phase Change Temperature (deg C)', fontsize=label_fontsize)

plt.ylabel("$C_{kWh,mat}$ (\$/kWh)", fontsize=label_fontsize)
plt.suptitle("Latent")

adjust_text(texts,  arrowprops = dict(arrowstyle='->'), force_points=(1,-2))

from es_utils.plot import adjust_text_after

alter_dict = {
    "NaCl/NaBr/Na_{2}MoO_{4}": (500,40),
    "K_{2}CO_{3}": (1400, 15),
    "LiF/NaF": (600, 50),
    "Mg": (600, 30),
    "KOH": (250, 25)
}

for alter_name, (x,y) in alter_dict.items():
    adjust_text_after(fig, ax, alter_name, texts, x,y)

leg = ax.get_legend()
leg.set_title('')
leg.set_bbox_to_anchor([0,0,0.3,0.2])

plt.tight_layout()

plt.savefig(pjoin(output_dir,'latent.png'))
# %%
