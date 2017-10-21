from scrapy import Selector
from scrapy.spiders import Spider

from JueDiQiuSheng import Utils


class JueDiQiuSheng(Spider):
    name = "JueDiQiuSheng"
    start_urls = [
        "http://www.gamersky.com/z/playbattlegrounds/",
    ]

    def __init__(self):
        super(JueDiQiuSheng, self).__init__()

    def parse(self, response):
        content = response.body.decode("utf-8")

        currentUrl = response.url

        selector = Selector(text=content)

        GLHJtitSelector = selector.css("span.GLHJtit")

        # yield insertQuestionCategory(content)

        for item in GLHJtitSelector:
            try:
                name = item.css("a::text")[0].extract()
                url = item.css("a::attr(href)")[0].extract()
                category = Utils.getCategoryId(url)
                print("url: " + url + ", name: " + name)
                yield insertData2DB(name, url, category)
            except Exception as e:
                yield insertRMBB(currentUrl, item)
                pass


def insertRMBB(currentUrl, item):
    # 说明是 入门必备，需要单独获取数据并存储，并分配 id 为： 10001 自行入库
    name = item.css("span::text")[0].extract()
    url = currentUrl
    return insertData2DB(name, url, 10001)


def insertQuestionCategory(content):
    # 需要抓取的分类
    question = "问题"
    selector = Selector(text=content)
    # 获取大分类
    midLSelector = selector.css("div.Mid_L")[0]
    titleDiv = midLSelector.css("div.MidLcon_R").css("li.mjtit").css("div.title")
    titList = titleDiv.css("div.tit::text").extract()
    hrefA = titleDiv.css("div.more").css("a::attr(href)").extract()
    for i in range(len(titList)):
        if question == titList[i]:
            url = hrefA[i]
            jid = Utils.getCategoryId(url)
            print("对应的链接是：" + url)
            print("对应的jid 是：" + jid)
            return insertData2DB(question, url, jid)


# 插入数据到数据库中
def insertData2DB(name, url, category):
    from JueDiQiuSheng.items import JDQSDCategory
    item = JDQSDCategory()
    item['id'] = category
    item['categoryName'] = name
    item['categoryUrl'] = url
    item['artifactCollection'] = Utils.getCollectionTime()
    return item
