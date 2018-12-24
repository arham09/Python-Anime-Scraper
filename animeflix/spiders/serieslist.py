# -*- coding: utf-8 -*-
import scrapy

import re
import os
import csv
import glob
import MySQLdb


class SerieslistSpider(scrapy.Spider):
    name = 'serieslist'
    allowed_domains = ['animeisme.com']
    start_urls = ['http://animeisme.com/anime-list/']

    def parse(self, response):
        series = response.xpath('//div[@class="col-md-15"]/div[@class="col-md-5 listanim"]/a/text()').extract()
        for serial in series:
            yield {
                "series":serial
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
                    'INSERT INTO series (series) VALUES (%s)', row)
            row_count += 1

        mydb.commit()
        cursor.close() 