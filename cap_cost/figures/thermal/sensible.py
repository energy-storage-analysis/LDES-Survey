
#%%
import re
import seaborn as sns
from es_utils.units import read_pint_df
import os
from os.path import join as pjoin

import matplotlib.pyplot as plt
import matplotlib as mpl
plt.rcParams.update({'font.size':12, 'savefig.dpi': 600})
label_fontsize = 14

from adjustText import adjust_text

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

df_sens_ds = df_sens.where(df_sens['C_kwh'] < 10).dropna(how='all')


plt.figure()

x_str='T_max'
y_str='C_kwh'

# df_sens_ds.plot.scatter(y=y_str, x=x_str, c='deltaT', cmap='jet', sharex=False)
# df_sens_ds.plot.scatter(y=y_str, x=x_str, sharex=False)
sns.scatterplot(data=df_sens_ds, y=y_str, x=x_str, hue='sub_type', legend=True)

ax = plt.gca()
texts = []
for name, row in df_sens_ds.iterrows():
    x = row[x_str]
    y = row[y_str]
    # name = name[0:25].replace('_','') #TODO: error when adding steinmann...

    txt= ax.text(x, y, "${}$".format(name))
    texts.append(txt)

# plt.xscale('log')
plt.yscale('log')
plt.ylim(0.05,20)
# plt.ylim(0,10)

plt.xlim(-500,3550)

plt.xlabel('Maximum Temperature (deg C)', fontsize=label_fontsize)
plt.ylabel("$C_{kWh,mat}$ (\$/kWh)", fontsize=label_fontsize)
plt.suptitle("Sensible")


# plt.gcf().axes[1].set_ylabel('Maximum DeltaT (deg C)')

adjust_text(texts,  arrowprops = dict(arrowstyle='->'), force_points=(5,2))

plt.savefig(pjoin(output_dir,'sensible.png'))
# %%
# %%

