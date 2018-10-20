# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    content=scrapy.Field()#评论内容
    id=scrapy.Field()#id
    productColor=scrapy.Field()#产品颜色
    productSize=scrapy.Field()#产品size
    referenceName=scrapy.Field()#产品描述
    userClientShow=scrapy.Field()#购买来源
    # price=scrapy.Field()#价格
    # commit=scrapy.Field()#评论数
    # icon=scrapy.Field()#自营信息