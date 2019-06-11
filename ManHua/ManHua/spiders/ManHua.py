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
            categoryName = item.css("a::text").extract()[0]
            categoryUrl = "https://www.tohomh123.com" + item.css("dd").css("a::attr('href')").extract()[0]
            categoryId = categoryUrl[categoryUrl.index("/f-") + 2:categoryUrl.index("-----")]
            categoryId = categoryId.replace("-", "")

            print("\n")
            print("categoryText->" + categoryName +
                  ",\ncategoryUrl->" + categoryUrl +
                  ",\ncategoryId->" + categoryId
                  )

            yield insertData2DB(categoryId, categoryUrl, categoryName)


# 插入数据到数据库中
def insertData2DB(mid, url, name):
    from ManHua.items import ManHuaItem
    item = ManHuaItem()
    item['mid'] = mid
    item['url'] = url
    item['name'] = name
    return item
