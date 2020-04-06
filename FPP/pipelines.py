# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import psycopg2


class FPPPipeline(object):
    def process_item(self, item, spider):
        print(item['category_name'])
        return item


class BaiduBaikePipeline(object):
    def open_spider(self, spider):
        hostname = 'localhost'
        username = 'postgres'
        password = '106250'
        database = 'FPP'
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        self.cur = self.connection.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()

    def process_item(self, item, spider):
        self.cur.execute(
            "INSERT INTO scrapy_items(source_name,source_word,source_url,category_id,category_name,context) VALUES(%s,%s,%s,%s,%s,%s); ",
            (item['source_name'], item['source_word'], item['source_url'], item['category_id'], item['category_name'],
             item['context']))
        self.connection.commit()
        return item
