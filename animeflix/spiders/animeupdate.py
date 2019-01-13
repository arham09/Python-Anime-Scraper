# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request
from selenium import webdriver
from scrapy.selector import Selector


import re
import os
import csv
import glob
import MySQLdb


class AnimeupdateSpider(Spider):
    name = 'animeupdate'
    allowed_domains = ['animeisme.me/']
    start_urls = ['https://animeisme.me/']

    def parse(self, response):
        link = response.xpath('//section[@class="featured"]/div[@class="grid row"]')[0]
        updates = link.xpath('.//div[@class="col-md-125 col-xs-50 col-sm-3"]/div[@class="grid-item"]/div[@class="mask"]/figure/figcaption/a/@href').extract()
        for update in updates:
            update_url = response.urljoin(update)
            yield Request(update_url, callback=self.parse_anime, dont_filter=True)

    
    def parse_anime(self, response):
        print(response.url)
        title = response.xpath('//header[@class="entry-header"]/h1/a/@title').extract_first()
        episode = response.url
        description = response.xpath('//div[@itemprop="description"]/text()').extract_first().strip()
        rating = response.xpath('//table/tr/td/div/strong/text()').extract_first()
        category = response.xpath('//table/tr/td/a/text()').extract_first()
        image = response.xpath('//div[@class="col-md-3"]/img/@src').extract_first()

        self.driver = webdriver.PhantomJS('/home/arham/node_modules/ghostdriver/bin/ghostdriver')
        self.driver.get(response.url)
        iframe = self.driver.find_element_by_id("mvframe")
        
        self.driver.switch_to.frame(iframe)

        sel = Selector(text=self.driver.page_source)
        video = sel.xpath('//video/source/@src').extract_first()

        self.driver.close()

        serial_fix = self.clean_text(title.strip())
        serial_ab = serial_fix.strip()
        episode_fix = next(re.finditer(r'\d+$', episode)).group(0)
        title_fix = serial_ab + " Episode " + episode_fix 
        slug = title_fix.replace(" ", "-").lower()

        
        yield {
            "title":title_fix,
            "series":serial_ab,
            "rating":rating,
            "category":category,
            "episode":episode_fix,
            "description":description,
            "image":image,
            "video":video, 
            "slug":slug            
        }


    # def close(self, reason):
    #     csv_file = max(glob.iglob('*.csv'), key=os.path.getctime)

    #     mydb = MySQLdb.connect(host='animedemy.me', user='root', password='toor', db='db_animeflix', charset='utf8', port=3306)
    #     cursor = mydb.cursor()

    #     csv_data = csv.reader(open(csv_file))

    #     row_count = 0
    #     for row in csv_data:
    #         if row_count != 0:
    #             cursor.execute(
    #                 'INSERT IGNORE INTO videos (title, series, rating, category, episode, description, image_url, video_url, slug, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())', row)
    #         row_count += 1
        
    #     mydb.commit()
    #     cursor.close()
    #     mydb.close()

    def clean_text(self, text):
        text = text.replace("Nonton", "")
        text = text.replace("Sub", "")
        text = text.replace("Indo","")
        text = text.replace("Streaming", "")
        text = text.replace("Online", "")
        return text