# Final Datasets

This folder contains the final datasets.

 * `mat_data.csv`: Contains information about the constituent materials of the storage media
    * minimum specific price between all sources (can also be changed to median or other statistic in `consolidate_data.py`). 
    * How many sources, how many storage media the material is used in
    * The molecular formula if applicable
    * Materials are indexed to a unique identifier. Usually the molecular formula when applicable, otherwise a unique name. 
* `SM_data.csv`: Contains information about each storage media including
    * The various physical properties used to calculate C_kwh
    * The total specific price, energy, and C_kwh
    * The material specification, either a single material, or a combination of materials in the format [(name 1, fraction 1), (name 2, fraction 2), ...] on a mass or molar fraction basis (specified in a separate column)

There are also corresponding dataset ending in `_all`. These correspond to the raw consolidated, but not combined, data from each source. So, these files contain duplicate storage media or materials from different sources. 

The `SM_column_info.csv` files contains full names for the columns in the storage medium datasets. 