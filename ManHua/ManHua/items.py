# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class ManHuaItem(scrapy.Item):
    # define the fields for your item here like:
    mid2 = Field()
    name = Field()
    picUrl = Field()
    newPageName = Field()
    mhUrl = Field()
    mhNewUrl = Field()
    pass
