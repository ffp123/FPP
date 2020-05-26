'''
该模块功能就是提取出期货数据里面的时间，转化为标准格式，给输入模块的输入日期函数用

'''

import scipy.io as scio
import pandas as pd
import numpy as np

datafile = 'model/FuturesDataCon.mat'
data = scio.loadmat(datafile)
#print(data['StockMat']['dtes'][0][0])
date_0 = data['StockMat']['dtes'][0][0]

# 当前date的格式为20200508,转换为标准日期格式
date = []
for word in date_0:
    #word = word.tolist() word是数值 而不是字符串str
    #print(type(word))
    Newword = '{}-{}-{}'.format(int(word/10000),int((word%10000)/100),int((word%100)))
    date.append(Newword)

FutureDate = pd.DataFrame(date,columns=['date'])
FutureDate['date'] = pd.to_datetime(FutureDate['date'])
#FutureDate = FutureDate['date'].strftime('%Y-%m-%d')
FutureDate = FutureDate.set_index('date')
date = []
for d in FutureDate.index:
    #print(d)
    date.append(d.strftime('%Y-%m-%d'))
#print(date)
dateBase = date
