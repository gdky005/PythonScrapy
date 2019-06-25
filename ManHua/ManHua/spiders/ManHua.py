import json

import requests
import scrapy
from scrapy import Selector
from scrapy.spiders import Spider
import re

from Utils import getHashCode


def getPic(selector):
    # 获取图片
    picList = selector.css("a").css("p::attr('style')").extract()
    for pic in picList:
        pic = pic.replace("background-image: url(", "")
        pic = pic.replace(")", "")

        print("pic: " + pic)
        return pic


def getNewPageName(selector):
    # 获取最新一集
    newList = selector.css("p").css("a::text").extract()
    for new in newList:
        print("最新章节是: " + new)
        return new


def getTitle(selector):
    # 获取标题
    titleList = selector.css("h2").css("a").css("a::attr('title')").extract()
    for title in titleList:
        print("title: " + title)
        return title


class ManHua(Spider):
    name = "ManHua"
    start_urls = [
        "https://www.tohomh123.com/zhegedashutailengao/83.html",
        # "http://127.0.0.1:8081/1-2000/00001_chaojiweixin",
        # "https://www.tohomh123.com/zhegedashutailengao/",
        # "https://www.tohomh123.com/f-1------updatetime--1.html",
        # "https://www.tohomh123.com/f-1-1-----hits--1.html",
        # "https://www.tohomh123.com",
        # "http://www.gamersky.com/z/playbattlegrounds/",
    ]

    def __init__(self):
        super(ManHua, self).__init__()

    # def start_requests(self):
    #
    #     page = 1
    #     pageCount = 2
    #     # pageCount = 2000
    #     urlSource = "http://zkteam.cc/ManHua/jsonMHAllData?page=" + str(page) + "&pageCount=" + str(pageCount)
    #
    #     res = requests.get(urlSource)
    #     resultList = res.json()['result']
    #
    #     i = 0
    #     for data in resultList:
    #         i = i+1
    #
    #         id = data['id']
    #         mid = data['mid']
    #         mid2 = data['mid2']
    #         url = data['mhUrl']
    #         newUrl = data['mhNewUrl']
    #
    #         yield self.make_requests_from_url(newUrl)

    def start_requests(self):
        # for i in range(1, 377):
        # ipListPath = "/Users/WangQing/Desktop/Scrapy/PythonScrapy/ProxyPro/ipList.txt"
        # ipListPath = "/Users/WangQing/PycharmProjects/ScrapyPro/ProxyPro/ipList.txt"
        # ipListPath = "/Users/WangQing/PycharmProjects/ScrapyPro/ProxyPro/ipList_xici.txt"
        ipListPath = "/Users/WangQing/PycharmProjects/ScrapyPro/ProxyPro/new_avilable_ip.txt"
        f = open(ipListPath)
        data = f.read()
        text = json.loads(data)

        page = 6
        # pageCount = 2
        pageCount = 2000
        urlSource = "http://zkteam.cc/ManHua/jsonMHAllData?page=" + str(page) + "&pageCount=" + str(pageCount)

        res = requests.get(urlSource)
        resultList = res.json()['result']

        start = (page - 1) * pageCount
        if start <= 0:
            start = 0
        end = page * pageCount

        if end < 2000:
            end = 2000

        dir = str(start) + "-" + str(end)

        i = 0
        for data in resultList:
            i = i + 1

            url = data['mhNewUrl']
            id = data['id']
            idStr = str(id)
            id = idStr.zfill(5)

            fileName = url[url.rindex("/") + 1: len(url) - 1]

            # http://127.0.0.1:8081/0-2000/00001_22.htm
            baseUrl = "http://127.0.0.1:8081/" + dir + "/" + id + "_" + fileName[0:len(fileName)]
            print(baseUrl)
            yield self.make_requests_from_url(baseUrl)

        yield

    def parse(self, response):
        content = response.body.decode("utf-8")
        # print(content)

        selector = Selector(text=content)

        chapterItem = selector.css("div.mCustomScrollBox").css("li")

        # for chapter in chapterItem:
        #
        #     pic = chapter.css("a::attr('href')").extract()[0]
        #     picTitle = chapter.css("a::text").extract()[0]
        #     picTitle_p = chapter.css("a").css("span::text").extract()[0]
        #
        #     print("\n")
        #     print("pic->" + pic +
        #           ",\npicTitle->" + picTitle +
        #           ",\npicTitle_p->" + picTitle_p)

        chapterItem = selector.css("script::text")[4].extract()
        pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')  # 匹配模式
        pic = chapterItem.split(";")[9]
        pic = re.findall(pattern, pic)[0]
        pic = pic[0:len(pic) - 1]

        count = chapterItem.split(";")[5]
        count = count[count.index("= ") + 2:len(count)]

        url = pic[0:pic.rindex("/")]
        id2 = url[url.rindex("/") + 1:len(url)]
        print(id2)

        url = url[0:url.rindex("/")]
        id1 = url[url.rindex("/") + 1:len(url)]
        print(id1)

        mid = getHashCode(id1)

        sourceUrl = response.url
        sourceUrl = "https://www.tohomh123.com/" +id1 + "/" + sourceUrl[sourceUrl.rindex("_") + 1 : sourceUrl.rindex(".")] +".html"
        print("首张图片地址是：" + pic + ", 总共：" + count + " P" + ", id1=" + id1 + ", id2=" + id2 + ", sourceUrl=" + sourceUrl)
        yield insertData2DB(mid, id1, pic, count, sourceUrl)


# 插入数据到数据库中
def insertData2DB(mid, mid2, picUrl, count, sourceUrl):
    from ManHua.items import ManHuaItem
    item = ManHuaItem()
    item['mid'] = mid
    item['mid2'] = mid2
    item['picUrl'] = picUrl
    item['count'] = count
    item['sourceUrl'] = sourceUrl
    return item
