# -*- coding: utf-8 -*-
import scrapy

import re
import logging
import json
class BladiSpider(scrapy.Spider):
    name = 'bladi'
    #allowed_domains = ['www.bladi.net']

    custom_settings = {
        
        'LOG_LEVEL': logging.WARNING,

        'FEED_FORMAT':'csv', # format d'exportation
        'FEED_URI': 'bladi.csv', # fichier d'exportation
        'FEED_EXPORT_ENCODING': 'utf-8', #encodage
        'COOKIES_ENABLED ': False, # Disable cookies (enabled by default)
    
        'ROBOTSTXT_OBEY': False ,# Obey robots.txt rules
        

    }

    
    start_urls = ['https://www.bladi.net/maroc.html?debut_suite_rubrique=0#pagination_suite_rubrique']

    def parse(self, response):
        
        links=response.css("div.grid4 a::attr(href)").getall()

        url=response.url

        

        for link in links:
            link="http://www.bladi.net/"+link
            yield scrapy.Request(link,callback=self.parse_article)


        num_page=re.findall("=\d+",url)[0] #recupere le '=num_page'
        num_page=num_page.split("=")[1] #supprimme le '=' pour recuperer juste le numero de la page
        num_page=int(num_page)

        if  num_page <= 1764:

            next_page=re.sub("=\d+","="+str(num_page+12),url)

            if next_page is not None:
                #repete les meme operation que precedement
                yield response.follow(next_page,callback=self.parse)

    
    def parse_article(self,response):

        date=response.css("p[class='datenews mbs']::text").get().split("-")[0]

        title= response.css("div[class='magauche pas article'] h1::text").get() #recupere le titre
        resume=response.css("div[class='mbs mtm'] strong p").get() #recupere le resumé de l'article ecris en gras

        if resume is not None :

            resume=re.sub("<[^>]*>","",resume) #supprime les tags html s'il y'en a
            
            yield {"title":title,"resume":resume,"date":date}