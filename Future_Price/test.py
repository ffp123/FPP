# -*- coding: utf-8 -*- 
"""
@Time        : 2020/5/27 9:46 
@Author      : tmooming
@File        : test.py 
@Description : TODO
"""
import datetime
import sys

sys.path.append("..")
from Future_Price import *
from Future_Price.readmat import *
from Future_Price.config import FUTURES, WORDS

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

def Cfear(futureData,scoreList):
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
    return CFEARlist,wordslist

def result(futures,futuresData,scoreList):
    for future in futures:
        futureData = futuresData[future]
        CFEARlist, wordslist =Cfear(futureData,scoreList)
        yield CFEARlist, wordslist



if __name__ == "__main__":
    L = 30  # L代表回溯时间长度，也是时间窗口的长度，如果以天为单位，就是过去L天的搜索量数据和return数据拿来做回归做计算CFEAR因子。
    CFEARLength = 3  # 想要计算CFEAR的长度,就是想要算多少天每天的CFEAR因子值，如果以天为单位就是CFEARLength个天的CFEAR因子值。后面使用 时间长度-时间窗口 来代替它

    mat_path = "model/FuturesDataCon.mat"
    array_name = {'StockMat': ['dtes', 'rets', "settle"]}
    google_path = '../docs/google_trends/google_indexs.csv'
    start_time = '2011-01-01'
    end_time = '2011-05-01'
    futures = ['CU']
    data = Data(mat_path, google_path, array_name)
    mat_data, google_data = data.mat_data, data.google_data
    futuresData = mat_data['StockMat-rets'].loc[start_time:end_time]
    googleData = google_data.loc[start_time:end_time]
    futuresPriceData = mat_data['StockMat-settle'].loc[start_time:end_time]
    scoreList = google_standard(googleData)
    r = futuresData['CU']  # r为收益率
    futurePriceData = futuresPriceData['CU']
    for cfear,words in result(futures,futuresData,scoreList):
        print(cfear,words)
        pricePlot = futurePriceData[L:]  # 作图用的收益率，时间上和搜索量数据对齐
        X = range(len(cfear))
        plt.figure()
        plt.subplot(2, 1, 1)
        plt.bar(X, cfear, label='CFEAR')
        plt.subplot(2, 1, 2)
        plt.plot(X, pricePlot, c='r', label='priceValue')
        plt.legend()
        plt.show()
    # print(len(CFEARlist))
    # print(len(returnPlot))
