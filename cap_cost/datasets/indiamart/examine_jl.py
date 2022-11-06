#%%

import os

import numpy as np
import pandas as pd


df = pd.read_json('output/items.jl', lines=True).set_index('index')
df.to_csv('output/items.csv')

df = pd.read_json('output/items_dropped.jl', lines=True).set_index('index')
df.to_csv('output/items_dropped.csv')