# Energy Capital Cost data acumulation

The codes in this folder collect and analyze data to estimate the energy capital cost ($/kWh) of different storage media. The collected data consists of two main components:

* Material specific prices ($/kg)
* Storage media, defined principally as
    * one or more materials, used to calculate total specific price
    * a set of physical properties, used to calculate the specific energy (kWh/kg)


The data are extracted and processed from the primary sources in the `datasets` folder, there is a readme file in each source's folder that contains more information about that specific source and the processing steps used. See the README file in the `datasets` folder for more information. 

The `consolidate_data.py` script collects data from each source's folder in the `datasets` folder, and consolidates them into a set of main csv files in the `data_consolidated` folder. This script is followed by `calc_Ckwh.py` which calculates the energy capital cost (AKA C_kwh ~ $/kWh). 

The `data_consolidated` folder contains two important csv files that comprise the main dataset of this work.

 * `mat_data.csv`: Contains information about the constituent materials of the storage media
    * median and standard deviation of specific price between all sources. 
    * How many sources, how many storage media the material is used in
    * The molecular formla if applicable
    * Materials are indexed to a unique identifier. Usually the molecular formula when applicable, otherwise a unique name. 
* `SM_data.csv`: Contains information about each storage media including
    * The various physical properties used to calculate C_kwh
    * The total specific price, energy, and C_kwh
    * The material specification, either a single material, or a combination of materials in the format [(name 1, fraction 1), (name 2, fraction 2), ...] on a mass or molar fraction basis (specified in a separate column)

The `figure_panels` folder contains various scripts that generate the figure panels (individual plots in figures) of the data. 
The `source_meta` folder contains scripts that generate metadata about the datasets in the form of tables. 

The `gen_dataset.sh` shell script can be used to run the consolidation and calculation scripts. Adding the `vis` argument will also run the visualization generation shell script `figure_panels/genvis_all.sh`.
