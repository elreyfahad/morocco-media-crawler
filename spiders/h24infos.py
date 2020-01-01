# -*- coding: utf-8 -*-
import scrapy

import re
import logging
import json

class H24infosSpider(scrapy.Spider):
    name = 'h24infos'
    custom_settings = {
        
        'LOG_LEVEL': logging.WARNING,

        'FEED_FORMAT':'csv', # format d'exportation
        'FEED_URI': 'h24infos.csv', # fichier d'exportation
        'FEED_EXPORT_ENCODING': 'utf-8', #encodage
        'COOKIES_ENABLED ': False, # Disable cookies (enabled by default)
    
        'ROBOTSTXT_OBEY': False ,# Obey robots.txt rules
        

    }
    #allowed_domains = ['www.h24info.ma']
    start_urls = ['http://www.h24info.ma/maroc']

    def parse(self, response):

        links=response.css("h3[class='entry-title td-module-title'] a::attr(href)").getall()

        for link in links:
             yield scrapy.Request(link,callback=self.parse_article)

        next_page=response.css("div[class='page-nav td-pb-padding-side'] a::attr(href)").getall()[-1]

        if next_page is not None:
            #repete les meme operation que precedement
            yield response.follow(next_page,callback=self.parse)

    
    def parse_article(self,response):

        resume=response.css("p strong::text").get() 

        date=response.css("span time::text").get()
        
        date=date.split(",")

        mois=date[0]
        year=date[1].split()[0]

        date=mois+" "+year
        title=response.css("h1.entry-title::text").get() #recupere le titre

        if int(year)>2017 and resume:
            yield {"title":title,"resume":resume,"date":date,"url":response.url} 
