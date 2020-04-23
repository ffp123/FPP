# -*- coding: utf-8 -*- 
"""
@Time        : 2020/4/15 9:30 
@Author      : tmooming
@File        : test.py 
@Description : TODO
"""
import sys

sys.path.append("..")

from utils.rw_excel import read_from_excel
import pandas as pd

if __name__ == '__main__':
    excel_path = '../docs/期货文档/scrapy_items.csv'
    # xl = pd.ExcelFile(excel_path)
    # sheet_names = xl.sheet_names[:-1]
    # print(sheet_names)
    df = pd.read_csv(excel_path)
    print(df['context'])
    with open('../docs/期货文档/scrapy_items.txt', 'w', encoding='utf-8') as f:
        for ele in df['context']:
            ele = ele + '\n'
            f.write(ele)
        f.close()
