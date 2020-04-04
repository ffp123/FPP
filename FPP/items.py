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
    # 一级标题 如：玉米
    title = Field()
    # 二级标题 如：（玉米）种植技术
    # title_h2 = Field()
    # # 三级标题 如：（玉米）（种植技术）选用优良品种
    # title_h3 = Field()
    # 主要内容
    context = Field()
    # 文章中的url字段，暂时不添加
    pass
