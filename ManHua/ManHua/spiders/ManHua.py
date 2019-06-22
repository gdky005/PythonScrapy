from scrapy import Selector
from scrapy.spiders import Spider

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
        "https://www.tohomh123.com/zhenhunjie/",
        # "https://www.tohomh123.com/f-1------updatetime--1.html",
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

        pic = selector.css("div.cover").css("img::attr('src')").extract()[0]
        title = selector.css("div.info").css("h1::text").extract()[0]
        author = selector.css("div.info").css("p::text").extract()[0]
        state = selector.css("p.tip").css("span.block")[0].css("span::text").extract()[1]
        time = selector.css("p.tip").css("span.block")[2].css("span::text").extract()[0]
        detail = selector.css("p.content").css("p::text").extract()[0]

        category = selector.css("p.tip").css("span.block")[1].css("a::text").extract()
        tag = selector.css("p.tip").css("span.block")[3].css("a::text").extract()

        url = response.url
        url = url[url.index("com/") + 4:url.rindex("/")]

        print("当前计算的 url 是：" + url)
        mid = getHashCode(url)

        sort = selector.css("div.left-bar")[0].css("div.detail-list-title").css("a::text").extract()[0] # 倒序

        chapterItem = selector.css("div.left-bar")[0].css("ul.view-win-list.detail-list-select")[1].css("li")

        for chapter in chapterItem:
            chapterName = chapter.css("a::text").extract()[0]
            chapterName_p = chapter.css("a").css("span::text").extract()[0]
            chapterUrl = "https://www.tohomh123.com" + chapter.css("a::attr(href)").extract()[0]

            count = chapterName_p[chapterName_p.index("（") + 1:chapterName_p.index("P")]

            print("\n")
            print("chapterName->" + chapterName +
                  ",\nchapterName_p->" + chapterName_p +
                  ",\nchapterUrl->" + chapterUrl +
                  ",\nmid->" + str(mid)
                  )
            yield insertData2DB(mid, chapterName, chapterUrl, chapterName_p, count)


# 插入数据到数据库中
def insertData2DB(mid, name, url, pCount, count):
    from ManHua.items import ManHuaItem
    item = ManHuaItem()
    item['mid'] = mid
    item['name'] = name
    item['url'] = url
    item['pCount'] = pCount
    item['count'] = count
    return item


def getStringForList(items):
    data = ''
    for item in items:
        data += (item + ",")
    return data[0:len(data)-1]
