
#%%
import seaborn as sns
import pandas as pd
import os
from os.path import join as pjoin

from es_utils.units import read_pint_df
from es_utils.plot import annotate_points, draw_arrows, prepare_fixed_texts
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
ADJUST_TEXT_LIM = 50

CkWh_cases = pd.read_csv(pjoin(REPO_DIR, 'cap_cost','figure_panels','CkWh_cases.csv'), index_col=0)
Ckwh_cutoff = CkWh_cases['value']['MDES']
# Ckwh_cutoff = 100
y_lim = (0.005, Ckwh_cutoff*2)
hot_xlim = (0,2100)

OVERWRITE_FIX_POSITIONS = True

df = read_pint_df(pjoin(REPO_DIR,'cap_cost/data_consolidated/SM_data.csv'), index_col=[0,1], drop_units=True).reset_index('SM_type')

df['SM_type'] = df['SM_type'].str.replace('_',' ').str.title()
df['sub_type'] = df['sub_type'].str.replace('_',' ').str.title()
df['mat_type'] = df['mat_type'].str.replace('_',' ').str.title()


# %%
df_sens = df.where(df['SM_type'] == 'Sensible Thermal').dropna(subset=['SM_type'])
df_sens = df_sens.dropna(axis=1, how='all')
df_sens = df_sens.rename({'Vegetable Oil': 'Veg. Oil'})

df_sens_ds = df_sens.where(df_sens['C_kwh'] < Ckwh_cutoff).dropna(how='all')


formula_strings = [format_chem_formula(s) for s in df_sens_ds.index]
df_sens_ds['display_text'] = formula_strings

df_sens_ds['display_text'] = df_sens_ds['display_text'].str.replace('Therminol\ VP_{1}', 'Therminol\ VP1', regex=False)

df_sens_ds.dropna(axis=1, how='all').to_csv(pjoin(output_dir,'sens_ds.csv'))

#%%


df_cold = df_sens_ds[df_sens_ds['sub_type'] == 'Cold']
df_hot = df_sens_ds[~(df_sens_ds['sub_type'] == 'Cold')]

df_hot

#%%


#%%

df_manual = df_hot.loc[['MgO','Graphite']][['C_kwh','T_max']]

df_hot = df_hot.drop('MgO')
df_hot = df_hot.drop('Graphite')

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
ax_cold.set_ylabel("$C_{kWh,SM}$ (\$/kWh)", fontsize=label_fontsize)
ax_cold.set_title("Cold Sensible")

case_lns = []
for case, row in CkWh_cases.iterrows():
    case_lns.append(ax_cold.axhline(row['value'], linestyle=row['linestyle'], color='gray'))

x_str='T_max'
y_str='C_kwh'


#https://stackoverflow.com/questions/225115MARKER_SIZE/gridspec-with-shared-axes-in-python
ax_hot = fig.add_subplot(spec[1:], sharey=ax_cold)
sns.scatterplot(data=df_hot, y=y_str, x=x_str, hue='mat_type',legend=True,ax=ax_hot, s=MARKER_SIZE, style='mat_type')
texts_hot =annotate_points(df_hot, x_str,y_str,text_col='display_text',ax=ax_hot)

leg = ax_hot.get_legend()
leg.set_bbox_to_anchor([0.95,0,0,0.4])
leg.set_title('')

#Custom for values off screen
manual_y = df_manual.loc['MgO']['C_kwh']
ax_hot.text(2000, manual_y, 'MgO', horizontalalignment='right')

manual_y = df_manual.loc['Graphite']['C_kwh']
ax_hot.text(2000, manual_y, 'Graphite', horizontalalignment='right')



ax_hot.set_yscale('log')
# ax_hot.set_ylim(0.05,110)
ax_hot.set_xlim(*hot_xlim)

ax_hot.set_xlabel('Maximum Temperature (deg C)', fontsize=label_fontsize)
# ax_hot.set_ylabel("$C_{kWh,SM}$ (\$/kWh)")
# ax_hot.xticks.remove()
ax_hot.set_title("Hot Sensible")


case_lns = []
for case, row in CkWh_cases.iterrows():
    case_lns.append(ax_hot.axhline(row['value'], linestyle=row['linestyle'], color='gray'))

# fig.tight_layout()
labs = plt.setp(ax_hot.get_yticklabels(), visible=False)
ax_hot.yaxis.label.set_visible(False)

# Adjust cold texts

texts = texts_cold

fn_fix_positions = 'fix_positions_sensible_cold.csv'
fix_positions = pd.read_csv(fn_fix_positions, index_col=0)

texts, texts_fix, orig_xy, orig_xy_fixed = prepare_fixed_texts(texts, fix_positions, ax=ax_cold)

arrows_fix = draw_arrows(texts_fix, arrowprops=dict(arrowstyle='->'), ax=ax_cold, orig_xy=orig_xy_fixed)

if len(texts):
    adjust_text(texts, 
                ax=ax_cold,
                expand_text = (1.05, 1.2),      #(1.05, 1.2)
                expand_points = (2,2),          #(1.05, 1.2)
                expand_objects = (1.05, 1.2),   #(1.05, 1.2)
                expand_align = (1.05, 1.2),     #(1.05, 1.2)
                force_text= (0.2, 0.5),         #(0.1, 0.25)
                force_points = (0.2, 0.5),      #(0.2, 0.5)
                force_objects = (0.1, 0.25),    #(0.1, 0.25)
                lim=ADJUST_TEXT_LIM, 
                add_objects=[*texts_fix, *arrows_fix], 
                arrowprops=dict(arrowstyle='->')
                )
# 


from es_utils.plot import gen_text_position_fix_csv, combine_fix_pos

if OVERWRITE_FIX_POSITIONS:
    df_text_position = gen_text_position_fix_csv(fix_positions, texts, ax_cold)
    df_text_position = combine_fix_pos(df_cold, df_text_position)
    df_text_position.to_csv(fn_fix_positions)

# Adjust hot texts

texts = texts_hot

fn_fix_positions = 'fix_positions_sensible_hot.csv'
fix_positions = pd.read_csv('fix_positions_sensible_hot.csv', index_col=0)

texts, texts_fix, orig_xy, orig_xy_fixed = prepare_fixed_texts(texts, fix_positions, ax=ax_hot)

arrows_fix = draw_arrows(texts_fix, arrowprops=dict(arrowstyle='->'), ax=ax_hot, orig_xy=orig_xy_fixed)

if len(texts):
    adjust_text(texts, 
                ax=ax_hot,
                expand_text = (1.05, 1.2),      #(1.05, 1.2)
                expand_points = (2,2),          #(1.05, 1.2)
                expand_objects = (1.05, 1.2),   #(1.05, 1.2)
                expand_align = (1.05, 1.2),     #(1.05, 1.2)
                force_text= (0.2, 0.5),         #(0.1, 0.25)
                force_points = (0.2, 0.5),      #(0.2, 0.5)
                force_objects = (0.1, 0.25),    #(0.1, 0.25)
                lim=ADJUST_TEXT_LIM, 
                add_objects=[*texts_fix, *arrows_fix], 
                arrowprops=dict(arrowstyle='->')
                )

if OVERWRITE_FIX_POSITIONS:
    df_text_position = gen_text_position_fix_csv(fix_positions, texts, ax_hot)
    df_text_position = combine_fix_pos(df_hot, df_text_position)
    df_text_position.to_csv(fn_fix_positions)

plt.savefig('output/sensible_hotcold.png')
# %%
