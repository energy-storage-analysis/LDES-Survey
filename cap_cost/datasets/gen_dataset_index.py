#%%
import os 
import pandas as pd

dataset_index = {
    'folder': [],
    'processing_script':[],
    'extract_script':[]
}

for dirpath, dirnames, filenames in os.walk('.'):
    if 'unused' in dirpath:
        continue

    if 'readme.md' not in [f.lower() for f in filenames]:
        continue

    if 'output' not in dirnames:
        continue
        # print(dirpath, dirnames, filenames)

    folder_name = dirpath.removeprefix('.\\')
    dataset_index['folder'].append(folder_name)

    dataset_index['processing_script'] = 'y' if 'process.py' in filenames else ''
    dataset_index['extract_script'] = 'y' if 'extract.py' in filenames else ''


df = pd.DataFrame(dataset_index)

#%%

source_name = df['folder'].str.split('\\').apply(lambda x: x[-1])

def cap(word):
    return word[0].upper() + word[1:]

def title_preserving_caps(string):
    return " ".join(map(cap, string.split(' ')))

source_name = source_name.apply(title_preserving_caps)
source_name = source_name.str.replace('_',' ')

df['source'] = source_name
df = df.set_index('source')

df.to_csv('dataset_index.csv')
