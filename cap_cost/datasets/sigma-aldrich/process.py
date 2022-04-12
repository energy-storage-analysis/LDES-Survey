import pandas as pd

df = pd.read_csv('raw_data.csv', index_col=0)


import pint

ureg = pint.UnitRegistry()


min_quantity_kg = []
min_unit_kg = []
for index, row in df.iterrows():
    unit = row['quantity_unit']

    val_min_unit = ureg.Quantity(row['quantity'], '{}'.format(unit))
    min_quantity_kg.append(val_min_unit.to('kg').magnitude)

    val_1 = ureg.Quantity(1, '{}'.format(unit))
    min_unit_kg.append(val_1.to('kg').magnitude)

    # break

# %%
df['quantity_kg'] = min_quantity_kg
df['quantity_unit_kg'] = min_unit_kg
df
# %%
df['specific_price'] = df['price']/df['quantity_kg']
df

df.to_csv('output/mat_data.csv')