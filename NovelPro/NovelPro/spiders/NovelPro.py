import urllib
from urllib.parse import urlparse

from scrapy import Selector
from scrapy.spiders import Spider
import requests


class NovelPro(Spider):
    name = "NovelPro"
    start_urls = [
        # "https://m.liyuxiang.net/gushi/duanpianxiaoshuo.html",
        "https://m.liyuxiang.net/gushi/2/12795.html",
    ]

    def __init__(self):
        super(NovelPro, self).__init__()

    def parse(self, response):
        content = response.body.decode('utf-8')
        url = response.url
        # print("爬取的内容如下：" + content)

        selector = Selector(text=content)
        chapterNameExtract = selector.css("div.wen-box")

        detailStr = ""
        for chapterName in chapterNameExtract:
            name = chapterName.css("h2::text").extract()[0]
            author = chapterName.css("div.shiwen").css("div::text").extract()[0].strip()
            author = author[author.index("：") + 1:author.rindex(")")]

            details = chapterName.css("div.shiwen").css("p::text").extract()
            detailStr = "\n"
            for index, detailItem in enumerate(details):
                if index >= len(details) - 4:
                    break
                detailItem = detailItem.strip()
                if detailItem != "":
                    detailStr += "    " + detailItem + "\n"

            pages = chapterName.css("div.shiwen").css("p.pages-box").css("a")

            pageNum = pages.css("a::text").extract()
            pageUrl = pages.css('a::attr(href)').extract()
            for index, pageNumber in enumerate(pages):
                if index >= len(pages) - 1:
                    break
                mPageNum = pageNum[index]
                mPageUrl = pageUrl[index]
                print("当前页数是：" + mPageNum + ", pageUrl=" + mPageUrl)

                # 获取当前页面 索引的下一页
                res = urlparse(url)
                if mPageUrl == res.path:
                    nextPage = pageUrl[index + 1]
                    detailStr = self.getNextPageContent(detailStr, nextPage)

            print("\n名字=" + name
                  + ", \nauthor=" + author
                  + ", \nurl=" + url)

        print("\ndetailStr：\n" + detailStr)

    def getNextPageContent(self, detailStr, nextUrl):
        resp = requests.get("https://m.liyuxiang.net/" + nextUrl)
        content = resp.text
        selector1 = Selector(text=content)
        chapterNameExtract1 = selector1.css("div.wen-box")
        for chapterName in chapterNameExtract1:
            details = chapterName.css("div.shiwen").css("p::text").extract()
            for index, detailItem in enumerate(details):
                if index >= len(details) - 4:
                    break
                if detailItem != "":
                    detailStr += "    " + detailItem + "\n"
        return detailStr