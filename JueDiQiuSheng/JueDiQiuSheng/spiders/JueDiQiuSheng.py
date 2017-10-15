from scrapy import Selector
from scrapy.spiders import Spider
from selenium import webdriver

from JueDiQiuSheng.items import JuediqiushengItem


class JueDiQiuSheng(Spider):
    name = "JueDiQiuSheng"
    start_urls = [
        "http://www.gamersky.com/z/playbattlegrounds/",
    ]

    def __init__(self):
        super(JueDiQiuSheng, self).__init__()

    def parse(self, response):
        print(response.body.decode('utf-8'))

        # from Consumers12315.items import Consumers12315Item
        # item = Consumers12315Item()

        item = JuediqiushengItem()

        item['id'] = '0023133333'
        item['jid'] = '99999'
        item['name'] = 'Hello'
        item['url'] = "http://www.baidu.com"

        yield item
