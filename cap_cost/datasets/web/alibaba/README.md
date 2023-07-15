# Alibaba

This dataset is a set of prices obtained by webscraping alibaba with the `scrapy` python package. A list of search strings, The corresponding molecular formula, strings that the result title must contain, and strings that the title can not contain are determined manually. The scraper then iterates through the searchers and pulls the first page of results. Items with 'fake' prices (i.e. 0.001$/ton) prices are dropped.  

The minimum order quantity must be at least a kilogram. When the price is in the form of a range "low-high" the low price is taken to correspond with bulk order quantity. The median is taken of all prices. 

Certain materials are tagged as hydrates. In these materials the number of hydrates in the molecular formula is determined by searching the title for strings (monohydrat, dihydrat, etc.) and then the price is scaled by the ratio of the molecular weights of the hydrated and anhydrous molecules. This means that all prices are scaled to correspond to the anhydrous molecular formula. 

For a few materials prices are added manually to `single_manual.csv`, which are combined with the scraped data before processing. 

Accessed on 06/25/2022 for scraped prices. Manual data obtained at various times from 2022 to 2023 (see git history).
## Development
The webscraper is based on

https://github.com/scrapehero/alibaba-scraper

The searches are defined in `resources/mat_data_searches.csv` and the CSS fields to scrape are determined in `resources/search_results.yml` which is formed with the help of the selectorlib chrome extension. 


There is also a `single_manual.csv` file for manually adding entries, which will be combined with the scraped data with a preference for scraped data. 

the main command is `scrapy crawl alibaba_crawler`. This is then followed by `extract.py` and then `process.py`. the main csv file with the searches in it is found in `scrapy_alibaba/resources/mat_data_searches.csv` and was formed by finding a search that seemed to mainly show the revevant material in the results, with an added 'must contain' word. 

TODO: currently a different conda environment is used for scraping, but they should be merged once code is finalized. 

TODO: the spider will attempt to pull prices from the main search page, but doesn't step into the product pages yet. 

the returned data are processed in `pipelines.py`, some conditions on the data drop those responses and around output into `output/items_dropped.jl`. The remaining items to be utilized are output into `items.jl`. 

The data output by `extract.py` has a column 'keep' that can be made empty to remove an entry from the output dataset. after aquiring a reasonable dataset I look through the titles and remove any that don't match the index reasonably. 
TODO: The intention is that a column is added to the original search csv file for 'cant_contain' words and for the next iteration of scraping words can be added on the bassis of entries that were removed during the previous scraping session, minimizing the incorrect entries. 

`runner.py` will run the main scrapy command from a python file so a debugger can be used. 

`run_many.sh` runs the command multiple times from a shell script (this cannot be done with scrapy execute) because the results that are returned seem somewhat random, so I am dealing with this somewhat by just acquiring multiple datasets (scraping runs) for everything, then combining those acquisitions and dropping duplicates. 

