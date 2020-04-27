# -*- coding: utf-8 -*-
"""
@Time        : 2020/4/20 17:47
@Author      : tmooming
@File        : nongyehishi.py
@Description : 农业知识网站信息爬取
"""
from FPP.spiders import *

class NongyezhishiSpider(scrapy.Spider):
    name = 'nongyezhishi'
    allowed_domains = ['nongyezhishi.com']
    # start_urls = ['http://nongyezhishi.com/']

    # custom_settings = {
    #     'ITEM_PIPELINES': {'FPP.pipelines.BaiduBaikePipeline': 400}
    # }

    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
    }
    # excel_path = '../../docs/期货文档/金属期货.xlsx'
    # xl = pd.ExcelFile(excel_path)
    # word_list = xl.sheet_names[:-1]

    word_list = ['玉米']

    def start_requests(self):
        for word in self.word_list:
            url = 'http://zhannei.baidu.com/cse/search?q='+word+'&p=0&s=7390061894137036671&nsid='
            yield Request(url,meta={'word': word}, callback=self.parse)
    def parse(self, response):
        all_detail_url = response.xpath("//div[contains(@class,'result')]//a/@href").extract()
        for detail_url in all_detail_url:
            yield Request(detail_url,meta={'detail_url':detail_url},headers=self.header,callback=self.parse_detail)
    def parse_detail(self,response):
        print(response.text)
