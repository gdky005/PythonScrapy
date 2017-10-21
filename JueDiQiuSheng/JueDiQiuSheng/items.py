# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class JDQSDCategory(scrapy.Item):
    id = Field()
    tjName = Field()
    tjUrl = Field()
    tjCollection = Field()
    pass
