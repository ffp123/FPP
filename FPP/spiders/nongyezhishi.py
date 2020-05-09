# -*- coding: utf-8 -*-
"""
@Time        : 2020/4/20 17:47
@Author      : tmooming
@File        : nongyehishi.py
@Description : 农业知识网站信息爬取
"""
from scrapy_splash import SplashRequest
from FPP.spiders import *


class NongyezhishiSpider(scrapy.Spider):
    name = 'nongyezhishi'
    allowed_domains = ['nongyezhishi.com']
    # start_urls = ['http://nongyezhishi.com/']

    # custom_settings = {
    #     'ITEM_PIPELINES': {'FPP.pipelines.BaiduBaikePipeline': 400}
    # }

    header = {

        'User-Agent': USER_AGENT,

    }
    cookies = {
        'PHPSESSID': 'bo4641ngcf6ulhcpks3aj2p92r',
        'security_session_verify': '860aebcf51bf24cb64a00bb2509920a1',
        'srcurl': '68747470733a2f2f7777772e6e6f6e6779657a68697368692e636f6d2f6a697368752f7a686f6e677a68692f3238373730372e68746d6c',
        'security_session_mid_verify ': ' a8ba4acb94eb7254c50affe811716a38'
    }
    word_list = ['玉米']

    def start_requests(self):
        # -----------------从搜索页开始爬取--------------------------#
        for word in self.word_list:
            url = 'http://zhannei.baidu.com/cse/search?q=' + word + '&p=0&s=7390061894137036671&nsid='
            yield scrapy.FormRequest(url, method='GET', headers=self.header, cookies=self.cookies, dont_filter=True,
                                     meta={'word': word}, callback=self.parse)

    def parse(self, response):
        all_detail_url = response.xpath("//div[contains(@class,'result')]//a/@href").extract()
        for detail_url in all_detail_url:
            yield SplashRequest(url=detail_url, method='POST', callback=self.parse_detail, args={'wait': 1.5})

    def parse_detail(self, response):
        title = response.xpath("//main//h1[contains(@class,'detail-title')]/text()").extract()
        post_time = response.xpath("//div[contains(@class,'info')]//time/text()").extract()
        tags = response.xpath("//div[contains(@class,'info')]//ul[contains(@class,'tags')]/li/a/text()").extract()
