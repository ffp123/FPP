# -*- coding: utf-8 -*-
import collections
import json
import sys
import scrapy
import pandas as pd

from FPP.items import BaidubceItem

sys.path.append("../..")
from utils.rw_excel import read_from_excel


class BaidubceSpider(scrapy.Spider):
    name = 'baidubce'
    custom_settings = {
        'ITEM_PIPELINES': {'FPP.pipelines.BaidubcePipline': 401}
    }
    allowed_domains = ['aip.baidubce.com']
    # start_urls = ['http://aip.baidubce.com/']

    header = {"Content-Type": "application/json"}

    def start_requests(self):
        url = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/lexer?charset=UTF-8&access_token=24.bdf4b7fe6991244c8ba606842876605c.2592000.1589506618.282335-19399281'
        # FormRequest 是Scrapy发送POST请求的方法
        # yield scrapy.FormRequest(
        #     url= 'https://aip.baidubce.com/oauth/2.0/token',
        #     formdata={"grant_type": "client_credentials","client_id":"gOM62tcafM4Sbp3lKRt0RTcF","client_secret":"7TCwmtIsTKvoBznPwXSFG0kkjsr0Iqad"},
        #     callback=self.parse_page
        # )
        excel_path = '../../docs/期货文档/金属期货.xlsx'
        class_name = '金属期货'
        xl = pd.ExcelFile(excel_path)
        sheet_names = xl.sheet_names[:-1]
        df = read_from_excel(excel_path, sheet_names)
        for item in df.itertuples():
            word = getattr(item, '语料原文')
            yield scrapy.Request(url, method="POST", headers=self.header, callback=self.parse_page,
                                 body=json.dumps({"text": word}),
                                 meta={'class_name': class_name, 'future_name': getattr(item, 'sheet_name'),
                                       'category_id': getattr(item, 'index'), 'category_name': getattr(item, '相关因素')})

    def parse_page(self, response):
        item = BaidubceItem()
        item['class_name'] = response.meta['class_name']
        item['future_name'] = response.meta['future_name']
        item['category_id'] = response.meta['category_id']
        item['category_name'] = response.meta['category_name']
        item['context'] = json.loads(response.text)['text']
        item['fenci'], item['cixin'], item['shiti'], item['nz_word'], item['count_word'] = [], [], [], [], []
        res = json.loads(response.text)['items']
        for i in range(len(res)):
            item["fenci"].append(res[i]['item'])
            if res[i]['pos'] == '':
                item["cixin"].append(res[i]['ne'])
            item["cixin"].append(res[i]['pos'])  # 词性为nz的应该是需要主要的名词
            if res[i]['ne'] != '':
                item['shiti'].append(res[i]['item'])
            if res[i]['pos'] in ['nz'] and res[i]['item'] not in item['nz_word']:
                item['nz_word'].append(res[i]['item'])
        item['count_word'] = json.dumps(collections.Counter(item['fenci']),ensure_ascii=False)
        item['fenci'] = '\t'.join(item['fenci'])
        item['cixin'] = '\t'.join(item['cixin'])
        item['shiti'] = '\t'.join(item['shiti'])
        item['nz_word'] = '\t'.join(item['nz_word'])

        # t = i
        #
        # while items[t]['pos'] != 'v':
        #     t = t - 1
        # cixin_nz.append(('玉米', items[t]['item'], items[i]['item']))
        print(item)
        yield item
