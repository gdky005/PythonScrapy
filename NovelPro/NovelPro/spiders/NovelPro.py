from scrapy import Selector
from scrapy.spiders import Spider


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

        # print("爬取的内容如下：" + content)

        selector = Selector(text=content)

        # selector.css("dl.cat-list").css("dd")
        chapterNameExtract = selector.css("div.box-left").css("ul.article-lists").css("li")

        for chapterName in chapterNameExtract:
            name = chapterName.css("a::text").extract()[0]
            url = chapterName.css("a::attr(href)").extract()[0]
            print("我需要的名称：" + name + ", url=" + url)
