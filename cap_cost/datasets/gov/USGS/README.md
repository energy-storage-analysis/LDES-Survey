# USGS

Commodity price data was obtained from the [U.S. Geological Survey Mineral Commodity Summaries 2022 Data Release](https://www.sciencebase.gov/catalog/item/6197ccbed34eb622f692ee1c). The 'salient' dataset was used which contains commodity data for the last five years. During the data processing the price is averaged over these last five years and the units are converted to `USD/kg`.

## Development
The raw USGS data consists of a series of csv file and xml metadatafiles. The raw data is not included in the repository.

1. Download and extract the 'sailient' dataset from the USGS link above into a folder called `input_data`. 
2. run extract.py
3. run process.py