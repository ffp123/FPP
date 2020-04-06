# -*- coding: utf-8 -*-
import re

import scrapy
from FPP.items import BaiduBaike
from scrapy import Request


class BaiDuItem(scrapy.Spider):
    name = 'baiduitem'
    # start_url = ''
    custom_settings = {
        'ITEM_PIPELINES':{'FPP.pipelines.BaiduBaikePipeline': 400}
    }
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
    }

    def start_requests(self):
        url = 'https://baike.baidu.com/item/玉米/18401'
        yield Request(url, headers=self.header)

    def parse(self, response):
        all_text = response.xpath(
            "//div[@class='main-content']")
        category_id = [i for i in response.xpath(
            "//div[@class='main-content']//div[contains(@class ,'anchor-list')]/a[1]/@name").extract() if
                       not re.match('[a-z]', i)]
        category_name = response.xpath(
            "//div[@class='main-content']//div[contains(@class ,'anchor-list')]/a[3]/@name").extract()
        for i in range(1, len(category_id) + 1):
            item = BaiduBaike()
            tes = "./div[count(preceding-sibling::div[contains(@class,'anchor-list')])=" + str(
                i) + " and not(contains(@class,'anchor-list'))]"
            text = all_text.xpath(tes)
            item['source_name'] = '百度百科'
            item['source_word'] = '玉米'
            item['source_url'] = 'https://baike.baidu.com/item/玉米/18401'
            item['category_id'] = category_id[i - 1]
            item['category_name'] = category_name[i - 1]
            if len(text) > 1:
                con = [all_text.xpath(tes+"["+str(t)+"]").xpath('string(.)').extract()[0] for t in range(2, len(text)+1)]
                symbols = r"[\s]\[([0-9]*)\]"
                con = [''.join(temp.split()) for temp in con if len(temp)>1]
                item['context'] = '\n'.join([re.sub(r"\[([0-9]*)\]",'',i) for i in con])

            yield item

    def second_parse(self, response):
        pass
