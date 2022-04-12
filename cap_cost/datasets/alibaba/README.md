Alibaba data scraped using https://github.com/aspitarl/alibaba-scraper

two datasets

manual - combination of manual entries and semi-tailored search

bulk - data obtained by looping through all materials in the consoidated mat data

both dataset use extract.py to parse the raw scraped data (out.csv). Then those files are copied into _edit and titles deleted on results that don't correspond to the searched material. then run process.py