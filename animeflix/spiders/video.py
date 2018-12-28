# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from scrapy.selector import Selector

import re

class VideoSpider(scrapy.Spider):
    name = 'video'
    allowed_domains = ['animeisme.com']
    start_urls = ['http://animeisme.com/nonton-gaikotsu-shotenin-hondasan-sub-indo/episode-12/']

    def parse(self, response):
        title = response.xpath('//header[@class="entry-header"]/h1/a/@title').extract_first()
        episode = response.url
        description = response.xpath('//div[@itemprop="description"]/text()').extract_first().strip()
        rating = response.xpath('//table/tr/td/div/strong/text()').extract_first()
        category = response.xpath('//table/tr/td/a/text()').extract_first()
        image = response.xpath('//div[@class="col-md-3"]/img/@src').extract_first()
        

        self.driver = webdriver.PhantomJS('../ghostdriver/bin/ghostdriver')
        self.driver.get(response.url)
        iframe = self.driver.find_element_by_id("mvframe")
        
        self.driver.switch_to.frame(iframe)

        sel = Selector(text=self.driver.page_source)
        video = sel.xpath('//video/source/@src').extract_first()

        self.driver.close()
        

        yield {
            "title":title,
            "episode":episode,
            "description":description,
            "rating":rating,
            "category":category,
            "video":video
        }


    def clean_text(self, text):
        text = text.replace("Nonton", "")
        text = text.replace("Sub", "")
        text = text.replace("Indo","")
        text = text.replace("Streaming", "")
        text = text.replace("Online", "")
        return text
        
