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
from scrapy_splash import SplashRequest, SplashJsonResponse
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
        'BAIDUID': '7C4422DE481F571C7E041263530CC49A:FG=1',
        'BIDUPSID': '7C4422DE481F571C7E041263530CC49A',
        'PSTM': '1571639074',
        'MCITY': '-315%3A',
        'cflag': '13%3A3',
        'bdindexid': 'sa0sdsq4jeviifm3sbb7n6hdc4',
        'Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc': '1588299798,1588313145,1588989903',
        'BDUSS': 'FEMGVNVVR2Z0ZvZUhOQTJpYWdqbX5xTWtvdn5GMWVvbjhtcmRoOTBkUVpvZDFlRVFBQUFBJCQAAAAAAAAAAAEAAAB1PMDJsKLLubbZxaPI4gAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABkUtl4ZFLZefk',
        'CHKFORREG': '74223646f34140a158db712ecfdb4cee',
        'Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc': '1588991008',
        'H_PS_PSSID': '31351_1461_31169_21092_31253_31423_31464_30823_26350_31164',
        'RT': "z=1&dm=baidu.com&si=mgmyibstg1&ss=k9yzk76b&sl=e&tt=z73&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=ntfm&ul=2r0sk"
    }
    cookie = 'BAIDUID=7C4422DE481F571C7E041263530CC49A:FG=1; BIDUPSID=7C4422DE481F571C7E041263530CC49A; PSTM=1571639074; MCITY=-315%3A; cflag=13%3A3; bdindexid=sa0sdsq4jeviifm3sbb7n6hdc4; Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc=1588299798,1588313145,1588989903; BDUSS=FEMGVNVVR2Z0ZvZUhOQTJpYWdqbX5xTWtvdn5GMWVvbjhtcmRoOTBkUVpvZDFlRVFBQUFBJCQAAAAAAAAAAAEAAAB1PMDJsKLLubbZxaPI4gAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABkUtl4ZFLZefk; CHKFORREG=74223646f34140a158db712ecfdb4cee; Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc=1588991008; H_PS_PSSID=31351_1461_31169_21092_31253_31423_31464_30823_26350_31164; RT="z=1&dm=baidu.com&si=mgmyibstg1&ss=k9yzk76b&sl=e&tt=z73&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=ntfm&ul=2r0sk"'
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate,br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep - alive',
        'Cookie': 'BDUSS=FEMGVNVVR2Z0ZvZUhOQTJpYWdqbX5xTWtvdn5GMWVvbjhtcmRoOTBkUVpvZDFlRVFBQUFBJCQAAAAAAAAAAAEAAAB1PMDJsKLLubbZxaPI4gAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABkUtl4ZFLZefk',
        'DNT': '1',
        'Host': 'index.baidu.com',
        'Pragma': 'no-cache',
        # 'Proxy-Connection': 'keep-alive',
        'Referer': 'https://index.baidu.com/v2/main/index.html',
        'User-Agent': USER_AGENT,
        'X-Requested-With': 'XMLHttpRequest',
    }

    COUNTRY = {'全国': 0}
    script = '''
            function main(splash)
              local url = splash.args.url
              assert(splash:go(url))
              assert(splash:wait(0.5))
              local entries = splash:history()
              local last_response = entries[#entries].response
              return {
                url = splash:url(),
                headers = last_response.headers,
                http_status = last_response.status,
                cookies = splash:get_cookies(),
                html = splash:html(),
              }
            end
            '''

    def start_requests(self):
        # yield SplashJsonResponse('https://index.baidu.com/v2/index.html#/',callback=self.get_cookie,headers=self.headers,args={'lua_source': self.script})
        # yield scrapy.Request('https://index.baidu.com/v2/index.html#/', callback=self.get_cookie, headers=self.headers,)

        start_date = '2011-01-03'
        end_date = '2020-05-03'
        country = '全国'
        area = self.COUNTRY[country]
        for word in ['玉米']:
            url = f'http://index.baidu.com/api/SearchApi/index?word={word}&area={area}&startDate={start_date}&endDate={end_date}'
            yield scrapy.Request(url, method="GET", cookies=self.COOKIES, headers=self.headers,
                                 meta={'area': country, 'start_date': start_date, 'end_date': end_date},
                                 callback=self.parse)



    # def stringToDict(self):
    #     '''
    #     将从浏览器上Copy来的cookie字符串转化为Scrapy能使用的Dict
    #     :return:
    #     '''
    #     itemDict = {}
    #     items = self.cookie.split(';')
    #     print(items)
    #     for item in items:
    #         key = item.split('=',1)[0].replace(' ', '')
    #         value = item.split('=',1)[1]
    #         itemDict[key] = value
    #     print(itemDict)
    #     return itemDict
    def decrypt(self, keys, encrypt_data):
        w_data = {}
        for index in range(len(keys) // 2):
            w_data[keys[index]] = keys[len(keys) // 2 + index]

        decrypt_data = ''
        for i in range(len(encrypt_data)):
            decrypt_data += w_data[encrypt_data[i]]
        return decrypt_data

    def parse(self, response):
        print(response)
        item = BaiduIndexItem()
        data = json.loads(response.text)['data']
        # generalRatio = data['generalRatio'][0]
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
