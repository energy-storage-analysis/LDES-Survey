scrapy crawl alibaba_crawler -a spider_iter=1
scrapy crawl alibaba_crawler -a spider_iter=2
scrapy crawl alibaba_crawler -a spider_iter=3

cd scraped_data/temp

cat items_?.jl > items_combine.jl
cat items_dropped_?.jl > items_dropped_combine.jl

cd ..

mv temp/items_combine.jl items.jl
mv temp/items_dropped_combine.jl items_dropped.jl