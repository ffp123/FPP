import sys

from Future_Price.config import FUTURES

sys.path.append("..")
from Future_Price import *


# from get_date import startTime, endTime, future

class ReadMat(object):
    def __init__(self, mat_path, array_name):
        self.mat_path = mat_path
        self.array_name = self.walk(array_name)
        self.data = self._get_array()

    def _get_array(self):
        data = scio.loadmat(self.mat_path)
        arrays = {}
        for name in self.array_name:
            k = [i for i in name]
            s = "data['" + "']['".join(k) + "']"
            arrays['-'.join(k)] = eval(s).flatten()[0]
            # yield eval(s).flatten()[0]
        return arrays

    def walk(self, dicts):
        for key, value in dicts.items():
            if isinstance(value, dict):
                for tup in self.walk(value):
                    yield (key,) + tup
            else:
                if isinstance(value, list):
                    for l in value:
                        yield key, l


class Data(object):
    def __init__(self, mat_path, google_path, array_name):
        self.mat_data = self._get_mat_data(mat_path,array_name)
        self.google_data = self._get_google_data(google_path)

    def _get_mat_data(self,mat_path,array_name):
        mat_data = ReadMat(mat_path=mat_path, array_name=array_name).data
        date = pd.DataFrame(mat_data['StockMat-dtes'].flatten(), columns=['date'])
        date['date'] = date['date'].astype('str')
        mat_data['date'] = pd.to_datetime(date['date'],format="%Y-%m-%d")
        mat_data.pop('StockMat-dtes')
        mat_data['date'] = pd.DataFrame(mat_data['date'], columns=['date'])
        mat_data['StockMat-rets'] = pd.DataFrame(mat_data['StockMat-rets'], columns=FUTURES)
        mat_data['StockMat-settle'] = pd.DataFrame(mat_data['StockMat-settle'], columns=FUTURES)
        mat_data['StockMat-rets']['date'] = mat_data['date']['date']
        mat_data['StockMat-settle']['date'] = mat_data['date']['date']
        mat_data['StockMat-rets'] = mat_data['StockMat-rets'].set_index('date')
        mat_data['StockMat-settle'] = mat_data['StockMat-settle'].set_index('date')

        return mat_data
    def _get_google_data(self,google_path):
        googleData = pd.read_csv(google_path)
        googleData.drop(['Libyan crisis'], axis=1, inplace=True)
        googleData['date'] = pd.to_datetime(googleData['date'])
        googleData = pd.merge(googleData,  self.mat_data['date'] , on='date')
        googleData = googleData.set_index('date')
        return googleData





# '''
# 可实验的时间区间:'2010-01-11':'2020-05-08'
# 实验准备
# '''
# Future = future
# beginTime = startTime
# endTime = endTime
#
# '''
# 读取期货产品数据
# '''
# datafile = 'model/FuturesDataCon.mat'
# data = scio.loadmat(datafile)
# # print(data['StockMat']['dtes'][0][0])
# date_0 = data['StockMat']['dtes'][0][0]
#
# '''
# 读取关键字搜索量csv
# '''
# path = '../docs/google_trends/google_indexs.csv'
# # words = [] #word是一个二维list，代表所有关键字的搜索量
# googleData = pd.read_csv(path)
# # print(googleData.isna().sum()) #只有Libyan crisis 列有392个nan值，去掉这一列
# # 删除libyan crisis列
# googleData.drop(['Libyan crisis'], axis=1, inplace=True)
# # 将googledate的时间列转成datetime时间列
# googleData['date'] = pd.to_datetime(googleData['date'])
#
# '''
#
# 处理收益率数据的日期格式
# '''
# # 当前date的格式为20200508,转换为标准日期格式
# date = []
# for word in date_0:
#     # word = word.tolist() word是数值 而不是字符串str
#     # print(type(word))
#     Newword = '{}-{}-{}'.format(int(word / 10000), int((word % 10000) / 100), int((word % 100)))
#     date.append(Newword)
#
# # 去除googleData中的周六日、节假日的行，与收益率数据的日期对齐。
# FutureDate = pd.DataFrame(date, columns=['date'])
# FutureDate['date'] = pd.to_datetime(FutureDate['date'])
# # 期货日期列为单独的列，google搜索列为所有数据的列，直接对二者做merge
# googleData_1 = pd.merge(googleData, FutureDate, on='date')
# # print(googleData_1)
#
# '''
# 处理期货收益率数据,没有用到现货价格
# '''
# # 将期货品种收益率数据读出，转成数据帧格式
# rets = data['StockMat']['rets'][0][0]
# retsData = pd.DataFrame(rets, columns=['AL', 'CU', 'RU', 'A', 'WT', 'M', 'WS', 'CF', 'FU', 'C',
#                                        'B', 'SR', 'Y', 'TA', 'ZN', 'RO', 'L', 'P', 'AU', 'RB', 'WR', 'ER', 'V', 'IF',
#                                        'PB', 'J', 'ME', 'PM', 'AG', 'OI',
#                                        'RI', 'WH', 'FG', 'RM', 'RS', 'JM', 'TF', 'TC', 'BU', 'I', 'JD', 'JR', 'BB',
#                                        'FB', 'PP', 'HC', 'MA', 'LR', 'SF',
#                                        'SM', 'CS', 'T', 'NI', 'SN', 'IC', 'IH', 'ZC', 'CY', 'AP', 'SC', 'TS', 'SP',
#                                        'EG', 'CJ', 'UR', 'NR', 'RR',
#                                        'SS', 'EB', 'SA', 'PG'])
#
# # 将期货的价格数据读出，转成数据帧
# price = data['StockMat']['settle'][0][0]
# priceData = pd.DataFrame(price, columns=['AL', 'CU', 'RU', 'A', 'WT', 'M', 'WS', 'CF', 'FU', 'C',
#                                          'B', 'SR', 'Y', 'TA', 'ZN', 'RO', 'L', 'P', 'AU', 'RB', 'WR', 'ER', 'V', 'IF',
#                                          'PB', 'J', 'ME', 'PM', 'AG', 'OI',
#                                          'RI', 'WH', 'FG', 'RM', 'RS', 'JM', 'TF', 'TC', 'BU', 'I', 'JD', 'JR', 'BB',
#                                          'FB', 'PP', 'HC', 'MA', 'LR', 'SF',
#                                          'SM', 'CS', 'T', 'NI', 'SN', 'IC', 'IH', 'ZC', 'CY', 'AP', 'SC', 'TS', 'SP',
#                                          'EG', 'CJ', 'UR', 'NR', 'RR',
#                                          'SS', 'EB', 'SA', 'PG'])
#
# '''
# 处理google数据.
# '''
# googleData_1 = googleData_1.set_index('date')
# googleData_1 = googleData_1.loc[beginTime:endTime]
#
# '''
# 处理期货数据.
# '''
# # 处理日期列为单独的一个列
# # print(FutureDate)
#
# # 添加日期的完整数据retsData
# retsData['date'] = FutureDate  # 为restData增加一列时间列
# priceData['date'] = FutureDate
#
# # 为retsData设置日期类为索引列
# retsData = retsData.set_index('date')
# priceData = priceData.set_index('date')
# # 选取期货品种
# futures = retsData[Future]
# futuresprice = priceData[Future]
# # 选取时间区间
# futureData = futures.loc[beginTime:endTime]
# futurePriceData = futuresprice.loc[beginTime:endTime]
# # print(futureData)
