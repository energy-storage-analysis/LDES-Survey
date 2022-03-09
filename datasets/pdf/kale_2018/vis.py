#%%
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('output/processed.csv', index_col=0)

df['C_kwh'] = df['specific_price']/df['specific_energy']

df['C_kwh'].plot.bar()
plt.ylabel('$/kwh')

