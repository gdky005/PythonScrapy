from parsel import SelectorList
from scrapy import Selector
from scrapy.spiders import Spider
from selenium import webdriver

from JueDiQiuSheng.items import JuediqiushengItem


class JueDiQiuSheng(Spider):
    name = "JueDiQiuSheng"
    start_urls = [
        "http://www.gamersky.com/z/playbattlegrounds/",
    ]

    def __init__(self):
        super(JueDiQiuSheng, self).__init__()

    def parse(self, response):
        content = response.body.decode("utf-8")
        # print(content)

        selector = Selector(text=content)

        # 获取大分类
        midLSelector = selector.css("div.Mid_L")[0]

        midLtit = midLSelector.css("div.MidLtit")
        bigTitle = midLtit.css("div.tit.t1::text")[0].extract()
        print("大标题是：" + bigTitle)

        # // 攻略合集
        g_l_h_j = midLSelector.css("div.MidLcon.GLHJ")
        g_l_h_j2 = g_l_h_j.css("div.GLHJ-2")

        infoList = []

        infoList += rmbb(g_l_h_j)
        infoList += getOtherKinds(g_l_h_j2)

        for e in infoList:
            name = e["name"]
            url = e["url"]
            picUrl = e["picUrl"]

            yield insertData2DB(name, url, picUrl)


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

    return infoList


# 获取 攻略合集 里面 除过 入门必备 的其他分类
def getOtherKinds(element):
    infoList = []

    for e in element:
        sTitle = e.css("span.GLHJtit")
        name = sTitle.xpath("string(.)").extract()[0]
        print("小标题：\n\t" + name)

        imgliklistElements = e.css("ul.liklist").css("li.line1")
        print("获取 " + name + " 带图片属性：")
        infoList += getElement(imgliklistElements)

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


# 根据 Url 获取 Jid
def getJid(url):
    try:
        start = url.rindex("/")
        end = url.rindex(".")
        newUrl = url[(start + 1):end]
        if newUrl.__contains__("-"):
            newUrl = newUrl[0:newUrl.rindex("-")]
    except:
        newUrl = url
        pass

    return newUrl


# 插入数据到数据库中
def insertData2DB(name, url, pic_url):
    jid = getJid(url)

    item = JuediqiushengItem()
    item['jid'] = jid
    item['name'] = name
    item['url'] = url
    item['picUrl'] = pic_url
    return item
