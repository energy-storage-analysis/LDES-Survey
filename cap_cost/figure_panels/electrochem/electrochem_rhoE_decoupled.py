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


from adjustText import adjust_text
from dotenv import load_dotenv
load_dotenv()
REPO_DIR = os.getenv('REPO_DIR')

import matplotlib as mpl
plt.rcParams.update({
    "savefig.facecolor": 'white',
    "font.size": 12, 
    'savefig.dpi': 600, 
    'font.sans-serif': 'arial', 
    'figure.figsize': (7, 10)
})

CkWh_cases = pd.read_csv(pjoin(REPO_DIR, 'cap_cost','figure_panels','CkWh_cases.csv'), index_col=0)

label_fontsize = 14
marker_size = 50
ADJUST_TEXT_LIM = 5
Ckwh_cutoff = CkWh_cases['value']['A']

y_lim = (5e-3, Ckwh_cutoff*2)
xlim = (0.02, 60)

OVERWRITE_FIX_POSITIONS = False
fn_fix_positions = 'fix_positions_decoupled.csv'
fix_positions = pd.read_csv(fn_fix_positions, index_col=0)

output_dir = 'output'
if not os.path.exists(output_dir): os.makedirs(output_dir)

df = read_pint_df(pjoin(REPO_DIR,'cap_cost/data_consolidated/SM_data.csv'), index_col=[0,1], drop_units=True).reset_index('SM_type')



formula_strings = [format_chem_formula(s) for s in df.index]
df['display_text'] = formula_strings

#TODO: Quick fix. 
df['display_text'] = df['display_text'].replace("TiMn_{1.4}V_{0}.62H_{3.4}", "TiMn_{1.4}V_{0.62}H_{3.4}", regex=False)


df['SM_type'] = df['SM_type'].replace('liquid_metal_battery', 'liquid_metal')
df['SM_type'] = df['SM_type'].replace('synfuel', 'Synthetic fuel')
df['SM_type'] = df['SM_type'].str.replace('_',' ').str.title()
df['sub_type'] = df['sub_type'].str.replace('_',' ').str.title()
df['mat_type'] = df['mat_type'].str.replace('_',' ').str.title()
df['mat_type'] = df['mat_type'].str.replace('Lohc','LOHC')


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

#New adjustText version draws arrow even though this is off screen, just will put manually in figure. 
df_ec_decoupled = df_ec_decoupled.drop('H2 (Feedstock)')

#%%

print("Decoupled")


x_str='specific_energy'
y_str='C_kwh'

fig = plt.figure()

sns.scatterplot(data=df_ec_decoupled, y=y_str, x=x_str, hue='SM_type', style='SM_type', legend=True, s=marker_size)

ax = plt.gca()

plt.yscale('log')
plt.xscale('log')
plt.ylim(y_lim)
plt.xlim(*xlim)

texts = annotate_points(df_ec_decoupled, x_str, y_str, 'display_text', ax=ax)

# plt.gca().get_legend().set_bbox_to_anchor([0,0.6,0.5,0])

ax.set_title('Decoupled')
plt.xlabel('Specific Energy (kWh/kg)', fontsize=label_fontsize)
plt.ylabel("$C_{kWh,mat}$ (\$/kWh)", fontsize=label_fontsize)

leg = ax.get_legend()
leg.set_title('Sub Type')
leg.set_bbox_to_anchor([0,0,1,0.52])

case_lns = []
for case, row in CkWh_cases.iterrows():
    case_lns.append(plt.axhline(row['value'], linestyle=row['linestyle'], color='gray'))

fix_positions = {name : (row['x'],row['y']) for name, row in fix_positions.iterrows() if row['fix'] == 'y'}

texts, texts_fix, orig_xy, orig_xy_fixed = prepare_fixed_texts(texts, fix_positions, ax=ax)

arrows_fix = draw_arrows(texts_fix, arrowprops=dict(arrowstyle='->'), ax=ax, orig_xy=orig_xy_fixed)

adjust_text(texts, 
            expand_text = (1.05, 1.2),      #(1.05, 1.2)
            expand_points = (2,2),    #(1.05, 1.2)
            expand_objects = (1.05, 1.2),   #(1.05, 1.2)
            expand_align = (1.05, 1.2),     #(1.05, 1.2)
            force_text= (0.2, 0.5),        #(0.1, 0.25)
            force_points = (0.2, 0.5),      #(0.2, 0.5)
            force_objects = (0.1, 0.25),    #(0.1, 0.25)
            lim=ADJUST_TEXT_LIM, 
            add_objects=[*texts_fix, *arrows_fix, *case_lns], 
            arrowprops=dict(arrowstyle='->')
            )

all_texts = [*texts_fix, *texts]
# from es_utils.plot import adjust_text_after
# adjust_text_after(fig, ax, "Na_{2}LiAlH_{6}", all_texts, 3,12)

from es_utils.plot import gen_text_position_fix_csv, combine_fix_pos

if OVERWRITE_FIX_POSITIONS:
    df_text_position = gen_text_position_fix_csv(texts, ax)
    df_text_position = combine_fix_pos(df_ec_decoupled, df_text_position)
    df_text_position.to_csv(fn_fix_positions)


plt.savefig(pjoin(output_dir,'ec_rhoE_decoupled.png'))

# %%



