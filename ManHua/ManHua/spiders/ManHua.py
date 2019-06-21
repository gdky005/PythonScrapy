from urllib.parse import urlparse

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


def getMHUrl(selector):
    # 获取漫画的当前 URL
    mhUrlList = selector.css("a::attr('href')").extract()
    for mhUrl in mhUrlList:
        # print("mhUrl: " + mhUrl)
        return mhUrl


def getMHNewUrl(selector):
    # 获取漫画的最新章节 URL
    mhNewUrlList = selector.css("div.mh-item-detali").css("p.chapter").css("a::attr('href')").extract()
    for mhNewUrl in mhNewUrlList:
        # print("mhNewUrl: " + mhNewUrl)
        return mhNewUrl


class ManHua(Spider):
    name = "ManHua"
    start_urls = [
        "https://www.tohomh123.com/f-1------updatetime--377.html",
        # "https://www.tohomh123.com",
        # "http://www.gamersky.com/z/playbattlegrounds/",
    ]

    def __init__(self):
        super(ManHua, self).__init__()

    def parse(self, response):
        content = response.body.decode("utf-8")
        # print(content)

        result = urlparse(response.url)
        domain = result[0] + "://" + result[1]
        print(domain)

        selector = Selector(text=content)

        itemSelector = selector.css("div.mh-item")

        for item in itemSelector:
            pic = getPic(item)
            title = getTitle(item)
            newPageName = getNewPageName(item)

            mhPath = getMHUrl(item)
            mid2 = mhPath.replace("/", "")
            mhUrl = domain + mhPath
            mhNewUrl = domain + getMHNewUrl(item)

            print("\npic->" + pic +
                  "\ntitle->" + title +
                  "\nmid2->" + mid2 +
                  "\nnewPageName->" + newPageName +
                  "\nmhUrl->" + mhUrl +
                  "\nmhNewUrl->" + mhNewUrl +
                  "\n"
                  )

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

# 插入数据到数据库中
def insertData2DB(mid, url, name):
    from ManHua.items import ManHuaItem

    # id = models.IntegerField(primary_key=True).auto_created
    # mid2 = models.TextField()
    # name = models.TextField()
    # picUrl = models.TextField()
    # newPageName = models.TextField()
    # mhUrl = models.TextField()
    # mhNewUrl = models.TextField()

    item = ManHuaItem()
    item['mid'] = mid
    item['url'] = url
    item['name'] = name
    return item