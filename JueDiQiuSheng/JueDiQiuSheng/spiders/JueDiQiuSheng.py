from scrapy import Selector
from scrapy.spiders import Spider

from JueDiQiuSheng import Utils


class JueDiQiuSheng(Spider):
    name = "JueDiQiuSheng"
    start_urls = [
        "http://www.gamersky.com/z/playbattlegrounds/"
    ]

    def __init__(self):
        super(JueDiQiuSheng, self).__init__()

    def parse(self, response):
        content = response.body.decode("utf-8")

        currentUrl = response.url

        selector = Selector(text=content)

        # yield insertQuestionCategory(content)

        url = "http://www.gamersky.com/z/playbattlegrounds/"
        # 插入葵花宝典,分配 id: 10002
        yield insertData2DB("葵花宝典", currentUrl, 10002)

        url = "http://www.gamersky.com/z/playbattlegrounds/"
        # 插入精品推荐,分配 id: 10003
        yield insertData2DB("精品推荐", currentUrl, 10003)

        url = "http://www.gamersky.com/z/playbattlegrounds/handbook/"
        # 插入攻略专题,分配 id: 10004
        yield insertData2DB("攻略专题", url, 10004)

        url = "http://www.gamersky.com/z/playbattlegrounds/news/"
        # 插入热门资讯,分配 id: 10005
        yield insertData2DB("热门资讯", url, 10005)

        url = "http://www.gamersky.com/z/playbattlegrounds/862094_32615/"
        # 插入游戏更新,分配 id: 10006
        yield insertData2DB("游戏更新", url, 10006)

        url = "http://www.gamersky.com/z/playbattlegrounds/862094_28330/"
        # 插入上手体验,分配 id: 10007
        yield insertData2DB("上手体验", url, 10007)

        url = "http://www.gamersky.com/z/playbattlegrounds/862094_34214/"
        # 插入视频解说,分配 id: 10008
        yield insertData2DB("视频解说", url, 10008)

        # yield insertZiXunItem(selector)


# def insertZiXunItem(selector):
#     navHeaderSelector = selector.css("ul.nav").css("a::text")
#
#     for i in range(len(navHeaderSelector)):
#         name = navHeaderSelector[i].extract()
#         if name == "资讯":
#             zxName = name
#             zxUrl = selector.css("ul.nav").css("a::attr(href)")[i].extract()
#             return insertData2DB(zxName, zxUrl, 10000)


# 插入数据到数据库中
def insertData2DB(name, url, category):
    from JueDiQiuSheng.items import JDQSDCategory
    item = JDQSDCategory()
    item['id'] = category
    item['tjName'] = name
    item['tjUrl'] = url
    item['tjCollection'] = Utils.getCollectionTime()
    return item
