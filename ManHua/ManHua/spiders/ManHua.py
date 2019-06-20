from scrapy import Selector
from scrapy.spiders import Spider


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


class ManHua(Spider):
    name = "ManHua"
    start_urls = [
        "https://www.tohomh123.com/f-1------updatetime--1.html",
        # "https://www.tohomh123.com",
        # "http://www.gamersky.com/z/playbattlegrounds/",
    ]

    def __init__(self):
        super(ManHua, self).__init__()

    def parse(self, response):
        content = response.body.decode("utf-8")
        # print(content)

        selector = Selector(text=content)

        itemSelector = selector.css("div.mh-item")

        for item in itemSelector:
            pic = getPic(item)
            title = getTitle(item)
            newPageName = getNewPageName(item)
            print("\n")
            print("\npic->" + pic +
                  "\ntitle->" + title +
                  "\nnewPageName->" + newPageName
                  )
            yield insertData2DB(pic, newPageName, title)


# 插入数据到数据库中
def insertData2DB(picUrl, newPage, name):
    from ManHua.items import ManHuaItem
    item = ManHuaItem()
    item['picUrl'] = picUrl
    item['newPage'] = newPage
    item['name'] = name
    return item