#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import iqplot
from bokeh.io import show, output_file



# %%

df_all = pd.read_csv('data/C_kWh.csv', index_col=0)

#%%
cat_label = 'energy_type'

from matplotlib import ticker as mticker
plt.rcParams.update({'font.size': 20})

df_all['C_kwh_log'] = np.log10(df_all['C_kwh'])

fig = plt.figure(figsize = (13,8))
# plt.violinplot(dataset=df_singlemat['C_kwh'].values)
# sns.violinplot(data=df_singlemat, x='cat_label', y='C_kwh_log')
sns.stripplot(data=df_all, x=cat_label, y='C_kwh_log', size=10)

plt.axhline(np.log10(10), linestyle='--', color='gray')

fig.axes[0].yaxis.set_major_formatter(mticker.StrMethodFormatter("$10^{{{x:.0f}}}$"))
fig.axes[0].yaxis.set_ticks([np.log10(x) for p in range(-1,4) for x in np.linspace(10**p, 10**(p+1), 10)], minor=True)
# plt.gca().set_xticks(np.arange(0, len(labels)), labels=labels)

# plt.yscale('log')
plt.xticks(rotation=45)
plt.ylabel('Material Energy Cost ($/kWh)')
plt.tight_layout()
plt.savefig('output/fig_C_kwh.png')
# %%
#Raw entries

df_vis = df_all.reset_index().dropna(subset= ['C_kwh'])
#%%

# tips = [('index','@index'), ('entry source','@source'), ('original name', '@original_name'), ('specific price ($/kg)', '@specific_price'), ('specific energy (kWh/kg)','@specific_energy'), ("price type",'@price_type')]
tips = [('index','@index'),  ('physical property source','@physprop_source'), ('price_sources', '@price_sources'), ('specific price ($/kg)', '@specific_price'), ('specific energy (kWh/kg)','@specific_energy') ]

figure = iqplot.strip(
    data=df_vis, cats='energy_type', q='C_kwh', 
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

output_file('output/mat_cost_compare.html')
show(figure)