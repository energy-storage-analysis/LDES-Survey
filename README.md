# Energy Storage Material Capital Cost Analysis

This repository contains the codes used to generate the dataset and figures associated with the "A Technoeconomic Survey of Long Duration Energy Storage Viability" Article. More information and interactive visualizations can be found [here](https://mhdlab.github.io/projects/5_ES_TEA/)

The folder structure of the repository is outlined below. Most folders have README files that contain further information.

* cap_cost: The main codes and analysis to form the dataset and figures analyzing the energy capital cost of a wide range of energy storage media. This folder contains the main dataset and individual source datasets used in the work in the form of csv files. 
* es_utils: A package of utility functions used throughout the codebase
* figures: SVG files for schematics used in the main text.
* GESDB: Analysis of the DOE Global Energy Storage Database (Figure 1 in main text)
* lcos: Analysis of the levelized cost of storage. 
* seaborn: Fork of the seaborn library used for tweaked figure generation methods
* SI_docs: Writing and scripts to generate the supporting information document. 

## Installation

The codes in this work were run on Windows with VS Code running a linux terminal with Git Bash. The Python packages were managed with conda and an environment file was exported such that the environment can be recreated with the command `conda env create -f environment.yml`. The `environment_from_history.yml` was created with the `--from-history` flag, which may work on systems other than Windows. 

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

In general, Python scripts are meant to be run in their respective folders in a linux shell (i.e. `cd` into their directory). This can be accomplished on windows by installing Git Bash. The `run_all.sh` script in the top folder of the repository is a main script that runs various other shell and Python scripts to form the final dataset and generate the final analysis. This main script also serves as a high level overview of the data flow used in this work, and which folders or sub shell scripts to examine for further information about a specific portion of the process.  