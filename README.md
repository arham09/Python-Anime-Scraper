# Python-Anime-Scraper

Scrapping for animeisme

## Requirement

### Prerequisites
- Python - Download and Install [Python](https://www.python.org/)
- Pip - Download and Install [Pip](https://pypi.org/project/pip/) 

```
  $ pip install -r requirements.txt

```

## Run Program

Run command to starts scraping

**Start application**

```
$ cd folder
$ scrapy crawl <spidername>

```
## Spider

1. animeupdate (For daily update scrapping)


## Insert to DB

### 1. Manual Insert

uncomment code from line 68 - 85
```
scrapy crawl animeupdate -o anime.csv
```
Scrapy will automatically generate csv file and insert to DB

### 2. API Insert
Using request library, create insert api to automatically insert to db
