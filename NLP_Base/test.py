# -*- coding: utf-8 -*- 
"""
@Time        : 2020/4/15 9:30 
@Author      : tmooming
@File        : test.py 
@Description : TODO
"""
import sys

sys.path.append("../..")

from utils.rw_excel import read_from_excel
import pandas as pd

if __name__ == '__main__':
    excel_path = '../docs/农产品期货.xlsx'
    xl = pd.ExcelFile(excel_path)
    sheet_names = xl.sheet_names[:-1]
    df = read_from_excel(excel_path,sheet_names)
    print(df)
    # f2 = open("../docs/stopwords.txt", "r")
    # lines = f2.readlines()
    #
    # for line in lines:
    #     line = json.loads(line)
    #     result = {'fenci': [], 'cixin': [], 'shiti': [], 'nz_word': []}
    #     items = line['items']
    #     for i in range(len(items)):
    #         result["fenci"].append(items[i]['item'])
    #         result["cixin"].append(items[i]['pos'])  # 词性为nz的应该是需要主要的名词
    #         if items[i]['ne'] != '':
    #             result['shiti'].append(items[i]['item'])
    #         if items[i]['pos'] in ['nz'] and items[i]['item'] not in result['nz_word']:
    #             result['nz_word'].append(items[i]['item'])
    #             # t = i
    #             #
    #             # while items[t]['pos'] != 'v':
    #             #     t = t - 1
    #             # cixin_nz.append(('玉米', items[t]['item'], items[i]['item']))
    #     print(result)
