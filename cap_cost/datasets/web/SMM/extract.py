#%%
import pandas as pd
import os

if not os.path.exists('output'): os.mkdir('output')

dfs = []

fns = os.listdir('input_data')

for fn in fns:

    fp = os.path.join('input_data',fn)

    df = pd.read_excel(fp)

    df = df[['Name','Avg With Rate', 'Unit', 'Date']]

    dfs.append(df)

df = pd.concat(dfs)

df['Unit'] = df['Unit'].str.replace('RMB', 'USD')
df['Unit'] = df['Unit'].str.replace('USD/g', 'USD/oz') #The units change for this on the website....Only for Cs and Rb
df['Unit'] = df['Unit'].str.replace('Kg', 'kg')
df['Unit'] = df['Unit'].str.replace('mtu', 'metric_ton') 
df['Unit'] = df['Unit'].str.replace('mt', 'metric_ton') 

df['Avg With Rate'] = abs(df['Avg With Rate']) #There is a minus sign that appears to be "(c) symbol on website, not minus sign...not that that would make sense ayway"

df['Name'] = df['Name'].str.replace('＜','<')
df['Name'] = df['Name'].str.replace('（','(')
df['Name'] = df['Name'].str.replace('）',')')
df['Name'] = df['Name'].str.replace('#\d ','', regex=True)
df['Name'] = df['Name'].str.replace('\d# ','', regex=True)

df = df.set_index('Name')

df.to_csv('output/extracted.csv')
