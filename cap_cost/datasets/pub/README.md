# Publication datasets

This folder contains datasets from typically peer reviewed publications, usually in the form of pdfs. Most often, the data is extracted directly from pdfs. 


## pdf table scraping instructions


The first step is to copy the `extract_template.py` and `process_template.py` files into the source folder and rename them removing the `_template` suffix. 
### Running tabula

PDFs are extracted using tabula web interface to find the table region, then those regions are used with the camelot package for actual extraction. I couldn't get the camelot web interface to work. 

I had to run tabula with a different port as described here
https://github.com/tabulapdf/tabula#known-issues

This the command to run in a command prompt. 
`java -Dfile.encoding=utf-8 -Xms256M -Xmx1024M -Dwarbler.port=9999 -jar tabula.jar`

Once tabula is running import a pdf file

1. Define table regions and then select templates -> save template.
2. Go to to the templates page and export the tempate in the source folder as `tabula_template.json`


## Extracting pdf data


1. run `python extract.py` which will give a first pass at extracting the tables as well as generate a `extract_settings.json` file. 
2. `extract_settings.json` is where you can add specific table extraction settings for each table. There are settings that are passed into the `es_utils.pdf.extract_dfs` function which is a wrapper around the `camelot.read_pdf` function of the camelot package.
 
* extract_dfs settings 
    * "page_rotate" (= 90): is the table rotated? (TODO: sometimes this behaves strangely)
    * "column_rows": how many rows should be concatenated together  
* important camelot settings (see camelot documentation)
    * row_tol 
    * columns

Keep running `extract.py` and dialing in the settings. This can include cleaning of the extracted dataframes. The idea is to extract the table generally as close as possible to as it appears in the pdf, but easily loaded into the processing script (e.g. replacing bad characters etc)


## processing data

The processing data script then takes the extracted dataset and creates the output datasets. 

1. load in the data using `processing.py`
2. output the table as SM_lookup.csv or mat_lookup.csv to form lookup tables to conform names to standard SM or mat indexes
    * SM_lookup.csv columns : original_name, SM_name, SM_type, materials, mat_basis
    * mat_lookup.csv columns: orignal_name, material_name, molecular_formula, index_use
3. add the dataset to the dataset index
