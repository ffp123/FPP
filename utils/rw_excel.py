# -*- coding: utf-8 -*- 
"""
@Time        : 2020/4/15 12:05 
@Author      : tmooming
@File        : rw_excel.py 
@Description : excel的读写操作
"""
from utils import *
from openpyxl import load_workbook

def get_sheet_name(excel_path):
    sheet_names = []
    if isinstance(excel_path,str):
        excel_path = list(excel_path)
    for excel in excel_path:
        xl = pd.ExcelFile(excel)
        sheet_names = xl.sheet_names[1:]
    return sheet_names

def read_from_excel(excelPath, sheet_name):
    if isinstance(sheet_name, str):
        sheet_name = list(sheet_name)
    df = None
    for name in sheet_name:
        _df = pd.read_excel(excelPath, sheet_name=name)
        _df['sheet_name'] = [name]*len(_df)
        _df['index'] = [i for i in range(1,len(_df)+1)]
        if df is None:
            df = _df
        else:
            df = pd.concat([df, _df], ignore_index=True)
    return df


def write_to_excel(df, excelPath, sheet_name='Sheet1'):
    excelWriter = pd.ExcelWriter(excelPath, engine='openpyxl')
    excelWriter.book = load_workbook(excelWriter.path)
    try:
        df.to_excel(excel_writer=excelWriter, sheet_name=sheet_name, index=None)
    except Exception as e:
        print('写入错误：', e)
    finally:
        excelWriter.close()
