#%%
import os 

for dirpath, dirnames, filenames in os.walk('.'):
    if 'readme.md' in [f.lower() for f in filenames]:
        print(dirpath, dirnames, filenames)