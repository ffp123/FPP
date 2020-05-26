# -*- coding: utf-8 -*- 
"""
@Time        : 2020/5/9 17:17 
@Author      : tmooming
@File        : google_trends.py 
@Description : 谷歌趋势API
"""
import sys
import time

sys.path.append("../..")
import datetime

import pandas as pd
import pytrends
from _tkinter import _flatten
from pytrends.request import TrendReq
from FPP.save_data import GoogleTrends

def time_slice(start_time, end_time):
    mydelay = datetime.timedelta(weeks=28)
    str2time = lambda x: datetime.datetime.strptime(x, '%Y-%m-%d')
    start_time, end_time = str2time(start_time), str2time(end_time)
    time_list = []
    while mydelay + start_time < end_time:
        mid_time = mydelay + start_time
        time_list.append(start_time.strftime('%Y-%m-%d') + ' ' + mid_time.strftime('%Y-%m-%d'))
        start_time = mid_time
    if mydelay + start_time >= end_time:
        time_list.append(start_time.strftime('%Y-%m-%d') + ' ' + end_time.strftime('%Y-%m-%d'))

    return time_list


if __name__ == '__main__':
    # 间隔为半年
    mydelay = datetime.timedelta(weeks=28)
    start_time = '2020-04-09'
    end_time = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    # 定义语言和时区
    pytrends = TrendReq(hl='en-US', tz=360)
    # kw_list：搜索词，cat：类别(默认为0，所有类别)，timeframe：时间范围，gprop：属性（默认为Google网页搜索），geo：地区（默认为全球）
    keywords = list(_flatten([line.strip().split(',') for line in
                              open('../../docs/待爬词汇/hot words.txt', encoding='gbk').readlines()]))
    # keywords = ['corns']
    google_trends = GoogleTrends()
    for keyword in keywords:
        df = None
        for timescale in time_slice(start_time, end_time):
            pytrends.build_payload(kw_list=[keyword], cat=0, timeframe=timescale, gprop='', geo='US')
            _df = pytrends.interest_over_time()
            _df['date'] = _df.index
            _df['date'] = _df['date'].astype('str')
            _df['keyword'] = [keyword]*len(_df)
            _df['cat'] = ['0']*len(_df)
            _df['gprop'] = ['']*len(_df)
            _df['geo'] = ['US']*len(_df)
            # _df = _df.drop(['isPartial'],axis=1)

            df = pd.concat([df, _df], ignore_index=True)
        for index, row in df.iterrows():
            print(row)
            google_trends.process_item(row)
    google_trends.close_spider()
