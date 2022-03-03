# Material cost dataset accumulation


## Individual dataset formation
In general there are the following steps for each individual dataset:
1. Data extraction: Try and extract data in source (e.g. pdf table) and keep as close to original source as possbile.
    * pdf extraction
    * dataset cleaning
3. Form lookup table for chemical names to convert to consistent set of names/chemical formulas
2. Data output: Conversion to get datasets in to consistent output structure to be compared/combined
    * Add column of specified chemical name
    * Unit conversion (e.g to $/kg)
    * Combining of tables and adding of metadata


## Dataset combination

Now that each dataset is in a similar form we will form a master sqlite(?) database with two main tables

* chemical data
    * Acumulate list of all chemicals in individual datasets and get pubchem/chemspider data for it. 
    * Parse formulas and get list of elements
    * cost data based on calculation (e.g. all elements, only metal)
* instance data
    * Data of individual chemical occurences. 
    * chemical formula, physical data, energy density, source cost data, source
