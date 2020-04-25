# -*- coding: utf-8 -*- 
"""
@Time        : 2020/4/15 9:30 
@Author      : tmooming
@File        : test.py 
@Description : TODO
"""
import ast
import json
import sys

import numpy as np

sys.path.append("..")

from utils.rw_excel import read_from_excel
import pandas as pd

if __name__ == '__main__':
    excel_path = ['../docs/期货文档/农产品期货.xlsx','../docs/期货文档/能源期货.xlsx','../docs/期货文档/金属期货.xlsx']
    df = None
    # df1 = read_from_excel(excel_path[0],pd.ExcelFile(excel_path[0]).sheet_names[1:])
    for path in excel_path:
        xl = pd.ExcelFile(path)
        sheet_names = xl.sheet_names[1:]
        print(sheet_names)
        df = pd.concat([df, read_from_excel(path,sheet_names)], ignore_index=True)
    # print(df['context'])
    stopwords = [line.strip() for line in
                 open('../docs/stopwords/baidu_stopwords.txt', encoding='utf-8').readlines()]
    with open('../docs/分词结果/data.txt', 'w', encoding='utf-8') as f:
        for ele in df['分词结果']:
            if ele is np.nan:
                continue
            ele = ' '.join([e for e in ast.literal_eval(ele) if e not in stopwords]) + '\n'
            f.write(ele)
        f.close()
