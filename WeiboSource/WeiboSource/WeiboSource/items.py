# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeibosourceItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # id = scrapy.Field()
    # name = scrapy.Field()
    # uid = scrapy.Field()
    # index = scrapy.Field()
    # des = scrapy.Field()
    # img = scrapy.Field()
    # info = scrapy.Field()
    # isVip = scrapy.Field()
    # weiBo = scrapy.Field()
    # zhiHu = scrapy.Field()

    id = scrapy.Field()
    name = scrapy.Field()
    address = scrapy.Field()
    blog_list = scrapy.Field()
    img = scrapy.Field()



    pass
