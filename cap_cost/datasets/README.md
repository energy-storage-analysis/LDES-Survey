# Energy capital cost raw datasets

This folder contains raw datasets and their data extraction/processing codes. New datasets can be added here. Each source is declared in `dataset_index.csv` and this file will be used in the data consolidation process. When adding a new dataset, `gen_dataset_index.py` needs to be run again. All datasets can be extracted and/or processed with the `process_all.sh` script. 

Note that the raw data (including PDF files) for each source needed to run `process_all.sh` is not included in this repository. However, forming new processed data (described below) for a new dataset, or removing existing data from `dataset_index.csv` can be performed and then the consolidation scripts in the `cap_cost` folder can be run to alter the final dataset in the `data_consolidated` folder. To reproduce the processing of individual datasets, contact the author for the raw data, or follow the instructions in the source readme files. The files where raw data is needed can be determined by running `process_all.sh` and following errors for missing files. 

Ultimately, each source needs the following files in its directory.  

* `README.md`: Readme file describing source and qualitatively describing the processing steps. This file will be consolidated together with the `consolidate_readme.py` script (for supporting information of publication). Note anything after the `## Development` section in the markdown file will be ignored in this consolidation step. 
* `output/SM_data.csv` : Physical properties and materials composition of the storage media declared in the source
* `output/mat_data.csv`: Price data for single materials

The output files can be created manually, but most often are created through the extraction and processing of a raw dataset.


In general there are the following steps for each individual dataset:
1. Data extraction: Try and extract data in source (e.g. pdf table) and keep as close to original source as possible.
    * pdf extraction
    * cleaning, removing bad characters, dashes, etc.
2. Data processing: Conversion to get datasets in to consistent output structure to be compared/combined
    * convert material names to a consistent set of names using `mat_lookup.csv`
    * convert storage media names to desired names using `SM_lookup.csv`
    * Unit conversion (e.g to $/kg)
    * Define storage medium type/technology

3. run `gen_dataset_index.py`
4. If the dataset contains prices (`mat_data.csv`), Add the dataset year to `dataset_years.csv`


