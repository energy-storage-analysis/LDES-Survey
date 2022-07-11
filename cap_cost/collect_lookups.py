#%%
import os
import pandas as pd

def list_fps(filepath, search_term):
    paths = []
    for root, dirs, files in os.walk(filepath):
        for file in files:
            # fn = os.path.splitext(file)[0]
            if search_term in file:
                paths.append(os.path.join(root, file))
    return(paths)



# %%

folder = r'C:\Users\aspit\Git\MHDLab-Projects\Energy-Storage-Analysis\cap_cost\datasets'
fps = list_fps(folder, 'mat_lookup.csv')

dfs = []
for fp in fps:
    df = pd.read_csv(fp, index_col=0)

    print(fp)
    print(df.columns)

    dfs.append(df)

df_out = pd.concat(dfs)
# df_out.to_csv('mat_lookup_all.csv')

#%%

df_out


# %%

folder = r'C:\Users\aspit\Git\MHDLab-Projects\Energy-Storage-Analysis\cap_cost\datasets'
fps = list_fps(folder, 'SM_lookup.csv')

dfs = []
for fp in fps:
    df = pd.read_csv(fp, index_col=0)

    # print(fp)
    # print('----')
    # print(df.columns)

    dfs.append(df)

df_out = pd.concat(dfs)
df_out.to_csv('output/SM_lookup_all.csv')
# %%
df_out

#%%

#Check for differing entries by index

mat_defs = df_out.groupby(['SM_name','SM_type'])['materials'].apply(lambda x: len(set(x)))#.value_counts()
mat_def_dup = mat_defs[mat_defs > 1].dropna()
mat_def_dup

df_out.set_index(['SM_name','SM_type']).loc[mat_def_dup.index]

#%%


st_defs = df_out.groupby(['SM_name','SM_type'])['sub_type'].apply(lambda x: len(set(x)))#.value_counts()
st_def_dup = st_defs[st_defs > 1].dropna()
st_def_dup

df_out.set_index(['SM_name','SM_type']).loc[st_def_dup.index]
# %%

df_out