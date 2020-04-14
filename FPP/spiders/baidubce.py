# -*- coding: utf-8 -*-
import json

import scrapy


class BaidubceSpider(scrapy.Spider):
    name = 'baidubce'

    # allowed_domains = ['aip.baidubce.com']
    # start_urls = ['http://aip.baidubce.com/']

    header = {"Content-Type": "application/json"}

    def start_requests(self):
        # FormRequest 是Scrapy发送POST请求的方法
        # yield scrapy.FormRequest(
        #     url= 'https://aip.baidubce.com/oauth/2.0/token',
        #     formdata={"grant_type": "client_credentials","client_id":"gOM62tcafM4Sbp3lKRt0RTcF","client_secret":"7TCwmtIsTKvoBznPwXSFG0kkjsr0Iqad"},
        #     callback=self.parse_page
        # )
        url = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/lexer?charset=UTF-8&access_token=24.602c37ecda87df8bb4e958667be28699.2592000.1589425107.282335-19399281'
        word = '苗期应加强蚜虫的防治，可选用90%敌百虫可湿性粉剂2000倍液进行喷雾防治；大喇叭口期用50%辛硫磷乳剂300mL/hm2与70%多菌灵可湿性粉剂1125g/hm2混合兑水450kg/hm2，对病虫害进行一次性防治，可以减少玉米生长后期病虫害的危害程度；对玉米抽雄、吐丝期出现的双斑萤叶甲选用4.5%高效氯氰菊酯1000倍液防治；对露雄期出现的玉米螟选用敌百虫1000倍液进行灌心，或辛硫磷颗粒剂22.5-30.0kg/hm2撒入心叶防治。及时预防玉米粗缩病，选用农大108、浚单20等抗病性强的品种；将玉米播种方式由套种改为直播，避开灰飞虱高发期；在玉米苗期多次喷施扑虱灵或氧化乐果等药剂杀灭灰飞虱，切断粗缩病的传播途径；推迟间、定苗的时间，发现粗缩病株及时拔除。灌浆期要注意防治玉米叶斑病、锈病的危害，及时浇水，保护好叶片。'
        yield scrapy.Request(url, method="POST", headers=self.header, callback=self.parse_page,
                             body=json.dumps({"text": word}), )

    def parse_page(self, response):
        print('返回文本',json.loads(response.text))
        items= json.loads(response.text)['items']
        with open("test.txt", "w") as f:
            f.write(response.text)
            # for item in items:
        #     print(item['item'])
        #     print(item['ne'])