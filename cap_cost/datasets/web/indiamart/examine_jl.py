#%%

import os

import numpy as np
import pandas as pd


df = pd.read_json('scraped_data/items.jl', lines=True).set_index('index')
df.to_csv('scraped_data/items.csv')

df = pd.read_json('scraped_data/items_dropped.jl', lines=True).set_index('index')
df.to_csv('scraped_data/items_dropped.csv')