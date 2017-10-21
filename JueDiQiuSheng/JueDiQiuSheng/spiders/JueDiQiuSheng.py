from scrapy import Selector
from scrapy.spiders import Spider


from JueDiQiuSheng import Utils, JDQSDriverUtils


class JueDiQiuSheng(Spider):
    name = "JueDiQiuSheng"
    start_urls = [
        # Bug问题
        # "http://www.gamersky.com/z/playbattlegrounds/862094_34425/",
        # 葵花宝典
        "http://www.gamersky.com/z/playbattlegrounds/",
        # 攻略专题
        "http://www.gamersky.com/z/playbattlegrounds/handbook/",
        # 武器和装备
        # "http://www.gamersky.com/z/playbattlegrounds/862094_6792/"
        # 资讯
        # "http://www.gamersky.com/z/playbattlegrounds/news/"
    ]

    def __init__(self):
        super(JueDiQiuSheng, self).__init__()
        # print("当前运行时间是：" + Utils.getCollectionTime())

    def parse(self, response):
        content = response.body.decode("utf-8")
        # print(content)

        currentUrl = response.url

        if currentUrl == 'http://www.gamersky.com/z/playbattlegrounds/':
            khbdList = []
            queryKHBDData(content, khbdList, 10002)
            for item in khbdList:
                yield item

            jptjList = []
            queryJPTJData(content, jptjList, 10003)
            for item in jptjList:
                yield item

        if currentUrl == 'http://www.gamersky.com/z/playbattlegrounds/handbook/':
            glztList = []
            queryGLZTData(content, glztList, 10004)
            for item in glztList:
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


def queryGLZTData(content, glztList, categoryId):
    selector = Selector(text=content)

    textSelector = selector.css("div.Midcon").css("li.img")

    for item in textSelector:
        url = item.css("::attr(href)")[0].extract()
        picUrl = item.css("img::attr(src)")[0].extract()
        name = item.css("img::attr(alt)")[0].extract()
        data = JDQSDriverUtils.insertItemData2DB(name, Utils.getCollectionTime(), url, picUrl, categoryId)
        glztList.append(data)
