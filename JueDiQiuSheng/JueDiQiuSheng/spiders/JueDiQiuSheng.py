from parsel import SelectorList
from scrapy import Selector
from scrapy.spiders import Spider
from selenium import webdriver

from JueDiQiuSheng.items import JDQSItem

from JueDiQiuSheng import Utils


class JueDiQiuSheng(Spider):
    name = "JueDiQiuSheng"
    start_urls = [
        "http://www.gamersky.com/z/playbattlegrounds/862094_34425/",
    ]

    def __init__(self):
        super(JueDiQiuSheng, self).__init__()

    def parse(self, response):
        content = response.body.decode("utf-8")
        # print(content)

        selector = Selector(text=content)

        categoryId = Utils.getCategoryId(response.url)
        itemList = selector.css("ul.titlist").css("li.li1")
        for item in itemList:
            picUrl = ""

            artifactName = item.css("a::attr(title)")[0].extract()
            artifactDate = item.css("div.time::text")[0].extract()
            artifactSourceUrl = item.css("a::attr(href)")[0].extract()

            print("当前的分类 id 是：" + categoryId)
            print("当前的分类 name 是：" + artifactName)
            print("当前的分类 href 是：" + artifactDate)
            print("当前的分类 date 是：" + artifactSourceUrl)

            yield insertData2DB(artifactName, artifactDate, artifactSourceUrl, picUrl, categoryId)


            # 获取时间
            # selector.css("ul.titlist").css("li.li1").css("div.time::text")[0].extract()
            # 获取链接
            # selector.css("ul.titlist").css("li.li1")[0].css("a::attr(href)")[0].extract()
            # 获取名称
            # selector.css("ul.titlist").css("li.li1")[0].css("a::attr(title)")[0].extract()

            # # 获取大分类
            # midLSelector = selector.css("div.Mid_L")[0]
            #
            # midLtit = midLSelector.css("div.MidLtit")
            # bigTitle = midLtit.css("div.tit.t1::text")[0].extract()
            # print("大标题是：" + bigTitle)

            # # // 攻略合集
            # g_l_h_j = midLSelector.css("div.MidLcon.GLHJ")
            # g_l_h_j2 = g_l_h_j.css("div.GLHJ-2")
            #
            # infoList = []
            #
            # infoList += rmbb(g_l_h_j)
            # infoList += getOtherKinds(g_l_h_j2)
            #
            # for e in infoList:
            #     name = e["name"]
            #     url = e["url"]
            #     picUrl = e["picUrl"]
            #     category_id = e["category_id"]
            #     category_name = e["category_name"]
            #
            #     print(
            #         "\tname: " + name +
            #         "\tcategory_id: " + category_id +
            #         "\tcategory_name: " + category_name
            #     )
            #
            #     yield insertData2DB(name, url, picUrl, category_id, category_name)


# 入门必备
def rmbb(element):
    infoList = []
    GLHJtit = element.css("span.GLHJtit")

    name = GLHJtit.css("span::text").extract()[0]
    print("小标题是：" + name)

    imgliklistElements = element.css("ul.imgliklist")
    elements = imgliklistElements.css("li.img")
    print("获取 " + name + " 带图片属性：")
    infoList += getElement(elements)

    linkElements = imgliklistElements.css("li.lik").css("div.link")
    print("获取 " + name + " link 属性：")
    infoList += getElement(linkElements)

    category_url = GLHJtit.css("a::attr('href')").extract()[0]
    addCategoryData(infoList, name, category_url)

    return infoList


# 添加分类属性
def addCategoryData(infoList, name, category_url):
    category_id = Utils.getCategoryId(category_url)
    print("获取 " + name + " category_id：" + category_id)
    for item in infoList:
        item["category_id"] = category_id
        item["category_name"] = name


# 获取 攻略合集 里面 除过 入门必备 的其他分类
def getOtherKinds(element):
    infoList = []

    for e in element:
        sTitle = e.css("span.GLHJtit")
        name = sTitle.xpath("string(.)").extract()[0]
        print("小标题：\n\t" + name)

        imgliklistElements = e.css("ul.liklist").css("li.line1")
        print("获取 " + name + " 带图片属性：")
        elementList = getElement(imgliklistElements)

        try:
            category_url = sTitle.css("a::attr('href')").extract()[0]
            addCategoryData(elementList, name, category_url)
        except:
            pass

        infoList += elementList

    return infoList


# 获取相关属性
def getElement(element):
    infoList = []

    for e in element:
        name = ""
        url = ""
        picUrl = ""

        try:
            name = e.xpath("string(.)").extract()[0].strip()
        except:
            pass

        try:
            url = e.css("a::attr(href)").extract()[0]
        except:
            pass

        try:
            picUrl = e.css("img::attr(src)").extract()[0]
        except:
            pass

        print("\t属性是：\n\t\t" +
              "name:" + name + "\r\n\t\t" +
              "url:" + url + "\r\n\t\t" +
              "picUrl:" + picUrl + "\r\n\t\t")

        print("\r")

        d = {'name': name, 'url': url, 'picUrl': picUrl}
        infoList.append(d)

    return infoList


# 插入数据到数据库中
def insertData2DB(artifactName, artifactDate, artifactSourceUrl, picUrl, categoryId):
    jid = Utils.getJid(artifactSourceUrl)

    url = '<p><a href="http://www.zkteam.cc/JueDiQiuSheng/detail.html?jid=' + jid + \
          '">http://www.zkteam.cc/JueDiQiuSheng/detail.html?jid=' + jid + "</a></p>"

    item = JDQSItem()
    item['id'] = jid
    item['artifactName'] = artifactName
    item['artifactDate'] = artifactDate
    item['artifactSourceUrl'] = artifactSourceUrl
    item['artifactUrl'] = url
    item['picUrl'] = picUrl
    item['categoryId'] = categoryId

    return item
