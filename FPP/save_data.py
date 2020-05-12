# -*- coding: utf-8 -*- 
"""
@Time        : 2020/5/9 13:02 
@Author      : tmooming
@File        : save_data.py 
@Description : 将数据存储
"""
import datetime

import pandas as pd
import psycopg2
import redis
import pandas

try:
    redis_db = redis.Redis(host='127.0.0.1', port=12787, db=1)  # 连接本地redis，db数据库默认连接到0号库，写的是索引值
    postgres_connect = psycopg2.connect(host="127.0.0.1", port='12786', user="postgres", password="postgres",
                                        dbname="FPP")
except:
    redis_db = redis.Redis(host='127.0.0.1', port=6379, db=1)
    postgres_connect = psycopg2.connect(host="127.0.0.1", port='5432', user="postgres", password="postgres",
                                        dbname="FPP")
redis_data_dict = 'item_context'  # key的名字，里面的内容随便写，这里的key相当于字典名称，而不是key值。为了后面引用而建的


class BaiduIndexPipline(object):
    def __init__(self):
        self.connection = postgres_connect
        self.cur = self.connection.cursor()
        redis_db.flushdb()  # 清空当前数据库中的所有 key，为了后面将mysql数据库中的数据全部保存进去
        # print(redis_db)
        if redis_db.hlen(redis_data_dict) == 0:  # 判断redis数据库中的key，若不存在就读取mysql数据并临时保存在redis中
            # sql = 'select context from zhparser.scrapy_items'  # 查询表中的现有数据
            sql = 'select date,keyword,area,kind from baidu_index'
            df = pandas.read_sql(sql, self.connection)  # 读取mysql中的数据
            df['area'] = df['area'].astype('str')
            df['date'] = df['date'].astype('str')
            df['data'] = df['date'].str.cat([df['keyword'], df['area'], df['kind']], sep='_')
            for value in df['data']:
                redis_db.hset(redis_data_dict, value, 0)

    def close_spider(self):
        self.cur.close()
        self.connection.close()

    def process_item(self, item):
        if redis_db.hexists(redis_data_dict, '_'.join(
                [item['date'], item['keyword'], str(item['area']), item['kind']])):  # 比较的是redis_data_dict里面的field
            print('已存在该数据')
        else:
            self.do_insert(item)

    def do_insert(self, item):
        flag = True
        if flag:
            try:
                self.cur.execute(
                    "INSERT INTO baidu_index(date, keyword, area, kind,time_type, all_index, pc_index, wise_index) VALUES(%s,%s,%s,%s,%s,%s,%s,%s); ",
                    (item['date'],item['keyword'],item['area'],item['kind'],item['time_type'],item['all_index'],item['pc_index'],item['wise_index']))
            except Exception as e:
                print("错误", e)

            self.connection.commit()
        # else:
        #     print('测试')

class GoogleTrends(object):
    def __init__(self):
        self.connection = postgres_connect
        self.cur = self.connection.cursor()
        redis_db.flushdb()  # 清空当前数据库中的所有 key，为了后面将mysql数据库中的数据全部保存进去
        # print(redis_db)
        if redis_db.hlen(redis_data_dict) == 0:  # 判断redis数据库中的key，若不存在就读取mysql数据并临时保存在redis中
            # sql = 'select context from zhparser.scrapy_items'  # 查询表中的现有数据
            sql = 'select date,keyword,cat,gprop,geo from google_trends'
            df = pandas.read_sql(sql, self.connection)  # 读取mysql中的数据
            df['date'] = df['date'].astype('str')
            df['data'] = df['date'].str.cat([df['keyword'], df['cat'], df['gprop'],df['geo']], sep='_')
            for value in df['data']:
                redis_db.hset(redis_data_dict, value, 0)

    def close_spider(self):
        self.cur.close()
        self.connection.close()

    def process_item(self, item):
        if redis_db.hexists(redis_data_dict, '_'.join(
                [item['date'], item['keyword'], item['cat'], item['gprop'],item['geo']])):  # 比较的是redis_data_dict里面的field
            print('已存在该数据')
        else:
            self.do_insert(item)

    def do_insert(self, item):
        flag = True
        if flag:
            try:
                self.cur.execute(
                    "INSERT INTO google_trends(date, keyword, cat, gprop,geo, google_index) VALUES(%s,%s,%s,%s,%s,%s); ",
                    (item['date'],item['keyword'],item['cat'],item['gprop'],item['geo'],item[item['keyword']]))
            except Exception as e:
                print("错误", e)

            self.connection.commit()