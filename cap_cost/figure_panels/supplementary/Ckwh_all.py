#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import ticker as mticker

plt.rcParams.update({
    "savefig.facecolor": 'white',
    "font.size": 12, 
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


# %%

from scipy import stats

import seaborn as sns

# fig, axes = plt.subplots(figsize=(4,2))

x = sns.displot(
    df_all[['C_kwh_log', 'energy_type']], 
    x='C_kwh_log', 
    hue='energy_type', 
    palette=palette,
    kind='kde', 
    bw_adjust=1, 
    height=2,
    aspect=2,
    common_norm=True,
    fill=True,
    alpha=0.1
    )

plt.xlim(-3,4)

# plt.xscale('log')
# plt.yscale('log')

#%%

from matplotlib.colors import to_rgb


#%%
import numpy as np
from PIL import Image
from scipy.stats import gaussian_kde


df = df_all[['C_kwh_log', 'energy_type']]


for energy_sel in set(df['energy_type']):

    df_sel = df.where(df['energy_type'] == energy_sel).dropna(how='all')

    color_mpl = palette[energy_sel]

    density = gaussian_kde(df_sel['C_kwh_log'])
    density.set_bandwidth(0.1)

    y = density(xs)

    # Define width and height
    w, h = 465, 30

    # Make solid orange background
    cs = to_rgb(color_mpl)
    cs = tuple(int(c*255) for c in cs)
    im = Image.new('RGB', (w,h), cs)

    # xs = np.linspace(df['C_kwh_log'].min(),df['C_kwh_log'].max(),50)
    xs = np.linspace(-3,4,w)
    line = density(xs)
    line = (line/line.max())*255
    line = line.astype(np.uint8)
    # ... repeat that line h times to get the full height of the image
    alpha = np.tile(line, (h,1))

    # Put our lovely new alpha channel into orange image
    im.putalpha(Image.fromarray(alpha))

    output_dir = 'output/bands'
    if not os.path.exists(output_dir): os.makedirs(output_dir)
    im.save(os.path.join(output_dir, "{}.png".format(energy_sel)))


#%%


sns.displot(
    df_all[['C_kwh_log', 'energy_type']], 
    x='C_kwh_log', 
    kind='kde', 
    bw_adjust=1, 
    height=2,
    aspect=2,
    fill=True
    )

plt.yscale('log')

#%%


hue_order = [
    'Gravitational',
    'Electrostatic',
    'Magnetic',
    'Kinetic',
    'Pressure',
    'Thermal',
    'Chemical'
]

plt.figure(figsize=(5,1.8))

sns.histplot(
    df_all[['C_kwh_log', 'energy_type']], 
    x='C_kwh_log', 
    hue='energy_type',
    alpha=0.5,
    hue_order=hue_order,
    palette=palette

)


#%%

plt.figure(figsize=(6, 3))
bins = [
        df_all['C_kwh_log'].min(),
        np.log10(0.5) ,
        np.log10(5),
        np.log10(180),
        df_all['C_kwh_log'].max(),
        ]


sns.histplot(
    df_all[['C_kwh_log', 'energy_type']], 
    x='C_kwh_log', 
    hue='energy_type',
    alpha=1,
    hue_order=hue_order,
    palette=palette,
    bins=bins

)

#%%


from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

hue_order = [
    'Chemical',
    'Thermal',
    'Pressure',
    'Kinetic',
    'Gravitational',
    'Electrostatic',
    'Magnetic',
]

bins = [
        df_all['C_kwh'].min(),
        0.5,
        5,
        180,
        df_all['C_kwh'].max(),
        ]

df_sel = df_all[['C_kwh', 'energy_type']]

df_sel['C_kwh_bin'] = pd.cut(df_sel['C_kwh'], bins = bins)

df_stats = df_sel.groupby(['C_kwh_bin', 'energy_type']).count()

df_stats = df_stats.reset_index()

plt.figure(figsize=(6, 3.7))
ax = sns.barplot(
                data=df_stats, 
                x='C_kwh_bin', 
                y='C_kwh', 
                hue='energy_type', 
                palette=palette, 
                hue_order=hue_order
                # order=hue_order
                )
# plt.yscale('log')
# plt.xticks(None, rotation = 90)

# plt.yticks([0,50,100, 150])

plt.ylim(0,150)
ax.yaxis.set_major_locator(MultipleLocator(50))
ax.yaxis.set_minor_locator(MultipleLocator(10))

leg = ax.get_legend()
# leg.set_bbox_to_anchor([0,0,1.4,1])
leg.set_title('Energy Type')

# plt.xticks(['1','2','3','4'])
# plt.ylim(0,150)
# plt.ylabel('Count')
plt.ylabel("Number of Systems")
plt.xlabel('$C_{kWh}$ [USD/kWh]')

plt.tight_layout()

plt.savefig('output/Ckwh_all.png')

# %%
df_stats = df_sel.groupby(['C_kwh_bin']).count()
df_stats = df_stats.reset_index()

plt.figure(figsize=(6, 3))
ax = sns.barplot(data=df_stats, x='C_kwh_bin', y='C_kwh', color='lightblue')

plt.ylabel('Count')
plt.xlabel('$C_{kWh}$ [USD/kWh]')


#%%

