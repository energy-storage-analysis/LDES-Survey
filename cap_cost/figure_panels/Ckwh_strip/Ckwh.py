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


#%%


def calc_DDmax(log_C_kWh):
    return 2190/(10**log_C_kWh)

def inv_DDmax(DD_max):
    return np.log10(2190/DD_max)

df_all['DDmax'] = calc_DDmax(df_all['C_kwh_log'])




#%%

df_plot = df_all

np.random.seed(49)

fig = plt.figure()

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

# plt.axhline(np.log10(10), linestyle='--', color='gray')

fig.axes[0].yaxis.set_major_formatter(mticker.StrMethodFormatter("$10^{{{x:.0f}}}$"))
log_ticks = range(int(np.floor(df_plot['C_kwh_log'].min())), int(np.ceil(df_plot['C_kwh_log'].max())))

fig.axes[0].yaxis.set_ticks([np.log10(x) for p in log_ticks for x in np.linspace(10**p, 10**(p+1), 10)], minor=True)
plt.xticks(rotation=70)


plt.ylabel('$C_{kWh,mat}$ (USD/kWh)')
plt.xlabel('Technology')
plt.suptitle("{} Storage Media with Price and Energy data".format(len(df_plot)))


# strip_plot(df_all)

# plt.text(10,0.3, '$\phi = 100 hours$')


# plt.gca().get_legend().set_bbox_to_anchor([0,0,1.35,1])
plt.gca().get_legend().remove()
plt.suptitle('')


## Right hand axis
plt.twinx()

t_ax = sns.stripplot(
    data=df_plot, 
    x='display_text', 
    y='DDmax', 
    size=3, 
    color='black', 
    alpha=0 #This can be used to check alignment
                )

#TODO: Can't get secondary axis to work, but should be simpler than plotting fake data...
# https://matplotlib.org/stable/gallery/subplots_axes_and_figures/secondary_axis.html

# t_ax = ax.secondary_yaxis('right',functions=(calc_DDmax, inv_DDmax))

t_ax.set_yscale('log')
# plt.yscale('log')

t_ax_ylim = (
    2190/(10**(log_ticks.start)),
    2190/(10**(log_ticks.stop))
)

t_ax.set_ylim(*t_ax_ylim)

t_ax.set_yticks([1e6,1e5,1e4,1e3,1e2,1e1,1e0,1e-1,1e-2,1e-3,1e-4])

#TODO: Can't get working 
# t_ax.set_zorder(ax.get_zorder() + 1000)
# t_ax.set_frame_on(False)

t_ax.grid(linestyle = '--', alpha = 0.7)

t_ax.set_axisbelow(True)

plt.ylabel("$\\frac{DD_{max}}{LT \eta CF}$ [hours]")


plt.tight_layout()
plt.savefig(pjoin(output_dir,'Ckwh.png'))

# %%




