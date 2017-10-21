from scrapy import Selector
from scrapy.spiders import Spider

from JueDiQiuSheng import Utils


class JDQSPicCategory(Spider):
    name = "JueDiQiuSheng"
    start_urls = [
        # "http://www.gamersky.com/z/playbattlegrounds/",
        # 图库总页面
        "http://pic.gamersky.com/game/playerunknowns-battlegrounds/",
    ]

    def __init__(self):
        super(JDQSPicCategory, self).__init__()

    def parse(self, response):
        content = response.body.decode("utf-8")

        # 需要抓取的分类

        selector = Selector(text=content)

        # 获取大分类
        midtitSelector = selector.css("div.Midtit")

        for item in midtitSelector:
            url = item.css("a::attr(href)")[0].extract()
            name = item.css("h3::text")[0].extract()
            if url is not None and url != "":
                print("name: " + name)
                print("url: " + url)
                yield insertData2DB(name, url)


# 插入数据到数据库中
def insertData2DB(picCategoryName, picCategoryUrl):
    jid = Utils.getJid(picCategoryUrl)

    from JueDiQiuSheng.items import JDQSDPicCategoryItem
    item = JDQSDPicCategoryItem()
    item['id'] = jid
    item['picCategoryName'] = picCategoryName
    item['picCategoryUrl'] = picCategoryUrl
    item['picCategoryCollection'] = Utils.getCollectionTime()

    return item
