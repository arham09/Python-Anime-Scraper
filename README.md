# Python-Anime-Scraper

### Requirement

pip install
```
pip install -r requirements.txt
```
## Insert to DB

### 1. Manual Insert
uncomment code from line 68 - 85

Set the Db environment

run the spider : scrapy crawl animeupdate -o anime.csv

Scrapy will automatically generate csv file and insert to DB

### 2. API Insert
Using request library, create insert api to automatically insert to db
