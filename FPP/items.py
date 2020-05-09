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


class BaidubceItem(Item):
    # 类名 如： 农产品期货
    class_name = Field()
    # 期货名称 如： 玉米
    future_name = Field()
    # 类别id
    category_id = Field()
    # 类别 如：玉米的国内外消费情况等
    category_name = Field()
    # 主要内容
    context = Field()
    # 百度分词情况
    fenci = Field()
    # 百度词性标注情况
    cixin = Field()
    # 百度实体识别情况
    shiti = Field()
    # nz名词
    nz_word = Field()
    # 分词词频统计
    count_word = Field()


class BaiduIndexItem(Item):
    # 搜索词 如玉米
    keyword = Field()
    # 搜索范围 如：0代表全国
    area = Field()
    # 时间
    date = Field()
    # 搜索类别：百度搜索指数、百度媒体指数、百度咨询指数
    kind = Field()
    # 数值类型：周为单位或日为单位
    time_type = Field()
    # 总搜索指数：PC+移动端
    all_index = Field()
    # PC端搜索指数
    pc_index = Field()
    # 移动端搜索指数
    wise_index = Field()
