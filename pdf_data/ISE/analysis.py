#%%
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys

sys.path.append('..')
from pdf_utils import average_range


# %%

df = pd.read_csv('ISE.csv', encoding='ISO-8859-1', skiprows=[1,2])
df.columns = [c.strip() for c in df.columns]

df =df.drop([47,79,81]).reset_index(drop=True) # Seems to be a typo for cobalt entry

df['Price in USD'] = df['Price in USD'].apply(average_range)
df['Price in USD'] = df['Price in USD'].astype(float)
df
# df.columns
# %%
bins = np.logspace(np.log10(0.1), np.log10(1e6), 50)
df['Price in USD'].hist(bins=bins)
plt.xscale('log')
plt.xlabel('Cost ($/kg)')
plt.ylabel('Count')