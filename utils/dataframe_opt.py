# -*- coding: utf-8 -*- 
"""
@Time        : 2020/4/27 16:14 
@Author      : tmooming
@File        : dataframe_opt.py 
@Description : 针对dataframe的部分操作
"""
import sys

sys.path.append("..")
from utils import *
from utils.rw_excel import write_to_excel


def get_intersection_independent(list_name,*df):
    """
    对两个或两个以上dataframe的指定列分别取交集，再拼接列返回结果
    :param list_name: 需要取交集的列
    :param df: 多个数据集
    :return: 返回结果为dict
    """
    result = {}
    for name in list_name:
        _df = df[0]
        for i in range(1,len(df)):
            _df = pd.merge(_df, df[i], on=name)
        result[name] = _df[name].drop_duplicates().values.tolist()
    return result


def dict2dataframe(dicts):
    return pd.DataFrame(dict([(k, pd.Series(v)) for k, v in dicts.items()]))


if __name__ == '__main__':
    qihuo = pd.read_excel('../docs/聚类汇总.xlsx', '三者交集red期货再细分')
    baidu = pd.read_excel('../docs/聚类汇总.xlsx', '三者交集red百度再细分')
    jingrong = pd.read_excel('../docs/聚类汇总.xlsx', '三者交集red金融再细分')
    result = get_intersection_independent( ['red','green','blue'],qihuo, baidu,jingrong)
    write_to_excel(dict2dataframe(result),'../docs/聚类汇总.xlsx', '三者交集red三者交集')
    print(dict2dataframe(result))
