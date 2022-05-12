# Material cost dataset accumulation

In general there are the following steps for each individual dataset:
1. Data extraction: Try and extract data in source (e.g. pdf table) and keep as close to original source as possbile.
    * pdf extraction
    * cleaning, removing bad characters, dashes, etc.
2. Data processing: Conversion to get datasets in to consistent output structure to be compared/combined
    * convert material names to a consistent set of names using `chem_lookup.csv`
    * convert storage media names to desired names using `SM_lookup.csv`
    * Unit conversion (e.g to $/kg)
    * Define storage medium type/technology


