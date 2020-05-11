# -*- coding: utf-8 -*- 
"""
@Time        : 2020/5/1 10:30 
@Author      : tmooming
@File        : test.py.py 
@Description : TODO
"""
import datetime

import pandas as pd
import pytrends
from pytrends.request import TrendReq
from tkinter import _flatten


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
    start_time = '2010-01-09'
    end_time = '2010-01-24'
    # print(pd.date_range('20100109', '20171030',freq='5M'))
    # print(pd.date_range(start_time.replace('-',''), end_time.replace('-',''), freq='6M'))
    print(time_slice(start_time, end_time))
