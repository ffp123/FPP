# -*- coding: utf-8 -*- 
"""
@Time        : 2020/5/27 9:46 
@Author      : tmooming
@File        : test.py 
@Description : TODO
"""
import sys

sys.path.append("..")
from Future_Price import *


# def walk(dicts):
#     for key, value in dicts.items():
#         if isinstance(value, dict):
#             for tup in walk(value):
#                 yield (key,) + tup
#         else:
#             if isinstance(value, list):
#                 for l in value:
#                     yield key, l

class ReadMat(object):
    def __init__(self, file_path, array_name):
        self.file_path = file_path
        self.array_name = self.walk(array_name)
        pass

    def _get_array(self):
        data = scio.loadmat(self.file_path)
        for name in self.array_name:
            k = [i for i in name]
            s = "data['" + "']['".join(k) + "']"
            print(eval(s).flatten()[0])


    def walk(self, dicts):
        for key, value in dicts.items():
            if isinstance(value, dict):
                for tup in self.walk(value):
                    yield (key,) + tup
            else:
                if isinstance(value, list):
                    for l in value:
                        yield key, l


if __name__ == "__main__":
    file_path = "model/FuturesDataCon.mat"
    array_name = {'StockMat': ['rets', "settle"]}
    readmat = ReadMat(file_path=file_path, array_name=array_name)
    print(readmat._get_array())

    data = scio.loadmat(file_path)

    # print(len(data))
    # print(data.keys())
    # # print( exec('[{}]={}'.format(0,0)))
    # f = ["我", "2", ["3", "2"]]
    # g = [[1, 2], [1, 2]]
    # k = {"1": {"1_2": [2, 4]}, "2": ['1', 2]}
    # for i in walk(k):
    #     print(i,len(i),i[0])
    # print(walk(k))
