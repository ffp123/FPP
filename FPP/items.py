# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html


from scrapy.item import Item, Field


class FPPItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    para = Field()


class BaiduBaike(Item):
    # 搜索来源 如：百度百科
    source_name = Field()
    # 搜索词 如：玉米
    source_word = Field()
    # 搜索url
    source_url = Field()
    # 类别id
    category_id = Field()
    # 类别 如：玉米的形态特征、分布范围等
    category_name = Field()
    # 主要内容
    context = Field()
    pass
