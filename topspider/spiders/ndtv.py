# -*- coding: utf-8 -*-
import scrapy


class NdtvSpider(scrapy.Spider):
    name = "ndtv"
    allowed_domains = ["ndtv.com"]
    start_urls = (
        'http://www.ndtv.com/',
    )

    def parse(self, response):
        pass
