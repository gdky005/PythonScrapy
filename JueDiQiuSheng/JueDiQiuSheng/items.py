# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class JDQSContentItem(scrapy.Item):
    id = Field()
    artifactName = Field()
    artifactAuthor = Field()
    artifactContent = Field()
    jid = Field()
    artifactSourceUrl = Field()
    artifactUrl = Field()
    artifactCollection = Field()
    pass



