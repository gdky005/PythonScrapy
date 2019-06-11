# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class ManHuaItem(scrapy.Item):
    # define the fields for your item here like:
    mid = Field()
    url = Field()
    name = Field()
    pass

# class JuediqiushengItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     id = Field()
#     jid = Field()
#     name = Field()
#     url = Field()
#     picUrl = Field()
#     categoryId = Field()
#     categoryName = Field()
#     pass
