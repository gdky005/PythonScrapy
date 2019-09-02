from scrapy import Selector
from scrapy.spiders import Spider

from Utils import getHashCode

from NovelPro.items import NovelproItem


class NovelPro(Spider):
    name = "NovelPro"
    start_urls = [
        "https://m.liyuxiang.net/gushi/duanpianxiaoshuo.html",
    ]

    def __init__(self):
        super(NovelPro, self).__init__()

    def parse(self, response):
        content = response.body.decode('utf-8')
        # print(content)

        selector = Selector(text=content)
        chapterNameExtract = selector.css("div.box-left").css("ul.article-lists").css("li")

        for chapterName in chapterNameExtract:
            name = chapterName.css("a::text").extract()
            if len(name) > 0:
                name = chapterName.css("a::text").extract()[0]
                url = chapterName.css("a::attr(href)").extract()[0]
                pid = getHashCode(name)
                sourceUrl = "https://m.liyuxiang.net" + url
                print("我需要的名称：" + name + ", url=" + url + ", sourceUrl=" + sourceUrl + ", id=" + str(pid))
                yield insertData2DB(pid, url, name, sourceUrl)


# 插入数据到数据库中
def insertData2DB(pid, url, name, sourceUrl):
    item = NovelproItem()
    item['pid'] = pid
    item['url'] = url
    item['name'] = name
    item['sourceUrl'] = sourceUrl
    return item