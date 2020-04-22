# -*- coding: utf-8 -*- 
"""
@Time        : 2020/4/22 19:39 
@Author      : tmooming
@File        : excel2text.py 
@Description : 读取excel到text
"""
import sys
import pandas as pd
import numpy as np

sys.path.append("..")
from utils.rw_excel import read_from_excel

def write2txt(df,txt_path):
    with open(txt_path, 'w', encoding='utf-8') as f:
        for i,v in df.items():
            if v is np.nan:
                continue
            v = v + '\n'
            f.write(v)



if __name__ == "__main__":
    excel_path = "../docs/期货文档/农产品期货.xlsx"
    txt_path = "../docs/期货文档/农产品期货.txt"
    xl = pd.ExcelFile(excel_path)
    sheet_names = xl.sheet_names[1:]
    print(sheet_names)
    df = read_from_excel(excel_path, sheet_names)['语料原文']
    write2txt(df,txt_path)
