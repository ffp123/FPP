# -*- coding: utf-8 -*-
import re

import scrapy
from FPP.items import BaiduBaike
from scrapy import Request


class BaiDuItem(scrapy.Spider):
    name = 'baiduitem'
    # start_url = ''

    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
    }

    def start_requests(self):
        url = 'https://baike.baidu.com/item/玉米/18401'
        yield Request(url, headers=self.header)

    def parse(self, response):
        infos = []
        items = []
        item = BaiduBaike()
        all_text = response.xpath(
            "//div[@class='main-content']/div[contains(@class, 'para-title') or contains(@class ,'para')]")
        item['title'] = '玉米'
        para = ''
        # 将数据按照标题存入item
        for text in all_text:
            # 能否筛除掉不必要的标签信息，如：<a>编辑</a>、[12]等
            # if '编辑' in text.xpath('string(.)').extract()[0]:
            #     print(text.xpath('string(.)').extract()[0])
            #     continue
            symbols = r"[\s]\[([0-9]*)\]"
            temp = text.xpath('string(.)').extract()[0]
            temp = re.sub(symbols,'\n',temp)
            temp = '\n'.join([i.replace('编辑','') if i.startswith('编辑') else i for i in temp.split('\n') if len(i)>1])
            para = para + temp
        item['context'] = para
        # for para in paras:
        #     # print(type(para))
        #     # print(para)
        #     info = para.xpath('string(.)').extract()[0]
        #     infos.append(info)
        #     print('---------------------')
        #     print(info)
        #     print('------------------------')
        # print(infos)

        yield item

    def second_parse(self, response):
        pass
