import pandas as pd
import os

tables = {fn.strip('.csv') : pd.read_csv(os.path.join('tables',fn)) for fn in os.listdir('tables')}


df = pd.concat(tables.values())


df['specific_energy'] = df['specific_energy'].astype(float)
df['enthalpy'] = df['enthalpy'].astype(float)
df['temperature'] = df['temperature'].astype(float)

df['enthalpy'] = df['enthalpy']/3600 #kJ to kWh
df['specific_energy'] = df['specific_energy']/3600 #kJ to kWh

df = df.rename({
    'reactant':'molecular_formula'
}, axis=1)

df.to_csv('output/process.csv')