# Energy storage analysis

## Installation

the es_utils module in the base path of the repository needs to be accessed. This can be done using conda by running `conda develop .` in the repository directory

You need to create a file called `.env` in the root repository directory with the following info

```
PDF_FOLDER_PATH='C:\Users\your\path\to_pdf_files'
REPO_DIR='C:\Users\aspit\Git\MHDLab-Projects\Energy-Storage-Analysis'
```

The some custom changes have been made to the seaborn plotting library and it is included as a git submodule of a fork on GitHub. To initialize run

```
git submodule init
git submodule update
cd seaborn
python setup.py develop
```

## Generating the figures

```
cd cap_cost
./run_all.sh
```
Once that is finished
```
cd analysis
./genvis_all.sh
```

Final figures are output into `analysis/figures/output`