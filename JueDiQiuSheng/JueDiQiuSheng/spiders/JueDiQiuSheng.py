from scrapy import Selector
from scrapy.spiders import Spider


class JueDiQiuSheng(Spider):
    name = "JueDiQiuSheng"
    start_urls = [
        "http://www.gamersky.com/z/playbattlegrounds/",
    ]

    def __init__(self):
        super(JueDiQiuSheng, self).__init__()

    def parse(self, response):
        content = response.body.decode("utf-8")

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
                jid = getCategoryId(url)
                print("对应的链接是：" + url)
                print("对应的jid 是：" + jid)
                yield insertData2DB(question, url)


# 获取对应的 category_id
def getCategoryId(url):
    url = url[0: url.__len__() - 1]
    print(url)

    start = url.rindex("_")
    categoryId = url[(start + 1):url.__len__()]
    if categoryId.__contains__("-"):
        categoryId = categoryId[0:categoryId.rindex("-")]
    return categoryId


# 插入数据到数据库中
def insertData2DB(name, url):
    jid = getCategoryId(url)

    from JueDiQiuSheng.items import JDQSDCategory
    item = JDQSDCategory()
    item['categoryId'] = jid
    item['categoryName'] = name
    item['categoryUrl'] = url

    return item
