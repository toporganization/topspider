# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from topspider.items import TopspiderItem


class HacknewsSpider(scrapy.Spider):
    name = "hacknews"
    allowed_domains = []
    start_urls = (
        'https://news.ycombinator.com/',
    )

    def parse(self, response):
        if 'news.ycombinator.com' in response.url:
            soup = BeautifulSoup(response.body, "lxml")
            items = [(x[1].text, x[1].get('href'),x[1]) for x in
                    filter(None, [
                        x.findChildren() for x in
                        soup.findAll('td', {'class': 'title'})[1::2]
                        ])
                    ]

            for item in items:
                print item
                hn_item = TopspiderItem()
                hn_item['title'] = item[0]
                hn_item['link'] = item[1]
                try:
                    yield scrapy.http.Request(item[1], callback=self.parse)
                except ValueError:
                    yield scrapy.http.Request('https://news.ycombinator.com/' +
                            item[1], callback=self.parse)
                    yield hn_item
