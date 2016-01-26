# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from topspider.items import NdtvItem



class NdtvSpider(scrapy.Spider):
    name = "ndtv"
    allowed_domains = ["ndtv.com"]
    start_urls = (
            'http://ndtv.com',
    )

    def parse(self, response):
        if 'www.ndtv.com' in response.url:
            soup = BeautifulSoup(response.body, "lxml")
            items = [(x[0].text, x[0].findChildren()[0].get('href')) for x in
                    filter(None, [
                        x.findChildren() for x in
                        soup.findAll('div', {'class': 'description'})
                        ])
                    ]
            for item in items:
                article = NdtvItem()
                article['title'] = item[0]
                article['link'] = item[1]
                try:
                    if  article['link'] != None:
                        yield scrapy.http.Request(article['link'], 
                                callback=self.parse_content,
                                meta={'article':article})
                except ValueError:
                    pass
                    #yield article
            return

    def parse_content(self, response):
        article = response.meta['article']
        soup = BeautifulSoup(response.body, "lxml")
        item = soup.find(id='ins_storybody')
        try:
            article['content'] = item.text
        except AttributeError as e:
            pass
        return article

