# -*- coding: utf-8 -*-
import scrapy
import re
import logging
import json

class HespressSpider(scrapy.Spider):
    name = 'hespress'
    custom_settings = {
        
        'LOG_LEVEL': logging.WARNING,

        'FEED_FORMAT':'csv', # format d'exportation
        'FEED_URI': 'hespress.csv', # fichier d'exportation
        'FEED_EXPORT_ENCODING': 'utf-8', #encodage
        'COOKIES_ENABLED ': False, # Disable cookies (enabled by default)
    
        'ROBOTSTXT_OBEY': False ,# Obey robots.txt rules
        

    }
    #allowed_domains = ['www.fr.hespress.com']
    start_urls = ['https://fr.hespress.com/societe?action=ajax_listing&type=category&id=9&paged=1',#societe
    'https://fr.hespress.com/societe?action=ajax_listing&type=category&id=2&paged=1',#politique
    'https://fr.hespress.com/societe?action=ajax_listing&type=category&id=6&paged=1',#marocains dans le monde
    'https://fr.hespress.com/societe?action=ajax_listing&type=category&id=8&paged=1',#faits divers
    'https://fr.hespress.com/societe?action=ajax_listing&type=category&id=66&paged=1',#culture
    ]
    #start_urls=["https://fr.hespress.com/?action=ajax_listing&paged=1"] #tous les articles

    def parse(self, response):
        
        #recupere les liens des articles de la page et leurs titres
        links_articles=response.css(".thumbnail-tall a::attr(href)").getall()
        #title_articles=response.css(".thumbnail-tall a::attr(title)").getall()

        url=response.url
        
        #date publication

        dates=response.css(".time::text").getall()
        for link,date in zip(links_articles,dates):

            year= int(date.split()[2]) #recupere l'année du publication

            if year > 2017 : #test si l'année est superieur a 2017
                
                yield scrapy.Request(link,callback=self.parse_article,meta={"date":date})
        
        page_num=url[-1] #le numero de la page courant qui est le dernier caracter de l'url

        if int(page_num)<2000: #s'il est infieur a 2000

            next_page=re.sub(page_num,str(int(page_num)+1),url) #remplace le numero du page courant par la page svt
             #repete les meme operation que precedement
            yield response.follow(next_page,callback=self.parse)
    
    def parse_article(self,response):
        date=response.meta.get("date")

        title= response.css("div[class='col article-container'] h1::text").get() #recupere le titre
        resume=response.css("div.content p strong::text").get() #recupere le resumé de l'article ecris en gras

        #article=response.css("div.content p").getall() #recupere les paragraphe de l'article
        #article=" ".join(article) #join les paragraphes
        #article=re.sub("<[^>]*>"," ",article) #supprime les tags html

        yield {"title":title,"resume":resume,"date":date} #"article":article
                 



