# pdf table scraping instructions

PDFs are extracted using tabula web interface to find the table region, then those regions are used with the camelot package for actual extraction. I couldn't get the camelot web interface to work. 

## Running tabula

use tabula to extract the table regions. I had to run tablula with a different port as described here

https://github.com/tabulapdf/tabula#known-issues

`java -Dfile.encoding=utf-8 -Xms256M -Xmx1024M -Dwarbler.port=9999 -jar tabula.jar`

had to press ctrl-C in the prompt to get the web page to unfreeze

## Adding a new table extraction

## PDF table instructions



1. extract table with tabula
2. export to `tabula_template.json`
3. copy `tablua_template.json` to `extract_settings.json` and delete all contents of each list element leaving a blank dictionary. This is where you can add settings to pass into camelot for each table, but can be left blank if default settings extract all tables. Using a vscode extension to 'prettify' the json file helps here. 
    * column_rows: number of rows at the top to combined into column names
4. copy an `extract_template.py` script and set specific info in the script. 


## processing data

1. load in the data using processing template
2. output the table as SM_lookup.csv or mat_lookup.csv to form lookup tables to conform names to standard SM or mat indexes
3. add the dataset to the dataset index