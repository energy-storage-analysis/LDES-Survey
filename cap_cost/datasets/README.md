# Energy capital cost raw datasets

This folder contains raw datasets and their data extraction/processing codes. Each source is declared in `dataset_index.csv` and this file will be used in the data consolidation process. Ultimately, each source needs the following files in its directory. 

* `README.md`: Readme file describing source and qualitatively describing the processing steps. This file will be consolidated together with the `consolidate_readme.py` script (for supporting information of publicaiton). Note anything after the `## Development` section in the markdown file will be ignored in this consolidation step. 
* `output/SM_data.csv` : Physical properties and materials composition of the storage media declared in the source
* `output/mat_data.csv`: Price data for single materials

The output files can be created manually, but most often are created through the extraction and processing of a raw dataset.


In general there are the following steps for each individual dataset:
1. Data extraction: Try and extract data in source (e.g. pdf table) and keep as close to original source as possbile.
    * pdf extraction
    * cleaning, removing bad characters, dashes, etc.
2. Data processing: Conversion to get datasets in to consistent output structure to be compared/combined
    * convert material names to a consistent set of names using `chem_lookup.csv`
    * convert storage media names to desired names using `SM_lookup.csv`
    * Unit conversion (e.g to $/kg)
    * Define storage medium type/technology


