# -*- coding: utf-8 -*-
"""
@Time        : 2020/5/01 10:25
@Author      : tmooming
@File        : baiduindex.py
@Description : 获取百度指数
"""
import datetime

import requests
from FPP.items import BaiduIndexItem
from FPP.settings import USER_AGENT
from FPP.spiders import *


class BaiduindexSpider(scrapy.Spider):
    name = 'baiduindex'
    allowed_domains = ['index.baidu.com']
    start_urls = ['http://index.baidu.com/']
    word_url = 'http://index.baidu.com/api/SearchApi/thumbnail?area=0&word={}'
    custom_settings = {
        'ITEM_PIPELINES': {'FPP.pipelines.BaiduIndexPipline': 402}
    }
    COOKIES = {
        "CHKFORREG": "74223646f34140a158db712ecfdb4cee",
        "BAIDUID": "7C4422DE481F571C7E041263530CC49A:FG=1",
        "BIDUPSID": "7C4422DE481F571C7E041263530CC49A",
        "PSTM": 1571639074,
        "MCITY": "-315%3A",
        "BDUSS": "1A5MktCSnRQeExmRjAzWE9vVU56QXlVd29McmVqcUFaa05pVUlGYzVDSFZyc1JlRVFBQUFBJCQAAAAAAAAAAAEAAAB1PMDJsKLLubbZxaPI4gAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANUhnV7VIZ1eb",
        "ZD_ENTRY": "empty",
        "H_PS_PSSID": "31351_1461_31169_21092_31253_31423_31341_31464_30823_26350_31164_31473",
        "BDRCVFR[feWj1Vr5u3D]": "I67x6TjHwwYf0",
        "delPer": 0,
        "PSINO": 3,
        "Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc": 1588299798,
        "bdindexid": "32rk4ts1k7ibl1nor068lv17o0",
        "Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc": 1588300131,
        "RT": "z=1&dm=baidu.com&si=9nnqsci8esv&ss=k9nkoukr&sl=6&tt=aja&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf"
    }
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate,br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep - alive',
        'Cookie': 'BAIDUID=7C4422DE481F571C7E041263530CC49A:FG=1; BIDUPSID=7C4422DE481F571C7E041263530CC49A; PSTM=1571639074; MCITY=-315%3A; BDUSS=1A5MktCSnRQeExmRjAzWE9vVU56QXlVd29McmVqcUFaa05pVUlGYzVDSFZyc1JlRVFBQUFBJCQAAAAAAAAAAAEAAAB1PMDJsKLLubbZxaPI4gAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANUhnV7VIZ1eb; ZD_ENTRY=empty; H_PS_PSSID=31351_1461_31169_21092_31253_31423_31341_31464_30823_26350_31164_31473; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; delPer=0; PSINO=3; Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc=1588299798; bdindexid=32rk4ts1k7ibl1nor068lv17o0; Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc=1588300131; RT="z=1&dm=baidu.com&si=9nnqsci8esv&ss=k9nkoukr&sl=6&tt=aja&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf"',
        'DNT': '1',
        'Host': 'index.baidu.com',
        'Pragma': 'no-cache',
        # 'Proxy-Connection': 'keep-alive',
        'Referer': 'https://index.baidu.com/v2/main/index.html',
        'User-Agent': USER_AGENT,
        'X-Requested-With': 'XMLHttpRequest',
    }

    COUNTRY = {'全国': 0}

    def start_requests(self):
        start_date = '2011-01-03'
        end_date = '2020-05-03'
        country = '全国'
        area = self.COUNTRY[country]
        for word in ['玉米']:
            url = f'http://index.baidu.com/api/SearchApi/index?word={word}&area={area}&startDate={start_date}&endDate={end_date}'
            yield scrapy.FormRequest(url, method="GET", cookies=self.COOKIES, headers=self.headers,
                                     meta={'area': country, 'start_date': start_date, 'end_date': end_date},
                                     callback=self.parse)

    def decrypt(self, keys, encrypt_data):
        w_data = {}
        for index in range(len(keys) // 2):
            w_data[keys[index]] = keys[len(keys) // 2 + index]

        decrypt_data = ''
        for i in range(len(encrypt_data)):
            decrypt_data += w_data[encrypt_data[i]]
        return decrypt_data

    def parse(self, response):
        item = BaiduIndexItem()
        data = json.loads(response.text)['data']
        generalRatio = data['generalRatio'][0]
        uniqid = data['uniqid']

        userIndexes = data['userIndexes'][0]
        item['search_word'] = userIndexes['word']
        item['area'] = response.meta['area']
        item['start_date'] = response.meta['start_date']
        item['end_date'] = response.meta['end_date']
        item['time_type'] = userIndexes['type']

        # 获取解码
        uniqid_url = 'https://index.baidu.com/Interface/api/ptbk?uniqid={}'.format(uniqid)
        resp = requests.get(uniqid_url, headers=self.headers)
        key_data = json.loads(resp.text)['data']
        item['all_data'] = self.decrypt(key_data, userIndexes['all']['data']).split(',')
        item['pc_data'] = self.decrypt(key_data, userIndexes['pc']['data']).split(',')
        item['wise_data'] = self.decrypt(key_data, userIndexes['wise']['data']).split(',')

        # df = pd.DataFrame(
        #     columns=['index_time', 'time_type', 'area', 'search_word', 'all_data', 'pc_data', 'wise_data'])
        # for i in range(len(item['all_data'])):
        #     start_date = datetime.datetime.strptime(item['start_date'], '%Y-%m-%d')
        #     delta = datetime.timedelta(days=7)
        #     df.loc[i,:]={'index_time': start_date + delta * i, 'time_type': item['time_type'], 'area': item['area'],
        #                'search_word': item['search_word'], 'all_data': item['all_data'][i],
        #                'pc_data': item['pc_data'][i], 'wise_data': item['wise_data'][i]}
        # print(df)

        yield item
        # yield baiduindexitem
        # for userIndexe in userIndexes:
        #     if isinstance(userIndexes[userIndexe], dict):
        #         userIndexes[userIndexe]['data'] = self.decrypt(key_data, userIndexes[userIndexe]['data'])
