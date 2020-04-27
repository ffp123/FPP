# -*- coding: utf-8 -*- 
"""
@Time        : 2020/4/15 9:30 
@Author      : tmooming
@File        : test.py 
@Description : 测试
"""
import sys

sys.path.append("..")
from NLP_Base import *

if __name__ == '__main__':
    # excel_path = ['../docs/期货文档/农产品期货.xlsx', '../docs/期货文档/能源期货.xlsx', '../docs/期货文档/金属期货.xlsx']
    # df = None
    # # df1 = read_from_excel(excel_path[0],pd.ExcelFile(excel_path[0]).sheet_names[1:])
    # for path in excel_path:
    #     xl = pd.ExcelFile(path)
    #     sheet_names = xl.sheet_names[1:]
    #     print(sheet_names)
    #     df = pd.concat([df, read_from_excel(path, sheet_names)], ignore_index=True)
    # print(df['context'])
    # stopwords = [line.strip() for line in
    #              open('../docs/stopwords/baidu_stopwords.txt', encoding='utf-8').readlines()]
    # with open('../docs/分词结果/data.txt', 'w', encoding='utf-8') as f:
    #     for ele in df['分词结果']:
    #         if ele is np.nan:
    #             continue
    #         ele = ' '.join([e for e in ast.literal_eval(ele) if e not in stopwords]) + '\n'
    #         f.write(ele)
    #     f.close()

    qihuo = pd.read_excel('../docs/聚类汇总.xlsx', '期货词向量')
    baidu = pd.read_excel('../docs/聚类汇总.xlsx', '百度&金融交集')
    jingrong = pd.read_excel('../docs/聚类汇总.xlsx', '金融词向量')
    result = pd.merge(qihuo['blue'], baidu['blue'], on=['blue'])

    # result = {'red': [word for word in baidu['red']],
    #           'green': [word for word in baidu['green'] if word in jingrong['green']],
    #           'blue': [word for word in baidu['blue'] if word in jingrong['blue']],
    #           'others': [word for word in baidu['red'] if  word in jingrong['red']]}
    write_to_excel(result.drop_duplicates(),'../docs/聚类汇总.xlsx', 'blue')
