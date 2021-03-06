import scrapy
from parsel import SelectorList
from scrapy import Selector
from scrapy.spiders import Spider
from selenium import webdriver

import JueDiQiuSheng.Constant_JDQS as Constant

from JueDiQiuSheng.items import JDQSDetailItem


class JueDiQiuShengDetail(Spider):
    name = "JueDiQiuShengDetail"
    start_urls = [
        # 图文网页
        # "http://www.gamersky.com/handbook/201705/906915.shtml",
        # "http://www.gamersky.com/handbook/201708/945256.shtml",
        # 分页
        "http://www.gamersky.com/handbook/201704/893376.shtml",
    ]

    def __init__(self):
        super(JueDiQiuShengDetail, self).__init__()

    def parse(self, response):
        content = response.body.decode("utf-8")
        # print(content)
        selector = Selector(text=content)

        jid = getJid(response.url)

        print("当前文件中的 id 是：" + jid)

        # yield insertData2DB(jid, "我是文章名字", "wq", "我是内容内容")


        pages = []
        subString = ""

        getPageCount(selector, pages)

        word = selector.css("div.Mid2L_tit")
        articleName = word.css("h1::text")[0].extract()
        articleAuthor = word.css("div.detail::text")[0].extract().strip()

        print("文章名称：\r\n\t" + articleName)
        print("文章作者：\r\n\t" + articleAuthor)
        print("\r\n\t下面是正文：\r\n\t")

        subString += "<h1><p align=\"center\">" + articleName + "</p></h1>\r\n"
        subString += "<h5><p align=\"right\">" + articleAuthor + "</p></h5>"

        wordDetail = selector.css("div.Mid2L_con")
        elements = wordDetail.xpath("p")

        subString += getContent(elements)

        Constant.global_detail_list.clear()
        Constant.global_detail_list.append(subString)

        length = len(pages)

        if length is None or length == 0:
            print("正文内容是：\r\n" + subString)
            yield insertData2DB(jid, articleName, articleAuthor, subString)
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
        jid = response.meta["jid"]
        articleName = response.meta["articleName"]
        articleAuthor = response.meta["articleAuthor"]

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

            print("正文内容是：\r\n" + content)
            yield insertData2DB(jid, articleName, articleAuthor, content)

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


# 根据 Url 获取 Jid
def getJid(url):
    try:
        start = url.rindex("/")
        end = url.rindex(".")
        newUrl = url[(start + 1):end]
        if newUrl.__contains__("-"):
            newUrl = newUrl[0:newUrl.rindex("-")]
    except:
        newUrl = url
        pass

    return newUrl


# 插入数据到数据库中
def insertData2DB(jid, artifact_name, artifact_author, content):
    item = JDQSDetailItem()
    item['jid'] = jid
    item['artifactName'] = artifact_name
    item['artifactAuthor'] = artifact_author
    item['content'] = content

    return item
