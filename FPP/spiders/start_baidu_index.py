import sys
import time

import pandas as pd

sys.path.append("../..")
from FPP.spiders.baidu_index.utils import test_cookies
from FPP.spiders.baidu_index import config
from FPP.spiders.baidu_index import BaiduIndex, ExtendedBaiduIndex
from FPP.items import BaiduIndexItem
from FPP.spiders.baidu_index.save_data import BaiduIndexPipline
cookies = 'BAIDUID=7C4422DE481F571C7E041263530CC49A:FG=1; BIDUPSID=7C4422DE481F571C7E041263530CC49A; PSTM=1571639074; MCITY=-315%3A; cflag=13%3A3; bdindexid=sa0sdsq4jeviifm3sbb7n6hdc4; Hm_lvt_d101ea4d2a5c67dab98251f0b5de24dc=1588299798,1588313145,1588989903; BDUSS=FEMGVNVVR2Z0ZvZUhOQTJpYWdqbX5xTWtvdn5GMWVvbjhtcmRoOTBkUVpvZDFlRVFBQUFBJCQAAAAAAAAAAAEAAAB1PMDJsKLLubbZxaPI4gAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABkUtl4ZFLZefk; CHKFORREG=74223646f34140a158db712ecfdb4cee; Hm_lpvt_d101ea4d2a5c67dab98251f0b5de24dc=1588991008; H_PS_PSSID=31351_1461_31169_21092_31253_31423_31464_30823_26350_31164; RT="z=1&dm=baidu.com&si=mgmyibstg1&ss=k9yzk76b&sl=e&tt=z73&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=ntfm&ul=2r0sk"'

if __name__ == "__main__":
    # 测试cookies是否配置正确
    # True为配置成功，False为配置不成功
    print(test_cookies(cookies))

    keywords = ['玉米']

    # 获取城市代码, 将代码传入area可以获取不同城市的指数, 不传则为全国
    # 媒体指数不能分地区获取
    # print(config.PROVINCE_CODE)
    # print(config.CITY_CODE)
    # 获取百度搜索指数(地区为全国)
    baidu_index = BaiduIndex(
        keywords=keywords,
        start_date='2011-01-03',
        end_date=time.strftime('%Y-%m-%d',time.localtime(time.time())),
        cookies=cookies,
        area=0
    )
    baidu_save = BaiduIndexPipline()
    for index in baidu_index.get_index():
          baidu_save.process_item(index)
          print(index)
    baidu_save.close_spider()


    # 获取百度媒体指数
    # news_index = ExtendedBaiduIndex(
    #     keywords=keywords,
    #     start_date='2019-01-01',
    #     end_date='2019-01-10',
    #     cookies=cookies,
    #     kind='news'
    # )
    # for index in baidu_index.get_index():
    #     print(index)
    #
    # # 获取百度咨询指数
    # feed_index = ExtendedBaiduIndex(
    #     keywords=keywords,
    #     start_date='2019-01-01',
    #     end_date='2019-01-10',
    #     cookies=cookies,
    #     kind='feed'
    # )
    # for index in feed_index.get_index():
    #     print(index)
