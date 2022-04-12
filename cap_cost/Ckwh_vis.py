#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import iqplot
from bokeh.io import show, output_file, save



# %%

df_all = pd.read_csv('data_consolidated/C_kWh.csv', index_col=0)
df_all = df_all.dropna(subset=['C_kwh'])

display_text = pd.read_csv('tech_lookup.csv', index_col=0)

df_all['SM_type'] = df_all['SM_type'].str.replace("(","\n(", regex=False)

df_all['display_text'] = [display_text['long_name'][s].replace('\\n','\n') for s in df_all['SM_type'].values]
df_all['energy_type'] = [display_text['energy_type'][s].replace('\\n','\n') for s in df_all['SM_type'].values]

df_all = df_all.sort_values('C_kwh').sort_values('energy_type')

#%%
cat_label = 'display_text'

from matplotlib import ticker as mticker
plt.rcParams.update({'font.size': 20})

df_all['C_kwh_log'] = np.log10(df_all['C_kwh'])

fig = plt.figure(figsize = (16,8))
# plt.violinplot(dataset=df_singlemat['C_kwh'].values)
# sns.violinplot(data=df_singlemat, x='cat_label', y='C_kwh_log')
sns.stripplot(data=df_all, x=cat_label, y='C_kwh_log', size=10, hue='energy_type')

plt.axhline(np.log10(10), linestyle='--', color='gray')

fig.axes[0].yaxis.set_major_formatter(mticker.StrMethodFormatter("$10^{{{x:.0f}}}$"))

log_ticks = range(int(np.floor(df_all['C_kwh_log'].min())), int(np.ceil(df_all['C_kwh_log'].max())))

fig.axes[0].yaxis.set_ticks([np.log10(x) for p in log_ticks for x in np.linspace(10**p, 10**(p+1), 10)], minor=True)
# plt.gca().set_xticks(np.arange(0, len(labels)), labels=labels)

# plt.yscale('log')
plt.xticks(rotation=90)
plt.ylabel('Material Energy Cost ($/kWh)')


plt.gca().get_legend().set_bbox_to_anchor([0,0,1.35,1])

plt.xlabel('Technology')
plt.suptitle("{} Storage Media with Price and Energy data".format(len(df_all)))

plt.tight_layout()
plt.savefig('results/fig_C_kwh.png')
# %%
#Raw entries

df_vis = df_all.reset_index().dropna(subset= ['C_kwh'])
#%%

# tips = [('index','@index'), ('entry source','@source'), ('original name', '@original_name'), ('specific price ($/kg)', '@specific_price'), ('specific energy (kWh/kg)','@specific_energy'), ("price type",'@price_type')]
tips = [('index','@SM_name'),  ('SM_sources','@SM_sources'), ('price_sources', '@price_sources'), ('specific price ($/kg)', '@specific_price'), ('specific energy (kWh/kg)','@specific_energy') ]

figure = iqplot.strip(
    data=df_vis, cats='SM_type', q='C_kwh', color_column='energy_type',
    q_axis='y',y_axis_type='log' ,
    jitter=True,
    tooltips= tips,
    plot_width = 1000,plot_height=700,
    marker_kwargs={'size':10}
    )

figure.xaxis.major_label_orientation = np.pi/4
figure.yaxis.axis_label = "Energy Capital Cost ($/kWh)"
# show(figure)
figure.yaxis.axis_label_text_font_size = "16pt"
figure.xaxis.major_label_text_font_size = "16pt"

output_file('results/mat_cost_compare.html')
save(figure)