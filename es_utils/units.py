import pandas as pd
import pint_pandas
import pint
import os

cwd = os.path.dirname(os.path.abspath(__file__))
fp_definitions = os.path.join(cwd,'unit_defs.txt')


ureg = pint.UnitRegistry()
ureg.load_definitions(fp_definitions)
pint_pandas.PintType.ureg = ureg

def get_unit_row(df_unit):
    unit_row = []
    for col in df_unit.columns:
        if isinstance(df_unit[col].dtype, pint_pandas.pint_array.PintType):
            # df_unit[col] = df_unit[col].pint.dequantify()
            unit_row.append(df_unit[col].pint.units)
        else:
            unit_row.append('N/U')

    unit_row = pd.Series(unit_row, index=df_unit.columns)
    unit_row.name = 'unit_row'
    return unit_row


def prep_df_pint_out(df_in):
    """
    This is a function that takes units in columns that are pint quantified and pulls them out into the column header
    Essentially a quick fix to 
    https://github.com/hgrecco/pint-pandas/issues/46
    Which manually dequantifies pint columns (with pint.magnitude)
    """

    df = df_in.copy()

    unit_row = get_unit_row(df)
    # unit_row = unit_row.to_frame().T

    for col in df.columns:
        if 'pint' in str(df[col].dtype):
            df[col] = df[col].pint.magnitude

    # df = pd.concat([unit_row, df])

    df.columns = pd.MultiIndex.from_arrays([df.columns, unit_row])

    return df


def read_pint_df(filepath, index_col=0, drop_units=False):
    """
    Reads a csv file saved by prep_df_pint_out to a format where columns with units are pint quantified
    """
    df = pd.read_csv(filepath, header=[0,1], index_col=index_col)

    types = {}
    for col, unit in df.columns:
        if unit != 'N/U':
            types[col] = 'pint[{}]'.format(unit)

        
    df.columns = df.columns.droplevel(1)

    df = df.astype(types)

    if drop_units:
        for col in df.columns:
            if 'pint' in str(df[col].dtype):
                df[col] = df[col].pint.magnitude

    return df

unit_lookup = {
    'specific_price': 'USD/kg',
    'sp_latent_heat': 'kWh/kg',
    'phase_change_T': 'degC',
    'Cp': 'kWh/kg/K',
    'deltaH_thermochem': 'kWh/kg',
    'specific_capacitance': 'F/g',
    'deltaV_cap': 'V',
    # 'specific_strength': 'kWh/kg'
}

def convert_units(df):
    for key, unit in unit_lookup.items():
        if key in df.columns:
            df[key] = df[key].pint.to(unit)
    
    return df


def convert_row(df, val_col, unit_col, unit_to):
    """Converts the val_col of a dataframe to units of unit_to based on unit_col starting units"""
    data_out = []
    for index, row in df.iterrows():
        unit = row[unit_col]
        val = row[val_col]
        val = ureg.Quantity(val, unit)
        val = val.to(unit_to).magnitude
        data_out.append(val)

    data_out = pd.Series(data_out, index=df.index, dtype="pint[{}]".format(unit_to)) 

    return data_out