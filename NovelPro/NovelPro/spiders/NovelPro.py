from scrapy import Selector
from scrapy.spiders import Spider


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

        for chapterName in chapterNameExtract:
            name = chapterName.css("h2::text").extract()[0]
            author = chapterName.css("div.shiwen").css("div::text").extract()[0].strip()
            author = author[author.index("：") + 1:author.rindex(")")]

            details = chapterName.css("div.shiwen").css("p::text").extract()

            detailStr = "\n"
            for index, detailItem in enumerate(details):
                if index >= len(details) - 4:
                    break
                detailStr += "    " + detailItem + "\n"

            print("\n名字=" + name
                  + ", \nauthor=" + author
                  + ", \nurl=" + url)

            print("\ndetailStr：" + detailStr)
