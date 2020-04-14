# -*- coding: utf-8 -*-
import re

import scrapy
from FPP.items import BaiduBaike
from scrapy import Request


class BaiDuItem(scrapy.Spider):
    name = 'baiduitem'
    # start_url = ''
    custom_settings = {
        'ITEM_PIPELINES': {'FPP.pipelines.BaiduBaikePipeline': 400}
    }
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
    }
    # word_list = ['玉米','大豆']
    word_list = ['棕榈油', '玉米', '玉米淀粉', '乙二醇', '纤维板', '铁矿石', '聚丙烯', '梗米', '焦炭', '焦煤', '胶合板', '黄大豆', '豆油', '豆粨', '苯乙烯',
                 'PVC', 'LLDPE','纸浆']

    def start_requests(self):
        for word in self.word_list:
            url = 'https://baike.baidu.com/item/' + word
            yield Request(url, headers=self.header, meta={'word': word}, callback=self.parse)

    def parse(self, response):

        all_text = response.xpath(
            "//div[@class='main-content']")
        category_id = [i for i in response.xpath(
            "//div[@class='main-content']//div[contains(@class ,'anchor-list')]/a[1]/@name").extract() if
                       not re.match('[a-z]', i)]
        print(category_id)
        category_name = response.xpath(
            "//div[@class='main-content']//div[contains(@class ,'anchor-list')]/a[3]/@name").extract()
        print(category_name)
        for i in range(1, len(category_id) + 1):
            print(response.meta['word'])
            item = BaiduBaike()
            tes = "./*[count(preceding-sibling::div[contains(@class,'anchor-list')])=" + str(
                i) + " and not(contains(@class,'anchor-list'))  and contains(@class,'para')]"
            text = all_text.xpath(tes)
            item['source_name'] = '百度百科'
            item['source_word'] = response.meta['word']
            item['source_url'] = response.url
            item['category_id'] = category_id[i - 1]
            item['category_name'] = category_name[i - 1]
            if len(text) > 1:
                # print(text.xpath("./descendant-or-self::div[@class='para']").xpath('string(.)').extract())

                # con = [all_text.xpath(tes+"["+str(t)+"]").xpath('string(.)').extract()[0] for t in range(2, len(text)+1)]
                con = text.xpath("./descendant-or-self::div[@class='para']").xpath('string(.)').extract()
                con = [''.join(temp.split()) for temp in con if len(temp) > 1]
                item['context'] = '\n'.join([re.sub(r"\[([0-9]*)\]", '', i) for i in con])
                print(item['category_name'], item['context'])
            yield item

    def second_parse(self, response):
        pass
