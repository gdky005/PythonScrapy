# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class SubInfoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    id = Field()
    pid = Field()
    name = Field()
    pic = Field()
    url = Field()
    update_time = Field()
    intro = Field()
    capture_pic = Field()

    pass


class SubMovieDownloadInfoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    id = Field()
    pid = Field()
    fj_name = Field()
    fj_number = Field()
    fj_download_url = Field()

    pass


class SubMovieLastestInfoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    id = Field()
    pid = Field()
    fj_number = Field()

    pass
