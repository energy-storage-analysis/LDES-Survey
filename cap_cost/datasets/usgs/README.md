Commodity price data from the U.S. Geological Survey Mineral Commodity Summaries 2022 Data Release. Data is obtained from the 'salient' dataset which contains commodity data for the last 5 years. 

Data is obtained from the following website: 
https://www.sciencebase.gov/catalog/item/6197ccbed34eb622f692ee1c

## Development
The raw USGS data consists of a series of csv file and xml metadatafiles. The raw data is not included in the repository.

1. Download and extract the 'sailient' dataset from the USGS link above into a folder called `data`, meaning that raw data files are located in `data/salient`. 
2. run extract.py
3. run process.py