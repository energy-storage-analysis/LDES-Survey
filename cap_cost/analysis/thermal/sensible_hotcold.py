
#%%
import re
import seaborn as sns
import os
from os.path import join as pjoin

from es_utils.units import read_pint_df
from es_utils.plot import annotate_points

import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams.update({'font.size':12})
from adjustText import adjust_text, get_bboxes, get_midpoint

from dotenv import load_dotenv
load_dotenv()
REPO_DIR = os.getenv('REPO_DIR')

output_dir = 'output'
if not os.path.exists(output_dir): os.makedirs(output_dir)

df = read_pint_df(pjoin(REPO_DIR,'cap_cost/data_consolidated/SM_data.csv'), index_col=[0,1], drop_units=True).reset_index('SM_type')

df.index = [re.sub('(\D)(\d)(\D|$)',r'\1_\2\3', s) for s in df.index] #Simple way to format chemical equations as latex. Assumes only time numbers are showing up. 

# %%
df_sens = df.where(df['SM_type'] == 'sensible_thermal').dropna(subset=['SM_type'])
df_sens = df_sens.dropna(axis=1, how='all')
df_sens = df_sens.rename({'Vegetable Oil': 'Veg. Oil'})

df_sens_ds = df_sens.where(df_sens['C_kwh'] < 100).dropna(how='all')



#%%


df_cold = df_sens_ds.where(df_sens_ds['sub_type'] == 'cold').dropna(how='all')
df_hot = df_sens_ds.where(df_sens_ds['sub_type'].isin(['hot','both'])).dropna(how='all')

df_hot

#%%


def adjust_text_after(ax, text_alter, x,y):
    text_obj = texts_cold[text_alter]
    
    if x != None: text_obj.set_x(x)
    if y != None: text_obj.set_y(y)
    r = fig.canvas.renderer
    bbox = get_bboxes([text_obj] , r, (1, 1), ax)[0]
    cx, cy = get_midpoint(bbox)

    child_slot_alter = len(texts_cold)+1+text_alter
    arrow = ax_cold.get_children()[child_slot_alter]
    arrow.set_x(cx)
    arrow.set_y(cy)
#%%
# fig, axes = plt.subplots(1,2)
fig = plt.figure(figsize=(13.5,5), constrained_layout=True)
spec = fig.add_gridspec(1,4)

x_str='T_min'
y_str='C_kwh'

ax_cold = fig.add_subplot(spec[0,0])
sns.scatterplot(data=df_cold, y=y_str, x=x_str, legend=True, ax=ax_cold)
texts_cold =annotate_points(df_cold, x_str,y_str,ax=ax_cold)

ax_cold.set_yscale('log')
ax_cold.set_ylim(0.005,200)
ax_cold.set_xlim(-200,0)

ax_cold.set_xlabel('Min Temperature (deg C)')
ax_cold.set_ylabel("$C_{kWh,mat}$ (\$/kWh)")
ax_cold.set_title("Cold Sensible")


x_str='T_max'
y_str='C_kwh'


#https://stackoverflow.com/questions/22511550/gridspec-with-shared-axes-in-python
ax_hot = fig.add_subplot(spec[1:], sharey=ax_cold)
sns.scatterplot(data=df_hot, y=y_str, x=x_str, legend=True,ax=ax_hot)
texts_hot =annotate_points(df_hot, x_str,y_str,ax=ax_hot)


ax_hot.set_yscale('log')
# ax_hot.set_ylim(0.05,110)
ax_hot.set_xlim(0,2400)

ax_hot.set_xlabel('Maximum Temperature (deg C)')
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
    "Ethanol": (-80,8),
    "Isopentane": (-190,3),
    "N-propane": (-180,0.5),
    'Methanol': (-100,1),
    'N-pentane': (None,30),
    'N-hexane': (-100,20)
}

text_strings = [t.get_text().strip("$") for t in texts_cold]

for alter_name, (x,y) in alter_dict.items():
    text_index = text_strings.index(alter_name)
    adjust_text_after(ax_cold, text_index, x,y)

ax_cold.hlines(10,-200,0, linestyle='--', color='gray')

adjust_text(texts_hot,  arrowprops = dict(arrowstyle='->'), force_points=(1,1))

# alter_dict = {

# }
# text_strings = [t.get_text().strip("$") for t in texts_cold]

# for alter_name, (x,y) in alter_dict.items():
#     text_index = text_strings.index(alter_name)
#     adjust_text_after(ax_cold, text_index, x,y)

ax_hot.hlines(10,0,2400, linestyle='--', color='gray')
# fig.tight_layout()

plt.savefig('output/sensible_hotcold.png')
# %%
