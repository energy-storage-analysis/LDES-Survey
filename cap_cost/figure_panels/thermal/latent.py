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
ADJUST_TEXT_LIM = 50

CkWh_cases = pd.read_csv(pjoin(REPO_DIR, 'cap_cost','figure_panels','CkWh_cases.csv'), index_col=0)
Ckwh_cutoff = CkWh_cases['value']['MDES']
# Ckwh_cutoff = 100
y_lim = (0.1, Ckwh_cutoff*2)

OVERWRITE_FIX_POSITIONS = True
fn_fix_positions = 'fix_positions_latent.csv'
fix_positions = pd.read_csv(fn_fix_positions, index_col=0)

df = read_pint_df(pjoin(REPO_DIR,'cap_cost/data_consolidated/SM_data.csv'), index_col=[0,1], drop_units=True).reset_index('SM_type')


df['SM_type'] = df['SM_type'].str.replace('_',' ').str.title()
df['sub_type'] = df['sub_type'].str.replace('_',' ').str.title()
df['mat_type'] = df['mat_type'].str.replace('_',' ').str.title()

# %%
df_latent = df.where(df['SM_type'] == 'Latent Thermal').dropna(subset=['SM_type'])
df_latent = df_latent.dropna(axis=1, how='all')
df_latent_ds = df_latent.where(df_latent['C_kwh'] <Ckwh_cutoff).dropna(how='all')

#This drops Boron, with phase change > 2000
df_latent_ds = df_latent_ds.where(df_latent['phase_change_T'] < 2000).dropna(how='all')


display_text = [s.split(' ')[0] for s in df_latent_ds.index]
display_text = [format_chem_formula(s) for s in display_text]
df_latent_ds['display_text'] = display_text

# df_latent_ds.loc['Liquid Air','display_text'] = 'Liquid\ Air\ (LNG\ Tank)'

df_latent_ds.dropna(axis=1, how='all').to_csv(pjoin(output_dir,'latent_ds.csv'))

#%%

fig, ax = plt.subplots(1,1,figsize=(7,8))

xlim=(-220,1800)

# df_latent_ds.plot.scatter(y='C_kwh', x='phase_change_T', c='sp_latent_heat', cmap='jet', sharex=False)
# df_latent_ds.plot.scatter(y='C_kwh', x='phase_change_T', sharex=False, ax=ax)

sns.scatterplot(data=df_latent_ds, y='C_kwh', x='phase_change_T', hue='mat_type',style='mat_type', legend=True, s=MARKER_SIZE)

texts = annotate_points(df_latent_ds, 'phase_change_T', 'C_kwh', 'display_text')


plt.yscale('log')
plt.ylim(y_lim)
plt.xlim(*xlim)


case_lns = []
for case, row in CkWh_cases.iterrows():
    case_lns.append(ax.axhline(row['value'], linestyle=row['linestyle'], color='gray'))


plt.xlabel('Phase Change Temperature (deg C)', fontsize=label_fontsize)

plt.ylabel("$C_{kWh,SM}$ (\$/kWh)", fontsize=label_fontsize)
plt.suptitle("Latent")


texts, texts_fix, orig_xy, orig_xy_fixed = prepare_fixed_texts(texts, fix_positions, ax=ax)

arrows_fix = draw_arrows(texts_fix, arrowprops=dict(arrowstyle='->'), ax=ax, orig_xy=orig_xy_fixed)

if len(texts):

    adjust_text(texts, 
                expand_text = (1.05, 1.3),      #(1.05, 1.2)
                expand_points = (1,1),    #(1.05, 1.2)
                expand_objects = (1.05, 1.2),   #(1.05, 1.2)
                expand_align = (1.05, 1.2),     #(1.05, 1.2)
                force_text= (0.2, 0.2),        #(0.1, 0.25)
                force_points = (0.5, 0.7),      #(0.2, 0.5)
                force_objects = (0.2, 0.2),    #(0.1, 0.25)
                lim=ADJUST_TEXT_LIM, 
                add_objects=[*texts_fix, *arrows_fix], 
                arrowprops=dict(arrowstyle='->')
                )


# draw_arrows(all_texts, arrowprops=dict(arrowstyle='->'), ax=ax, orig_xy=orig_xy)
all_texts = [*texts_fix, *texts]
# from es_utils.plot import adjust_text_after
# adjust_text_after(fig, ax, "LiF/MgF_{2}", all_texts, 650,80)

from es_utils.plot import gen_text_position_fix_csv, combine_fix_pos

if OVERWRITE_FIX_POSITIONS:
    df_text_position = gen_text_position_fix_csv(fix_positions, texts, ax)
    df_text_position = combine_fix_pos(df_latent_ds, df_text_position)
    df_text_position.to_csv(fn_fix_positions)

leg = ax.get_legend()
leg.set_title('')
leg.set_bbox_to_anchor([0,0,0.3,0.3])

plt.tight_layout()

plt.savefig(pjoin(output_dir,'latent.png'))
# %%
