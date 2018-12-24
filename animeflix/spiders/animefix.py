# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request

import re
import os
import csv
import glob
import MySQLdb


class AnimefixSpider(Spider):
    name = 'animefix'
    allowed_domains = ['animeisme.com']
    start_urls = ['http://animeisme.com/anime-list/']

    def parse(self, response):
        series_url = response.xpath('//div[@class="col-md-15"]/div[@class="col-md-5 listanim"]/a/@href').extract()
        for serial in series_url:
            serial_url = response.urljoin(serial)
            yield Request(serial_url, callback=self.parse_list)

    
    def parse_list(self, response):
        episodes_list = response.xpath('//div[@id="pl"]/a/@href').extract()
        for episode in episodes_list:
            episode_url = response.urljoin(episode)
            yield Request(episode_url, callback=self.parse_episode)


    def parse_episode(self, response):
        title = response.xpath('//header[@class="entry-header"]/h1/a/@title').extract_first()
        episode = response.url
        description = response.xpath('//div[@itemprop="description"]/text()').extract_first().strip()
        rating = response.xpath('//table/tr/td/div/strong/text()').extract_first()
        category = response.xpath('//table/tr/td/a/text()').extract_first()
        image = response.xpath('//div[@class="col-md-3"]/img/@src').extract_first()
        video = response.css('iframe::attr(src)').extract_first()

        serial_fix = self.clean_text(title.strip())
        serial_ab = serial_fix.strip()
        episode_fix = next(re.finditer(r'\d+$', episode)).group(0)
        title_fix = serial_ab + " Episode " + episode_fix 
        
        yield {
            "title":title_fix,
            "series":serial_ab,
            "rating":rating,
            "category":category,
            "episode":episode_fix,
            "description":description,
            "image":image,
            "video":video            
        }

    
    def close(self, reason):
        csv_file = max(glob.iglob('*.csv'), key=os.path.getctime)

        mydb = MySQLdb.connect(host='localhost', user='root', password='root', db='animeflix', charset='utf8')
        cursor = mydb.cursor()

        csv_data = csv.reader(open(csv_file))

        row_count = 0
        for row in csv_data:
            if row_count != 0:
                cursor.execute(
                    'INSERT INTO videos (title, series, rating, category, episode, description, image_url, video_url, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW())', row)
            row_count += 1

        mydb.commit()
        cursor.close() 


    def clean_text(self, text):
        text = text.replace("Nonton", "")
        text = text.replace("Sub", "")
        text = text.replace("Indo","")
        text = text.replace("Streaming", "")
        text = text.replace("Online", "")
        return text