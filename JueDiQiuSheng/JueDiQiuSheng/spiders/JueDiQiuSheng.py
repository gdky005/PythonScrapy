import requests
from scrapy import Selector, Request
from scrapy.spiders import Spider

from JueDiQiuSheng import Utils, JDQSDriverUtils


class JueDiQiuSheng(Spider):
    name = "JueDiQiuSheng"
    start_urls = [
        # Bug问题
        # "http://www.gamersky.com/z/playbattlegrounds/862094_34425/",
        # 葵花宝典, 精品推荐
        # "http://www.gamersky.com/z/playbattlegrounds/",
        # 攻略专题
        # "http://www.gamersky.com/z/playbattlegrounds/handbook/",
        # 热门资讯
        # "http://www.gamersky.com/z/playbattlegrounds/news/"
        # 游戏更新
        # "http://www.gamersky.com/z/playbattlegrounds/862094_32615/"
        # 上手体验
        # "http://www.gamersky.com/z/playbattlegrounds/862094_28330/"
        # 游戏解说
        "http://www.gamersky.com/z/playbattlegrounds/862094_34214/"
    ]

    def __init__(self):
        super(JueDiQiuSheng, self).__init__()
        # print("当前运行时间是：" + Utils.getCollectionTime())

    def start_requests(self):
        params = {'pageCount': '100'}
        # 分类接口
        content = requests.get('http://zkteam.cc/JueDiQiuSheng/recommendedJson', params)
        json = content.json()
        resultJson = json["result"]

        for result in resultJson:
            newUrl = result["tjUrl"]
            print("当前抓取的 Url 是：" + newUrl)
            yield Request(newUrl)

    def parse(self, response):
        content = response.body.decode("utf-8")
        # print(content)

        currentUrl = response.url

        list = []
        categoryID = ""

        if currentUrl == 'http://www.gamersky.com/z/playbattlegrounds/':
            # 葵花宝典
            categoryID = 10002
            queryKHBDData(content, list, categoryID)

            # 精品推荐
            categoryID = 10003
            queryJPTJData(content, list, categoryID)

        if currentUrl == 'http://www.gamersky.com/z/playbattlegrounds/handbook/':
            # 攻略专题
            categoryID = 10004
            queryTopTJData(content, list, categoryID)

        if currentUrl == 'http://www.gamersky.com/z/playbattlegrounds/news/':
            # 热门资讯
            categoryID = 10005
            queryTopTJData(content, list, categoryID)

        if currentUrl == 'http://www.gamersky.com/z/playbattlegrounds/862094_32615/':
            # 游戏更新
            categoryID = 10006
            queryTextItemData(content, list, categoryID)

        if currentUrl == 'http://www.gamersky.com/z/playbattlegrounds/862094_28330/':
            # 上手体验
            categoryID = 10007
            queryTextItemData(content, list, categoryID)

        if currentUrl == 'http://www.gamersky.com/z/playbattlegrounds/862094_34214/':
            # 游戏解说
            categoryID = 10008
            queryYXJSJData(content, list, categoryID)

        for item in list:
            yield item

    def close(self, reason):
        # self.driver.close()
        print("当前结束时间是：" + Utils.getCollectionTime())


def queryKHBDData(content, khbdList, categoryId):
    selector = Selector(text=content)

    textSelector = selector.css("ul.bgx").css("a::text").extract()

    for i in range(len(textSelector)):
        picUrl = ''
        name = textSelector[i]
        url = selector.css("ul.bgx").css("a::attr(href)")[i].extract()

        data = JDQSDriverUtils.insertItemData2DB(name, Utils.getCollectionTime(), url, picUrl, categoryId)
        khbdList.append(data)


def queryJPTJData(content, jptjList, categoryId):
    selector = Selector(text=content)

    textSelector = selector.css("ul.ML1pic").css("a")

    for item in textSelector:
        url = item.css("::attr(href)")[0].extract()
        picUrl = item.css("img::attr(src)")[0].extract()
        name = item.css("img::attr(alt)")[0].extract()
        data = JDQSDriverUtils.insertItemData2DB(name, Utils.getCollectionTime(), url, picUrl, categoryId)
        jptjList.append(data)


def queryTopTJData(content, list, categoryId):
    selector = Selector(text=content)

    textSelector = selector.css("div.Midcon").css("li.img")

    for item in textSelector:
        url = item.css("::attr(href)")[0].extract()
        picUrl = item.css("img::attr(src)")[0].extract()
        name = item.css("img::attr(alt)")[0].extract()
        data = JDQSDriverUtils.insertItemData2DB(name, Utils.getCollectionTime(), url, picUrl, categoryId)
        list.append(data)


def queryYXJSJData(content, list, categoryId):
    selector = Selector(text=content)

    textSelector = selector.css("div.MidLcon").css("li").css("a")

    for item in textSelector:
        url = item.css("::attr(href)")[0].extract()
        picUrl = item.css("img::attr(src)")[0].extract()
        name = item.css("img::attr(alt)")[0].extract()
        data = JDQSDriverUtils.insertItemData2DB(name, Utils.getCollectionTime(), url, picUrl, categoryId)
        list.append(data)


def queryTextItemData(content, list, categoryId):
    selector = Selector(text=content)

    textSelector = selector.css("ul.titlist").css("li.li1")

    for item in textSelector:
        url = item.css("::attr(href)")[0].extract()
        # 这里暂时没有图片，需要的话，可以后面添加
        # picUrl = item.css("img::attr(src)")[0].extract()
        picUrl = ""
        name = item.css("a::attr(title)")[0].extract()
        date = item.css("div.time::text")[0].extract()
        data = JDQSDriverUtils.insertItemData2DB(name, date, url, picUrl, categoryId)
        list.append(data)
