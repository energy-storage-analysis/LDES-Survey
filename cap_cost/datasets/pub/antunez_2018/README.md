Antunez, P. F. Modelling and Development of Thermo-Mechanical Energy Storage. University of Cambridge, 2018.

This dataset is extracted from Table 1.1 which includes physical properties and cost data of sensible thermal storage including cold storage media. 

## Development

I couldn't get the tabula template to work properly, which I think has to do with the fact that the table is rotated but there is still regular text on the page. Adding rotate extract setting to 90 was needed but not sufficient. I had to manually swap x2 and y2 in the tabula_template.json (and dial them in a bit). 

TODO: I added a extration keword to do this now ('table_rotate'), but it's hacky and nees to be revisted. See extract_dfs function. 