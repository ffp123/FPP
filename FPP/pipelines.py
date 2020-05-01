# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import datetime

import pandas as pd
import psycopg2
import redis
import pandas
from scrapy.exceptions import DropItem

redis_db = redis.Redis(host='127.0.0.1', port=6379, db=1)  # 连接本地redis，db数据库默认连接到0号库，写的是索引值
redis_data_dict = 'item_context'  # key的名字，里面的内容随便写，这里的key相当于字典名称，而不是key值。为了后面引用而建的
postgres_connect = psycopg2.connect(host="127.0.0.1", user="postgres", password="postgres", dbname="FPP")


class FPPPipeline(object):
    def process_item(self, item, spider):
        print(item['category_name'])
        return item


class BaiduBaikePipeline(object):
    def __init__(self):
        self.connection = postgres_connect
        self.cur = self.connection.cursor()
        redis_db.flushdb()  # 清空当前数据库中的所有 key，为了后面将mysql数据库中的数据全部保存进去
        # print(redis_db)
        if redis_db.hlen(redis_data_dict) == 0:  # 判断redis数据库中的key，若不存在就读取mysql数据并临时保存在redis中
            # sql = 'select context from zhparser.scrapy_items'  # 查询表中的现有数据
            sql = 'select context from scrapy_items'
            df = pandas.read_sql(sql, self.connection)  # 读取mysql中的数据
            # print(df)
            for context in df['context'].values:
                redis_db.hset(redis_data_dict, context, 0)  # 把每个url写入field中，value值随便设，我设置的0  key field value 三者的关系

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()

    def process_item(self, item, spider):

        if redis_db.hexists(redis_data_dict, item['context']):  # 比较的是redis_data_dict里面的field
            raise DropItem("数据库已经存在该条数据: %s" % item)
        else:
            self.do_insert(item)

    def do_insert(self, item):
        flag = True
        if flag:
            try:
                self.cur.execute(
                    "INSERT INTO scrapy_items(source_name,source_word,source_url,category_id,category_name,context) VALUES(%s,%s,%s,%s,%s,%s); ",
                    (item['source_name'], item['source_word'], item['source_url'], item['category_id'],
                     item['category_name'], item['context']))
            except Exception as e:
                print("错误", e)

            self.connection.commit()
        else:
            print('测试')
        return item


class BaidubcePipline(object):
    def __init__(self):
        self.connection = postgres_connect
        self.cur = self.connection.cursor()
        redis_db.flushdb()  # 清空当前数据库中的所有 key，为了后面将mysql数据库中的数据全部保存进去
        # print(redis_db)
        if redis_db.hlen(redis_data_dict) == 0:  # 判断redis数据库中的key，若不存在就读取mysql数据并临时保存在redis中
            # sql = 'select context from zhparser.scrapy_items'  # 查询表中的现有数据
            sql = 'select context from shouce_baidubce'
            df = pandas.read_sql(sql, self.connection)  # 读取mysql中的数据
            # print(df)
            for context in df['context'].values:
                redis_db.hset(redis_data_dict, context, 0)

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()

    def process_item(self, item, spider):
        if redis_db.hexists(redis_data_dict, item['context']):  # 比较的是redis_data_dict里面的field
            raise DropItem("数据库已经存在该条数据: %s" % item)
        else:
            self.do_insert(item)

    def do_insert(self, item):
        flag = True
        if flag:
            try:
                self.cur.execute(
                    "INSERT INTO shouce_baidubce(class_name,future_name,category_id,category_name,context,fenci,cixin,shiti,nz_word,count_word) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s); ",
                    (item['class_name'], item['future_name'], item['category_id'], item['category_name'],
                     item['context'], item['fenci'], item['cixin'], item['shiti'], item['nz_word'], item['count_word']))
            except Exception as e:
                print("错误", e)

            self.connection.commit()
        else:
            print('测试')
        return item


class BaiduIndexPipline(object):
    def __init__(self):
        self.connection = postgres_connect
        self.cur = self.connection.cursor()
        redis_db.flushdb()  # 清空当前数据库中的所有 key，为了后面将mysql数据库中的数据全部保存进去
        # print(redis_db)
        if redis_db.hlen(redis_data_dict) == 0:  # 判断redis数据库中的key，若不存在就读取mysql数据并临时保存在redis中
            # sql = 'select context from zhparser.scrapy_items'  # 查询表中的现有数据
            sql = 'select index_time,time_type,area,search_word from baidu_index'
            df = pandas.read_sql(sql, self.connection)  # 读取mysql中的数据
            df['index_time'] = df['index_time'].astype('str')
            df['data'] = df['index_time'].str.cat([df['time_type'], df['area'], df['search_word']], sep='_')
            for value in df['data']:
                redis_db.hset(redis_data_dict, value, 0)

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()

    def process_item(self, item, spider):
        df = pd.DataFrame(
            columns=['index_time', 'time_type', 'area', 'search_word', 'all_data', 'pc_data', 'wise_data'])
        for i in range(len(item['all_data'])):
            start_date = datetime.datetime.strptime(item['start_date'], '%Y-%m-%d')
            delta = datetime.timedelta(days=7)
            now = start_date + delta * i
            df.loc[i, :] = {'index_time': now, 'time_type': item['time_type'], 'area': item['area'],
                            'search_word': item['search_word'], 'all_data': item['all_data'][i],
                            'pc_data': item['pc_data'][i], 'wise_data': item['wise_data'][i]}
            if redis_db.hexists(redis_data_dict, '_'.join([str(now.date()), item['time_type'], item['area'], item[
                'search_word']])):  # 比较的是redis_data_dict里面的field

                continue

            else:
                self.do_insert(df.loc[i, :])

    def do_insert(self, line):
        flag = True

        if flag:
            try:
                self.cur.execute(
                    "INSERT INTO baidu_index(index_time, time_type, area, search_word, all_data, pc_data, wise_data) VALUES(%s,%s,%s,%s,%s,%s,%s); ",
                    (line[:]))
            except Exception as e:
                print("错误", e)

            self.connection.commit()
        # else:
        #     print('测试')
