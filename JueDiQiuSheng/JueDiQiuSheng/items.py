# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class JDQSItem(scrapy.Item):
    id = Field()
    jid = Field()
    tjName = Field()
    tjDate = Field()
    tjSourceUrl = Field()
    tjUrl = Field()
    tjPicUrl = Field()
    categoryId = Field()
    pass
