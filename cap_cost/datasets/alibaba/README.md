# Alibaba scraping

This dataset contains price data obtained from webscraping alibaba based on 

https://github.com/scrapehero/alibaba-scraper

There is also a `single_manual.csv` file for manually adding entries, which will be combined with the scraped data with a preference for scraped data. 

the main command is `scrapy crawl alibaba_crawler`. This is then followed by `extract.py` and then `process.py`. the main csv file with the searches in it is found in `scrapy_alibaba/resources/mat_data_searches.csv` and was formed by finding a search that seemed to mainly show the revevant material in the results, with an added 'must contain' word. 

TODO: currently a different conda environment is used for scraping, but they should be merged once code is finalized. 

TODO: the spider will attempt to pull prices from the main search page, but doesn't step into the product pages yet. 

the returned data are processed in `pipelines.py`, some conditions on the data drop those responses and around output into `output/items_dropped.jl`. The remaining items to be utilized are output into `items.jl`. 


`runner.py` will run the main scrapy command from a python file so a debugger can be used. 

`run_many.sh` runs the command multiple times from a shell script (this cannot be done with scrapy execute) because the results that are returned seem somewhat random, so I am dealing with this somewhat by just acquiring multiple datasets (scraping runs) for everything, then combining those acquisitions and dropping duplicates. 

