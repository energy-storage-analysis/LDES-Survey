#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import ticker as mticker

plt.rcParams.update({
    "savefig.facecolor": 'white',
    "font.size": 7, 
    'savefig.dpi': 600, 
    'font.sans-serif': 'arial', 
    'figure.figsize': (4.6, 3)
})


# sns.set(font_scale=1)

import os
from os.path import join as pjoin
output_dir = 'output'
if not os.path.exists(output_dir): os.makedirs(output_dir)

from es_utils.units import read_pint_df

from dotenv import load_dotenv
load_dotenv()
REPO_DIR = os.getenv('REPO_DIR')

palette = pd.read_csv('../energy_colors.csv', index_col=0)['color'].to_dict()
palette = {key.replace('\\n','\n'): val for key,val in palette.items()}

CkWh_cases = pd.read_csv(pjoin(REPO_DIR, 'cap_cost','figure_panels','CkWh_cases.csv'), index_col=0)

df_all = read_pint_df(pjoin(REPO_DIR, 'cap_cost/data_consolidated/SM_data.csv'), index_col=[0,1], drop_units=True).reset_index('SM_type')

df_all = df_all.dropna(subset=['C_kwh'])

display_text = pd.read_csv('../tech_lookup.csv', index_col=0)

df_all['SM_type'] = df_all['SM_type'].str.replace("(","\n(", regex=False)

df_all['display_text'] = [display_text['long_name'][s].replace('\\n','\n') for s in df_all['SM_type'].values]
df_all['energy_type'] = [display_text['energy_type'][s].replace('\\n','\n') for s in df_all['SM_type'].values]
df_all['coupled'] = [display_text['coupled'][s].replace('\\n','\n') for s in df_all['SM_type'].values]
df_all['C_kwh_log'] = np.log10(df_all['C_kwh'])

median_Ckwh = df_all.groupby('SM_type')['C_kwh'].median().to_dict()

df_all['Ckwh_SMtype_median'] = df_all['SM_type'].map(median_Ckwh)
df_all = df_all.sort_values('Ckwh_SMtype_median')#.sort_values('energy_type')

# df_all

#%%

# Separate out volumetric 

syn_tanks = df_all.where(df_all['SM_type'] == 'synfuel').where(df_all['sub_type'] == 'tank').dropna(how='all')
syn_under = df_all.where(df_all['SM_type'] == 'synfuel').where(df_all['sub_type'] == 'underground').dropna(how='all')
press_cav = df_all.where(df_all['SM_type'] == 'pressure_cavern').dropna(how='all')
phes = df_all.where(df_all['sub_type'] == 'pumped_hydro').dropna(how='all')

SM_vol = pd.concat([syn_tanks,syn_under,press_cav,phes])

SM_vol
#%%


df_mat = df_all.drop(SM_vol.index)


#%%
# def calc_DDmax(log_C_kWh):
#     return 2190/(10**log_C_kWh)

# def inv_DDmax(DD_max):
#     return np.log10(2190/DD_max)

# df_all['DDmax'] = calc_DDmax(df_all['C_kwh_log'])

#%%
from es_utils.plot import gen_legend_figure

linestyle_dict = CkWh_cases['linestyle'].to_dict()

legendFig = gen_legend_figure(linestyle_dict, title='', style_type='linestyle', figsize=(1.2,0.5))
legendFig.savefig('output/legend_cases.png', transparent=True)



#%%

vol_plot_width = 1
ylim = (-3,4.3)

df_plot = df_mat

print("Outside Range Material Price ")
df_missing = df_plot.where(df_plot['C_kwh_log'] < ylim[0]).dropna(how='all')
print("below range: {}".format(df_missing[['C_kwh','SM_type']]))
df_missing = df_plot.where(df_plot['C_kwh_log']>ylim[1]).dropna(how='all')
print("above range: {}".format(df_missing[['C_kwh','SM_type']]))

np.random.seed(49)

fig = plt.figure(figsize=(4.6 - vol_plot_width, 3))

cat_label = 'display_text'
ax = sns.stripplot(
    data=df_plot, 
    x=cat_label, 
    y='C_kwh_log', 
    size=3, 
    hue='energy_type', 
    palette=palette, 
    style='coupled', 
    markers={'Coupled': 'X', 'Decoupled':'o'},
    jitter=0.2,
                )


for case, row in CkWh_cases.iterrows():
    plt.axhline(np.log10(row['value']), linestyle=row['linestyle'], color='gray')


fig.axes[0].yaxis.set_major_formatter(mticker.StrMethodFormatter("$10^{{{x:.0f}}}$"))
# log_ticks = range(int(np.floor(df_plot['C_kwh_log'].min())), int(np.ceil(df_plot['C_kwh_log'].max())))
log_ticks = range(int(np.floor(df_plot['C_kwh_log'].min())), int(6))


fig.axes[0].yaxis.set_ticks([np.log10(x) for p in log_ticks for x in np.linspace(10**p, 10**(p+1), 10)], minor=True)
plt.xticks(rotation=70)

plt.ylim(ylim)

plt.ylabel('$C_{kWh,SM}$ (USD/kWh)')
plt.xlabel('Technology')
plt.suptitle("{} Storage Media with Price and Energy data".format(len(df_plot)))


plt.gca().get_legend().remove()
plt.suptitle('')

plt.tight_layout()
plt.savefig(pjoin(output_dir,'Ckwh_mat.png'))

# %%



print("Outside Range Volumetric Price ")
df_missing = SM_vol.where(SM_vol['C_kwh_log'] < ylim[0]).dropna(how='all')
print("below range: {}".format(df_missing[['C_kwh','SM_type']]))
df_missing = SM_vol.where(SM_vol['C_kwh_log']>ylim[1]).dropna(how='all')
print("above range: {}".format(df_missing[['C_kwh','SM_type']]))


df_plot = SM_vol

np.random.seed(49)

fig = plt.figure(figsize=(vol_plot_width, 3))

cat_label = 'display_text'
ax = sns.stripplot(
    data=df_plot, 
    x=cat_label, 
    y='C_kwh_log', 
    size=3, 
    hue='energy_type', 
    palette=palette, 
    style='coupled', 
    markers={'Coupled': 'X', 'Decoupled':'o'},
    jitter=0.2,
                )


for case, row in CkWh_cases.iterrows():
    plt.axhline(np.log10(row['value']), linestyle=row['linestyle'], color='gray')

fig.axes[0].yaxis.set_major_formatter(mticker.StrMethodFormatter("$10^{{{x:.0f}}}$"))
# log_ticks = range(int(np.floor(df_plot['C_kwh_log'].min())), int(np.ceil(df_plot['C_kwh_log'].max())))

fig.axes[0].yaxis.set_ticks([np.log10(x) for p in log_ticks for x in np.linspace(10**p, 10**(p+1), 10)], minor=True)
plt.xticks(rotation=70)

plt.ylim(ylim)

plt.ylabel('$C_{kWh,SM}$ (USD/kWh)')
plt.xlabel('Technology')
plt.suptitle("{} Storage Media with Price and Energy data".format(len(df_plot)))


plt.gca().get_legend().remove()
plt.suptitle('')

plt.ylabel('')
plt.yticks([])

plt.tight_layout()
plt.savefig(pjoin(output_dir,'Ckwh_vol.png'))