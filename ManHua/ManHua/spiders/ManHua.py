import json
from urllib.parse import urlparse

import scrapy
from scrapy import Selector
from scrapy.spiders import Spider


class ManHua(Spider):
    name = "ManHua"
    start_urls = [
        "https://www.tohomh123.com/f-1------updatetime--1.html",
        # "https://www.tohomh123.com",
        # "http://www.gamersky.com/z/playbattlegrounds/",
    ]

    def __init__(self):
        super(ManHua, self).__init__()

    def make_requests_from_url(self, url):
        self.logger.debug('Try first time')
        return scrapy.Request(url=url, meta={'download_timeout': 10}, callback=self.parse, dont_filter=False)

    def start_requests(self):
        # for i in range(1, 377):
        ipListPath = "/Users/WangQing/PycharmProjects/ScrapyPro/ProxyPro/ipList.txt"
        f = open(ipListPath)
        data = f.read()
        text = json.loads(data)

        for i in range(1, 20):
            ipIndex = text[i % len(text)]

            scheme = ipIndex["type"]
            domain = ipIndex["url"]

            url1 = domain
            print(url1)
            proxy = url1

            # headers = {'Host': 'tohomh123.com',
            #            'Connection': 'keep-alive',
            #            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
            #            'Referer': 'http://www.tohomh123.com/'}

            print(i)
            url = "https://www.tohomh123.com/f-1------updatetime--" + str(i) + ".html"
            # url = "http://httpbin.org/get"
            print(url)
            yield scrapy.Request(url=url, meta={'download_timeout': 10, 'proxy': proxy}, callback=self.parse)

    def parse(self, response):
        content = response.body.decode("utf-8")
        # print(content)

        result = urlparse(response.url)
        domain = result[0] + "://" + result[1]
        print(domain)

        selector = Selector(text=content)

        itemSelector = selector.css("div.mh-item")

        for item in itemSelector:
            pic = getPic(item)
            title = getTitle(item)
            newPageName = getNewPageName(item)

            mhPath = getMHUrl(item)
            mid2 = mhPath.replace("/", "")
            mhUrl = domain + mhPath
            mhNewUrl = domain + getMHNewUrl(item)

            print("\npic->" + pic +
                  "\ntitle->" + title +
                  "\nmid2->" + mid2 +
                  "\nnewPageName->" + newPageName +
                  "\nmhUrl->" + mhUrl +
                  "\nmhNewUrl->" + mhNewUrl +
                  "\n"
                  )
            yield insertData2DB(mid2, title, pic, newPageName, mhUrl, mhNewUrl)


# 插入数据到数据库中
def insertData2DB(mid2, name, picUrl, newPageName, mhUrl, mhNewUrl):
    from ManHua.items import ManHuaItem
    item = ManHuaItem()
    item['mid2'] = mid2
    item['name'] = name
    item['picUrl'] = picUrl
    item['newPageName'] = newPageName
    item['mhUrl'] = mhUrl
    item['mhNewUrl'] = mhNewUrl
    return item


def getPic(selector):
    # 获取图片
    picList = selector.css("a").css("p::attr('style')").extract()
    for pic in picList:
        pic = pic.replace("background-image: url(", "")
        pic = pic.replace(")", "")

        # print("pic: " + pic)
        return pic


def getNewPageName(selector):
    # 获取最新一集
    newList = selector.css("p").css("a::text").extract()
    for new in newList:
        # print("最新章节是: " + new)
        return new


def getTitle(selector):
    # 获取标题
    titleList = selector.css("h2").css("a").css("a::attr('title')").extract()
    for title in titleList:
        # print("title: " + title)
        return title


def getMHUrl(selector):
    # 获取漫画的当前 URL
    mhUrlList = selector.css("a::attr('href')").extract()
    for mhUrl in mhUrlList:
        # print("mhUrl: " + mhUrl)
        return mhUrl


def getMHNewUrl(selector):
    # 获取漫画的最新章节 URL
    mhNewUrlList = selector.css("div.mh-item-detali").css("p.chapter").css("a::attr('href')").extract()
    for mhNewUrl in mhNewUrlList:
        # print("mhNewUrl: " + mhNewUrl)
        return mhNewUrl
