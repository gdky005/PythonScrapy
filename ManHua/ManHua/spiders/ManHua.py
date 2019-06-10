from scrapy import Selector
from scrapy.spiders import Spider


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
        "https://www.tohomh123.com/f-1------updatetime--1.html",
        # "https://www.tohomh123.com/f-1-1-----hits--1.html",
        # "https://www.tohomh123.com",
        # "http://www.gamersky.com/z/playbattlegrounds/",
    ]

    def __init__(self):
        super(ManHua, self).__init__()

    def parse(self, response):
        content = response.body.decode("utf-8")
        # print(content)

        selector = Selector(text=content)

        itemSelector = selector.css("dl.cat-list").css("dd")
        for item in itemSelector:
            categoryText = item.css("a::text").extract()[0]
            categoryUrl = "https://www.tohomh123.com" + item.css("dd").css("a::attr('href')").extract()[0]
            print("\n")
            print("categoryText->" + categoryText +
                  ",\ncategoryUrl->" + categoryUrl)

    # # 获取文章中的主要内容
    # def getContent(elements):
    #     subString = ""
    #     for i in range(len(elements)):
    #
    #         if i >= (len(elements) - 2):
    #             break
    #
    #         text = elements[i].extract()
    #         if "data-src" in text:
    #             text = text.replace("src=\"http://image.gamersky.com/webimg13/zhuanti/common/blank.png\" data-", "")
    #         subString += text
    #         subString += "\n"
    #     return subString
