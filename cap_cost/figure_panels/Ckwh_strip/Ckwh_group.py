#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import ticker as mticker
plt.rcParams.update({'font.size': 16})

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

def strip_plot(df_plot):

    cat_label = 'display_text'
    sns.stripplot(data=df_plot, x=cat_label, y='C_kwh_log', size=7, hue='energy_type', palette=palette, style='coupled')

    plt.axhline(np.log10(10), linestyle='--', color='gray')

    fig.axes[0].yaxis.set_major_formatter(mticker.StrMethodFormatter("$10^{{{x:.0f}}}$"))
    log_ticks = range(int(np.floor(df_plot['C_kwh_log'].min())), int(np.ceil(df_plot['C_kwh_log'].max())))

    fig.axes[0].yaxis.set_ticks([np.log10(x) for p in log_ticks for x in np.linspace(10**p, 10**(p+1), 10)], minor=True)
    plt.xticks(rotation=70)


    plt.ylabel('$C_{kWh,SM}$ (\$/kWh)')
    plt.xlabel('Technology')
    plt.suptitle("{} Storage Media with Price and Energy data".format(len(df_plot)))

#%%
elim_types = [
    'dielectric_capacitor',
    'EDLC',
    'pseudocapacitor',
    'gravitational',
    'pressure_cavern',
    'pressure_tank',
    'smes',
    'flywheel'
    ]


df_elim = df_all[df_all['SM_type'].isin(elim_types)]
df_elim['SM_type'] = pd.Categorical(df_elim['SM_type'], categories=elim_types, ordered=True)
df_elim = df_elim.sort_values('SM_type')
df_elim = df_elim[df_elim['C_kwh']<1e4]#.dropna(how='all')

fig = plt.figure(figsize = (7,6))
strip_plot(df_elim)

plt.gca().get_legend().remove()
plt.tight_layout()
plt.savefig(pjoin(output_dir,'Ckwh_eliminate.png'))

#%%

ec_types = [
    'solid_electrode',
    'liquid_metal_battery',
    'metal_air',
    'hybrid_flow',
    'flow_battery',
    'synfuel'
    ]


df_ec = df_all[df_all['SM_type'].isin(ec_types)]
df_ec['SM_type'] = pd.Categorical(df_ec['SM_type'], categories=ec_types, ordered=True)
df_ec = df_ec.sort_values('SM_type')
df_ec = df_ec[df_ec['C_kwh']<1e4]

fig = plt.figure(figsize = (8,8))
strip_plot(df_ec)

plt.gca().get_legend().remove()
plt.tight_layout()
plt.savefig(pjoin(output_dir,'Ckwh_ec.png'))

#%%

therm_types = [
    'sensible_thermal',
    'latent_thermal',
    'thermochemical'
    ]


df_therm = df_all[df_all['SM_type'].isin(therm_types)]
df_therm['SM_type'] = pd.Categorical(df_therm['SM_type'], categories=therm_types, ordered=True)
df_therm = df_therm.sort_values('SM_type')
df_therm = df_therm[df_therm['C_kwh']<1e4]

fig = plt.figure(figsize = (4,8))
strip_plot(df_therm)

plt.gca().get_legend().remove()
plt.tight_layout()
plt.savefig(pjoin(output_dir,'Ckwh_therm.png'))



