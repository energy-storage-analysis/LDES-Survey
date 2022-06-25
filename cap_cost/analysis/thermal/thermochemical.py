#%%
import matplotlib.pyplot as plt
import seaborn as sns
import re
from es_utils.units import read_pint_df
import os
from os.path import join as pjoin

import matplotlib as mpl
mpl.rcParams.update({'font.size':12})
from adjustText import adjust_text

from dotenv import load_dotenv
load_dotenv()
REPO_DIR = os.getenv('REPO_DIR')

output_dir = 'output'
if not os.path.exists(output_dir): os.makedirs(output_dir)

df = read_pint_df(pjoin(REPO_DIR,'cap_cost/data_consolidated/SM_data.csv'), index_col=[0,1], drop_units=True).reset_index('SM_type')

df.index = [re.sub('(\D)(\d)(\D|$)',r'\1_\2\3', s) for s in df.index] #Simple way to format chemical equations as latex. Assumes only time numbers are showing up. 

# %%


df_tc = df.where(df['SM_type'] == 'thermochemical').dropna(subset=['SM_type'])
df_tc = df_tc.dropna(axis=1,how='all')
df_tc = df_tc.where(df_tc['C_kwh'] < 10).dropna(how='all')

plt.figure()
x_str='temperature'
y_str='C_kwh'

sns.scatterplot(data=df_tc, y=y_str, x=x_str, hue='sub_type', legend=True)

ax = plt.gca()
texts = []
for name, row in df_tc.iterrows():
    x = row[x_str]
    y = row[y_str]
    # name = row['materials']

    txt = ax.text(x,y,"${}$".format(name))
    texts.append(txt)

plt.xlim(0,2000)
# plt.gca().get_legend().set_bbox_to_anchor([0,0,1.3,1])

plt.yscale('log')
plt.ylim(0.05,20)
# plt.ylim(0,10)

plt.xlabel('Reaction Temperature (C)')
plt.ylabel("$C_{kWh,mat}$ (\$/kWh)")
plt.suptitle("Thermochemcial")
plt.tight_layout()

adjust_text(texts, arrowprops = dict(arrowstyle='->'), force_points=(0,5))

plt.savefig(pjoin(output_dir,'thermochem.png'))
# %%