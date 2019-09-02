import urllib

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
        # print(content)

        # print("爬取的内容如下：" + content)

        selector = Selector(text=content)

        # selector.css("dl.cat-list").css("dd")
        chapterNameExtract = selector.css("div.wen-box")

        nextUrl = ""
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

                nextUrl = mPageUrl

                print("当前页数是：" + mPageNum + ", pageUrl=" + mPageUrl)

            print("\n名字=" + name
                  + ", \nauthor=" + author
                  + ", \nurl=" + url)

            # print("\ndetailStr：" + detailStr)


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

        print("\ndetailStr：\n" + detailStr)