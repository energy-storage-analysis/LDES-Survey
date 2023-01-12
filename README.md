# Energy storage analysis

This repository contains the codes used to generate the dataset and figures associated with the "First-Principles AnalysisFirst Principles Analysis of Long Duration Energy Storage Technologies" Article. The folder structure is 

* cap_cost: The main codes and analysis to form the dataset and figures analyzing the energy capital cost of a wide range of energy storage media. This folder contains the main dataset and individual source datasets used in the work in the form of csv files. See the README file in that folder for more information. 
* es_utils: A package of utility functions used throughout the codebase
* figures: SVG files for schematics used in the main text.
* GESDB: Analysis of the DOE Global Energy Storage Database (Figure 1 in main text)
* lcos: Analysis of the levelized cost of storage. 
* seaborn: Fork of the seaborn library used for tweaked figure generation methods
* SI_docs: Writing and scripts to generate the supporting information document. 

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

## Generating the dataset and figures

In general scripts are meant to be run in their respective folders in a linux shell (i.e. `cd` into their directory). This can be accomplished on windows by installing Git Bash. 

1. The data extraction and processing for each individual source can be performed with the shell script `cap_cost\datasets\process_all.sh`

2. Then the data is consolidated as visualizations generated with by running `run_all.sh vis` in the `cap_cost` folder. Final figures are output into `cap_cost\figures\final\output`

3. The source metadata is generated with the `cap_cost\source_meta\run_all.sh` shell script. 

4. The supporting information documentation is generated with the `SI_docs\gen_SI.sh` shell script. 
