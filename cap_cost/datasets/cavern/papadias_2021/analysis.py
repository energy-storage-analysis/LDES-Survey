#%%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df_3 = pd.read_csv('output/table_3_processed.csv', index_col=0)

vol = df_3['Cavern water volume (m3)']
lc = df_3['Leaching ($/kg)']


plt.plot(vol, lc, marker='o')

a, b = np.polyfit(vol, lc, 1)

line_fit = a*vol + b

plt.plot(vol, line_fit)


plt.ylabel("Leaching costs ($/kg)")
plt.xlabel("Water Volume (m^3)")

plt.suptitle("m: {}, b: {}".format(a,b))

plt.savefig('output/leaching_vol.png')

# %%
