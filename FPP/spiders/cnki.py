# -*- coding: utf-8 -*-
"""
@Time        : 2020/5/06 10:55
@Author      : tmooming
@File        : cnki.py
@Description : 知网论文爬取
"""
from scrapy_splash import SplashRequest
from FPP.spiders import *

class CnkiSpider(scrapy.Spider):
    name = 'cnki'
    allowed_domains = ['new.gb.oversea.cnki.net']
    start_urls = ['http://new.gb.oversea.cnki.net/']

    words = ['A novel secure data transmission scheme in industrial internet of things']
    def start_requests(self):
        pass
    def parse(self, response):
        pass
