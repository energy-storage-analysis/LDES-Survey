#%%

import numpy as np
import pandas as pd
from es_utils.units import read_pint_df
import seaborn as sns
import matplotlib.pyplot as plt

df = read_pint_df('output/SM_data.csv')

df['SM_type'] = df['SM_type'].astype(str)


df['specific_capacitance'] = df['specific_capacitance'].pint.magnitude

# df = df.pint.dequantify()
# %%

fig, axes = plt.subplots(
    2,1,
    sharex=True,
    )


# bins = np.linspace(0,1500, 30)

bins = np.logspace(np.log10(1e2), np.log10(2e3), 10)

sns.histplot(
    data=df[df['SM_type']=='EDLC'], 
    x='specific_capacitance',
    ax=axes[0],
    bins=bins)



sns.histplot(
    data=df[df['SM_type']=='pseudocapacitor'], 
    x='specific_capacitance',
    ax=axes[1],
    bins=bins)

for ax in axes:
    ax.set_xscale('log')

axes[0].set_title('EDLC')
axes[1].set_title('Pseudocapacitor')


plt.xlabel("Specific Capacitance (Farad/gram)")


plt.savefig('figures/capacitance.png')
# %%
