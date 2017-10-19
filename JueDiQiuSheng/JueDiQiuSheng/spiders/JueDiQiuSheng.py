import requests
import scrapy
import time
from parsel import SelectorList
from scrapy import Selector, Request
from scrapy.spiders import Spider
from selenium import webdriver

import JueDiQiuSheng.Constant_JDQS as Constant

from JueDiQiuSheng.items import JDQSContentItem

from JueDiQiuSheng import Utils


class JueDiQiuSheng(Spider):
    name = "JueDiQiuSheng"
    start_urls = [
        # 图文网页
        "http://www.gamersky.com/handbook/201710/967630.shtml",
        # "http://www.gamersky.com/handbook/201705/906915.shtml",
        # "http://www.gamersky.com/handbook/201708/945256.shtml",
        # 分页
        # "http://www.gamersky.com/handbook/201704/893376.shtml",
    ]

    def __init__(self):
        super(JueDiQiuSheng, self).__init__()

    def start_requests(self):

        params = {'pageCount': '100'}
        content = requests.get('http://zkteam.cc/JueDiQiuSheng/json', params)
        json = content.json()
        resultJson = json["result"]

        for result in resultJson:
            newUrl = result["artifactSourceUrl"]
            print("当前抓取的 Url 是：" + newUrl)
            yield Request(newUrl)

    def parse(self, response):
        content = response.body.decode("utf-8")
        # print(content)
        selector = Selector(text=content)

        jid = Utils.getJid(response.url)

        print("当前文件中的 id 是：" + jid)

        # yield insertData2DB(jid, "我是文章名字", "wq", "我是内容内容")

        pages = []
        subString = ""

        initParams()

        getPageCount(selector, pages)

        word = selector.css("div.Mid2L_tit")
        articleName = word.css("h1::text")[0].extract()
        articleAuthor = word.css("div.detail::text")[0].extract().strip()

        Constant.jid_id = Utils.getJid(response.url)
        Constant.artifactName = articleName
        Constant.artifactAuthor = articleAuthor
        Constant.artifactSourceUrl = response.url

        print("文章名称：\r\n\t" + articleName)
        print("文章作者：\r\n\t" + articleAuthor)
        print("\r\n\t下面是正文：\r\n\t")

        subString += "<h1><p align=\"center\">" + articleName + "</p></h1>\r\n"
        subString += "<h5><p align=\"right\">" + articleAuthor + "</p></h5>"

        wordDetail = selector.css("div.Mid2L_con")
        elements = wordDetail.xpath("p")

        subString += getContent(elements)

        Constant.global_detail_list.append(subString)

        length = len(pages)

        if length is None or length == 0:
            print("正文内容是：\r\n" + subString)
            Constant.artifactContent = subString
            yield insertData2DB()
        else:
            for i in range(length):
                yield scrapy.Request(url=pages[i], meta={
                    "page": i + 1,
                    "pageCount": length,
                    "jid": jid,
                    "articleName": articleName,
                    "articleAuthor": articleAuthor,
                }, callback=self.parserData)

    @staticmethod
    def parserData(response):
        content = response.body.decode("utf-8")
        # print(content)

        page = response.meta["page"]
        pageCount = response.meta["pageCount"]

        subString = ""
        selector = Selector(text=content)

        elements = selector.css("div.Mid2L_con").xpath("p")
        subString += getContent(elements)

        Constant.global_detail_list.append(subString)

        if pageCount == page:
            globalList = Constant.global_detail_list

            content = ""
            for text in globalList:
                content += text

            Constant.artifactContent = content
            print("正文内容是：\r\n" + content)
            yield insertData2DB()

            Constant.global_detail_list.clear()


def initParams():
    Constant.jid_id = ""
    Constant.artifactName = ""
    Constant.artifactAuthor = ""
    Constant.artifactContent = ""
    Constant.artifactSourceUrl = ""
    Constant.artifactUrl = ""
    Constant.global_detail_list.clear()


# 获取总页数
def getPageCount(selector, pages):
    pageElements = selector.css("div.page_css").xpath("a")
    for i in range(len(pageElements)):
        if i == len(pageElements) - 1:
            continue

        page = pageElements[i].css("a::attr(href)")[0].extract()
        pages.append(page)


# 获取文章中的主要内容
def getContent(elements):
    subString = ""
    for i in range(len(elements)):

        if i >= (len(elements) - 2):
            break

        text = elements[i].extract()
        if "data-src" in text:
            text = text.replace("src=\"http://image.gamersky.com/webimg13/zhuanti/common/blank.png\" data-", "")
        subString += text
        subString += "\n"
    return subString


# 插入数据到数据库中
def insertData2DB():
    item = JDQSContentItem()

    item['artifactName'] = Constant.artifactName
    item['artifactAuthor'] = Constant.artifactAuthor
    item['artifactContent'] = Constant.artifactContent
    item['jid_id'] = Constant.jid_id
    item['artifactSourceUrl'] = Constant.artifactSourceUrl
    item['artifactUrl'] = Constant.artifactUrl
    item['artifactCollection'] = Utils.getCollectionTime()

    return item
