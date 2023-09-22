# Long-Duration Energy Storage Energy Capital Cost Survey

This repository contains the codes used to generate the dataset and figures associated with our paper, "A Techno-economic Survey of Energy Storage Media for Long-Duration Energy Storage Applications" Article, currently in submission. A brief overview of the work including interactive visualizations of the dataset formed in this repository can be found [here](https://energy-storage-analysis.github.io/LDES-Viability.html)

**The final datasets for storage medium energy capital cost, storage media physical properties, and material prices can be found in CSV form in [cap_cost/data_consolidated](cap_cost/data_consolidated/)**

The folder structure of the repository is outlined below. The folders have README files that contain further information.

* cap_cost: The main codes and analysis to form the dataset and figures analyzing the energy capital cost of a wide range of energy storage media. This folder contains the final datasets as well as the processed data for individual sources used to form the final datasets. 
* es_utils: A package of utility functions used throughout the codebase.
* figures: Files that layout the final figures used in the text. The SVG files are linked to figure panel image files generated throughout the repository, meaning the final figures will automatically update with changes to the data or processing codes.  
* GESDB: Analysis of the [DOE Global Energy Storage Database](https://sandia.gov/ess-ssl/gesdb/public/index.html).
* lcos: Analysis of the levelized cost of storage. 
* seaborn: Fork of the seaborn library used for tweaked figure generation methods.
* SI_docs: Writing and scripts to generate the supporting information document. 

## Installation

The codes in this work were tested on Windows with VS Code running a linux terminal with Git Bash. The final figure generation was tested with a local python virtual environment with the `requirements/requirements.txt` file, see `requirements/README.md` for more information.  

Some external programs in addition to the python packages (described later) are needed to be installed manually. The excecutables associated with these programs must be added to the system PATH as described [here](https://www.architectryan.com/2018/03/17/add-to-the-path-on-windows-10/).
* [Inkscape](https://inkscape.org/) for SVG to PNG conversion: Install the inkscape program and add the `bin` folder to the PATH. Unfortunately adding the inkscape/bin folder also adds Inkscape's python to the system path, but it appears that this python can be ingored by placing the desired python installation for use in the command line (e.g. the one in Program Files) higher up in the environment variables list than the inskcape folder. 
* [Imagemagick](https://imagemagick.org/script/download.php) for conversion from PNG to final TIFF figures (has option to add to path during installation)
* [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) were required for the installation of python packages. Visual Studio Build Tools was downloaded and installed selecting only 'Desktop development with C++'
* [pandoc](https://github.com/jgm/pandoc) For SI documentation generation




a `.env` file needs to be created in the root repository directory with the following info
```
REPO_DIR='C:\Path\to\this\folder'
PDF_FOLDER_PATH='C:\Users\your\path\to_pdf_files' # If extracting tables from PDF files, not needed if not reproducing the processed source datasets 
```

The final dataset that is needed to generate the figures is included in `cap_cost\data_consolidated`, as well as the processed data for each source that is consolidated into this final dataset. It is not necessary, but to regenerate these processed datasets from each source's raw data, the raw input data files must be added to the repository, along with relevant publication pdf files added to the folder described in the `.env` file. The Readme files for each source give information on how to obtain their raw datasets. See `cap_cost\datasets` for more information on adding new sources or obtaining raw datasets to reproduce the raw data.

The following installation procedure was tested and used to generated the final publication figures. 

2. create a local virtual environment with `python -m venv venv` 
    * Tested using python 3.10.11. Installation did not work with 3.11
3. close the terminal and reopen (activating the newly created venv)
4. run `./install.sh` 
5. run `./run_all.sh` 
    * run `./run_all.sh process` to regenerate processed data (requires raw datasets as described above)

More information on the details of the setup and data processing can be found in the `.sh` scripts (see below)

## Running the codes

In general, Python scripts are meant to be run in their respective folders in a linux shell (i.e. `cd` into their directory). This can be accomplished on windows by installing Git Bash. The `run_all.sh` script in the top folder of the repository is a main script that runs various other shell and Python scripts to form the final dataset and generate the final analysis. This main script also serves as a high level overview of the data flow used in this work, and which folders or sub shell scripts to examine for further information about a specific portion of the process. 

There are various extra scripts, notebooks, etc. that were used throughout the research of this project, but did not contribute to the final figures in the main text or supporting information of this work. Some of these have been kept in case they are useful in the future, but only the scripts outlined in `run_all.sh` have been tested. 


## Development notes

requirements.txt generated with `pipreqs . --encoding=utf8 --ignore venv,seaborn --force` then removing `seaborn` and `cpi`. 
