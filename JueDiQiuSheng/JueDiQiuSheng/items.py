# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class JDQSDPicUrlItem(scrapy.Item):
    picId = Field()
    picUrl = Field()
    picTinyUrl = Field()
    picSmallUrl = Field()
    picZKUrl = Field()
    picName = Field()
    picCategoryId_id = Field()
    picCollection = Field()
    pass
