# -*- coding: utf-8 -*-
import scrapy


class Le360Spider(scrapy.Spider):
    name = 'le360'
    allowed_domains = ['www.fr.le360.ma']
    start_urls = ['http://www.fr.le360.ma/']

    def parse(self, response):
        pass
