#%%
backup_folder = r'C:\Users\aspit\Git\Energy-Storage-Analysis\LV-Data'

import os 
import pandas as pd
import shutil

from dotenv import load_dotenv
load_dotenv()
repo_dir = os.getenv('REPO_DIR')

dataset_folder = os.path.join(repo_dir, 'cap_cost', 'datasets')


def copy_folder(full_dir):

        rel_dir = os.path.relpath(full_dir, '.')

        full_dir = os.path.join(dataset_folder, rel_dir)

        out_dir = os.path.join(backup_folder, 'cap_cost', 'datasets', rel_dir)

        if os.path.exists(out_dir):
            shutil.rmtree(out_dir)

        shutil.copytree(full_dir, out_dir)

for dirpath, dirnames, filenames in os.walk('.'):


    if 'unused' in dirpath:
        continue

    if 'readme.md' not in [f.lower() for f in filenames]:
        continue

    if 'output' not in dirnames:
        continue
        # print(dirpath, dirnames, filenames)

    if 'tables' in dirnames:
        full_dir = os.path.join(dirpath, 'tables')
        copy_folder(full_dir)
        shutil.rmtree(full_dir)

    if 'input_data' in dirnames:
        full_dir = os.path.join(dirpath, 'input_data')
        copy_folder(full_dir)

        shutil.rmtree(full_dir)

    if 'scraped_data' in dirnames:
        full_dir = os.path.join(dirpath, 'scraped_data')
        copy_folder(full_dir)

        shutil.rmtree(full_dir)

        # break


    # folder_name = dirpath.removeprefix('.\\')
    # dataset_index['folder'].append(folder_name)

    # dataset_index['processing_script'].append('y') if 'process.py' in filenames else dataset_index['processing_script'].append('')
    # dataset_index['extract_script'].append('y') if 'extract.py' in filenames else dataset_index['extract_script'].append('')

#%%
