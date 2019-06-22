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
    name = Field()
    author = Field()
    picUrl = Field()
    state = Field()
    stateId = Field()
    remind = Field()
    time = Field()
    detail = Field()
    category = Field()
    categoryIdList = Field()
    tag = Field()
    url = Field()
    pass
