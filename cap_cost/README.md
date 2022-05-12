# Energy Capital Cost data acumulation

The codes in this folder collect and analyze data to estimate the energy capital cost ($/kWh) of different storage media. The collected data consists of two main components:

* Material specific prices ($/kg)
* Storage media, defined principally as
    * one or more materials, used to calculate total specific price
    * a set of physical properties, used to calculate the specific energy (kWh/kg)


The data are extracted and processed from the primary sources in the `datsets` folder, there is a readme file in there for more information. The `consolidate_data.py` script collects data from each source's folder in the `datasets` folder, and consolidates them into a set of main csv files in the `data_consolidated` folder. This script is followed by `calc_Ckwh.py` which calculates the energy capital cost (AKA C_kwh ~ $/kWh). 

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

Finally, the `analysis` folder contains various scripts that generate the visualizations of the data. These visualizations are output into the `output` folder, which is not version controlled (so figures do not show on GitHub)

The `run_all.sh` shell script can be used to run the above scripts and visualzations scripts in sequence (also describing the process to arrive at final figures). 
