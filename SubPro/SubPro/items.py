# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class SubproItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = Field()
    jid = Field()
    name = Field()
    url = Field()
    picUrl = Field()
    categoryId = Field()
    categoryName = Field()

    pass
