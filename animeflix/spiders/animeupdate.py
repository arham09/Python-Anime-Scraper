# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request

import re


class AnimeupdateSpider(Spider):
    name = 'animeupdate'
    allowed_domains = ['animeisme.com']
    start_urls = ['http://animeisme.com']

    def parse(self, response):
        link = response.xpath('//section[@class="featured"]/div[@class="grid row"]')[0]
        updates = link.xpath('.//div[@class="col-md-125 col-xs-50 col-sm-3"]/div[@class="grid-item"]/div[@class="mask"]/figure/figcaption/a/@href').extract()
        for update in updates:
            update_url = response.urljoin(update)
            yield Request(update_url, callback=self.parse_anime)

    
    def parse_anime(self, response):
        print(response.url)
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


    def clean_text(self, text):
        text = text.replace("Nonton", "")
        text = text.replace("Sub", "")
        text = text.replace("Indo","")
        text = text.replace("Streaming", "")
        text = text.replace("Online", "")
        return text