# -*- coding: utf-8 -*- 
"""
@Time        : 2020/4/19 21:19 
@Author      : tmooming
@File        : NLP_api.py
@Description : 使用NLP_API进行词性标注、分词、实体识别
"""
import sys
import pandas as pd

sys.path.append("../..")
from FPP.utils.rw_excel import write_to_excel, read_from_excel


class Baidu_API(object):
    def __init__(self, excel_path, from_sheet):
        self.yuanwen = self.get_yuanwen(excel_path, from_sheet)


    def get_yuanwen(self, excel_path, from_sheet):
        return pd.read_excel(excel_path, from_sheet).iloc[:, 0:4]


if __name__ == "__main__":
    excel_path = "../data/结果比较.xlsx"
    from_sheet = '原文'
    badiu_api = Baidu_API(excel_path, from_sheet)
    print(badiu_api.yuanwen)
