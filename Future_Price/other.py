# -*- coding: utf-8 -*-
'''
该模块作用：
程序入口模块，展示时直接运行这个模块
引入期货数据futerData和谷歌搜索量数据googleData_1,
将谷歌搜索量数据先做log差 log(t+1)-log(t)，再将其标准化。
得到的标准化数据和
'''
import sys

sys.path.append("..")
from Future_Price import *
from Future_Price.config import FUTURES, WORDS
from Future_Price.readmat import *


def z_score(seq):  # 将序列标准化函数
    seq1 = np.array(seq).reshape(-1, 1)  # 转换为列向量
    scaler = StandardScaler()
    seq1 = scaler.fit_transform(seq1)  # 计算并转化为标准化数据序列
    seq1 = np.array(seq1).reshape(1, -1)  # 转化为行向量
    seq1 = seq1[0]
    # print(seq1)

    return seq1.tolist()


def google_standard(googleData):
    '''
    对每个关键词的谷歌指数做log差，log(t+1) - log(t)
    '''
    Sinterest = []  # Sinterest是一个二维list，包含了每个关键词在整个实验的时间区间内的谷歌指数log
    for word in WORDS:
        Slog = []
        indexData = googleData[word].values
        indexData = np.array(indexData).tolist()
        for w in range(len(indexData) - 1):
            svalues = math.log(indexData[w + 1] + 1) - math.log(indexData[w] + 1)
            Slog.append(svalues)
        Sinterest.append(Slog)
    # Sinterest就是做完log变换后的谷歌指数,接下来做数据标准化
    # z-score数据标准化
    scoreList = []
    for word in Sinterest:
        scoreList.append(z_score(word))
    return scoreList


def Cfear(futureData, scoreList, L):
    CFEARlist = []  # CFEARlist是一个一维list，包含了该期货品种下规定日期每一天的CFEAR因子。
    # 将选择的关键词按天写入dataframe
    wordslist = []
    for i in range(len(futureData) - L):  # 这里的CFEARLength为: 输入的时间长度-回溯长度
        # 对于每一个关键词
        CFEAR = 0
        # 关键词索引
        wordIndex = 0
        # 选择的关键词list
        wordSelectList = []

        for word in scoreList:
            # print(len(word[i:i+L]))
            # print('Futurelen: {}'.format(len(futureData[i:i + L])))
            # print('googlelen: {}'.format(len(word[i:i + L])))
            est = sm.OLS(futureData[i:i + L], word[i:i + L]).fit()  # 需要保证关键词数据的起始时间点和return的起始时间点要相同
            # 后面接判断语句，t值或p值大于或小于阈值，则把参数选择出来，准备求和
            if abs(est.tvalues[0]) > 1.96:
                CFEAR += est.params[0]
                wordSelectList.append(WORDS[wordIndex])
            wordIndex += 1
            # print(wordSelectList)
            # print(wordIndex)
        wordslist.append(wordSelectList)
        # print(wordslist)
        CFEARlist.append(CFEAR)
    return CFEARlist, wordslist


def result(futures, futuresData, futuresPriceData, scoreList, L=20):
    for future in futures:
        futureData = futuresData[future]
        CFEARlist, wordslist = Cfear(futureData, scoreList, L)
        yield CFEARlist, wordslist, futuresPriceData[future][L:], future, futuresData[future][L:]


if __name__ == "__main__":
    # -----------参数---------------#
    L = [20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220,
         240]  # L代表回溯时间长度，也是时间窗口的长度，如果以天为单位，就是过去L天的搜索量数据和return数据拿来做回归做计算CFEAR因子。
    CFEARLength = 3  # 想要计算CFEAR的长度,就是想要算多少天每天的CFEAR因子值，如果以天为单位就是CFEARLength个天的CFEAR因子值。后面使用 时间长度-时间窗口 来代替它
    mat_path = "model/FuturesDataCon.mat"
    array_name = {'StockMat': ['dtes', 'rets', "settle"]}
    google_path = '../docs/google_trends/google_indexs.csv'
    start_time = '2010-01-18'
    end_time = '2020-05-08'
    futures = ['AL', 'CU', 'RU', 'A', 'M', 'CF', 'C', 'B', 'SR', 'Y', 'TA', 'ZN', 'L', 'P', 'AU', 'RB', 'V']

    data = Data(mat_path, google_path, array_name)
    mat_data, google_data = data.mat_data, data.google_data
    futuresData = mat_data['StockMat-rets'].loc[start_time:end_time]
    print(futuresData)
    googleData = google_data.loc[start_time:end_time]
    print(googleData)
    futuresPriceData = mat_data['StockMat-settle'].loc[start_time:end_time]
    scoreList = google_standard(googleData)
    # print(futuresData.isnull().sum())
    # pd.DataFrame(futuresData.isnull().sum()).to_csv('loss.csv')
    # ----------输出-------------#
    for l in L:
        for cfear, words, price, futureName, futureReturen in result(futures, futuresData, futuresPriceData, scoreList,
                                                                     l):
            print(len(cfear), len(words), len(price), futureName)
            data = {'name': futureName, 'CFFEAR': cfear, 'WORDS': words, 'futurePrice': price,
                    'futureReturn': futureReturen, 'windowLength': l}
            pd.DataFrame(data).to_csv('../docs/CFEAR计算结果/' + futureName + '-windowL' + str(l) + '.csv')

        # X = range(len(cfear))
        # plt.figure()
        # plt.subplot(2, 1, 1)
        # plt.bar(X, cfear, label='CFEAR')
        # plt.subplot(2, 1, 2)
        # plt.plot(X, price, c='r', label='priceValue')
        # plt.legend()
        # plt.show()

# '''
# 读取关键词的谷歌搜索数据
# '''
# # print(googleData_1)
# # 关键词搜索量数据的处理： 1先做时间切片，2再用循环读取每个关键词到list列表
#
# '''
# 读取期货价格的return数据
# '''
# # print(CU)
# # 收益率数据的处理，1先做时间切片，2再做品种选择
# r = futureData  # r为收益率
# '''
# 对每个关键词的谷歌指数做log差，log(t+1) - log(t)
# '''
# Sinterest = []  # Sinterest是一个二维list，包含了每个关键词在整个实验的时间区间内的谷歌指数log
# for word in WORDS:
#     Slog = []
#     indexData = googleData_1[word].values
#     indexData = np.array(indexData).tolist()
#     # print(indexData)
#     for w in range(len(indexData) - 1):
#         svalues = math.log(indexData[w + 1] + 1) - math.log(indexData[w] + 1)
#         Slog.append(svalues)
#     Sinterest.append(Slog)
# # Sinterest就是做完log变换后的谷歌指数,接下来做数据标准化
#
# # z-score数据标准化
# scoreList = []
# for word in Sinterest:
#     scoreList.append(z_score(word))
# scoreList为一个二维list，包含了每个关键词的在整个实验时间区间内的标准化后数据。

# 长度得考虑节假日的影响，期货数据在节假日也是没有的
# 2010-01-11 2020-05-11
# 前溯：20-240（步长20）
# 时间平滑：前溯7天取均值作为当天index数据，节假日跳过（不主动做均值操作，只被动参与均值操作）
# 变量、结果入库
'''
线性回归分析t检验，检验关键词对return的影响是否显著
'''
# 这里要注意控制关键词的时间起始点和return收益率的时间起始点需要相同。
# 对于每一个时间窗口
# CFEARlist = []  # CFEARlist是一个一维list，包含了该期货品种下规定日期每一天的CFEAR因子。
#
# # 将选择的关键词按天写入dataframe
# wordslist = []
# for i in range(len(r) - L):  # 这里的CFEARLength为: 输入的时间长度-回溯长度
#     # 对于每一个关键词
#     CFEAR = 0
#     # 关键词索引
#     wordIndex = 0
#     # 选择的关键词list
#     wordSelectList = []
#
#     for word in scoreList:
#         # print(len(word[i:i+L]))
#         est = sm.OLS(r[i:i + L], word[i:i + L]).fit()  # 需要保证关键词数据的起始时间点和return的起始时间点要相同
#         # 后面接判断语句，t值或p值大于或小于阈值，则把参数选择出来，准备求和
#         if abs(est.tvalues[0]) > 1.96:
#             CFEAR += est.params[0]
#             wordSelectList.append(WORDS[wordIndex])
#         wordIndex += 1
#         # print(wordSelectList)
#         # print(wordIndex)
#     wordslist.append(wordSelectList)
#     # print(wordslist)
#     CFEARlist.append(CFEAR)
# print(CFEARlist)
#
# pricePlot = futurePriceData[L:]  # 作图用的收益率，时间上和搜索量数据对齐
# # print(len(CFEARlist))
# # print(len(returnPlot))
# print(wordslist)
#
# X = range(len(CFEARlist))
# plt.figure()
# plt.subplot(2, 1, 1)
# plt.bar(X, CFEARlist, label='CFEAR')
# plt.subplot(2, 1, 2)
# plt.plot(X, pricePlot, c='r', label='priceValue')
# plt.legend()
# plt.show()
