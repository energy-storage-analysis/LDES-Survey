# Energy Capital Cost data accumulation

The codes in this folder collect and analyze data to estimate the energy capital cost ($/kWh) of different storage media. The collected data consists of two main components:

* Material specific prices ($/kg)
* Storage media, defined principally as
    * one or more materials, used to calculate total specific price
    * a set of physical properties, used to calculate the specific energy (kWh/kg)


The data are extracted and processed from the primary sources in the `datasets` folder, there is a readme file in each source's folder that contains more information about that specific source and the processing steps used. Only the processed 'output' data for each source is included in this repository. For more information on adding additional data or reproduce the processing of each source, see  the README file in the `datasets` folder.

The `consolidate_data.py` script collects data from each source's folder in the `datasets` folder, and consolidates them into a set of main csv files in the `data_consolidated` folder. This script is followed by `calc_Ckwh.py` which calculates the energy capital cost (AKA C_kwh ~ $/kWh). 

The `data_consolidated` folder contains two important csv files that comprise the main dataset of this work.

The `figure_panels` folder contains various scripts that generate the figure panels (individual plots in figures) of the data. 
The `source_meta` folder contains scripts that generate metadata about the datasets in the form of tables. 

The `gen_dataset.sh` shell script can be used to run the consolidation and calculation scripts. Adding the `vis` argument will also run the visualization generation shell script `figure_panels/genvis_all.sh`.
