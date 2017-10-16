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
        # names = selector.xpath('//ul[@id="zl_ul"]/li/a/text()').extract()

        # 获取大分类
        midLSelector = selector.css("div.Mid_L")[0]

        midLtit = midLSelector.css("div.MidLtit")
        bigTitle = midLtit.css("div.tit.t1::text")[0].extract()
        print("大标题是：" + bigTitle)

        # // 攻略合集
        g_l_h_j = midLSelector.css("div.MidLcon.GLHJ")
        g_l_h_j2 = g_l_h_j.css("div.GLHJ-2")

        rmbb(g_l_h_j2)



        # smallTitle = g_l_h_j.css("span.GLHJtit").css("span::text")[0].extract()
        # print("小标题是：" + smallTitle)
        #
        # element = g_l_h_j.css("ul.imgliklist").css("li.img")
        # print("获取 " + smallTitle + " 带图片属性：")

        # getElement(element)


        # item = JuediqiushengItem()
        #
        # item['id'] = '0023133333'
        # item['jid'] = '99999'
        # item['name'] = 'Hello'
        # item['url'] = "http://www.baidu.com"
        #
        # yield item


# //todo

def rmbb(element):
    GLHJtit = element.css("span.GLHJtit")

    name = GLHJtit.css("span::text").extract()[0]
    print("小标题是：" + name)

    imgliklistElements = element.css("ul.imgliklist")
    elements = imgliklistElements.css("li.img")
    print("获取 " + name + " 带图片属性：")
    getElement(elements)

    linkElements = imgliklistElements.css("li.lik").css("div.link")
    print("获取 " + name + " link 属性：")
    getElement(linkElements)


# 获取相关属性
def getElement(element):
    for e in element:
        name = ""
        url = ""
        imgUrl = ""

        try:
            name = e.select("string(.)").extract()[0].strip()
        except:
            pass

        try:
            url = e.css("a::attr(href)").extract()[0]
        except:
            pass

        try:
            imgUrl = e.css("img::attr(src)").extract()[0]
        except:
            pass

        print("\t属性是：\n\t\t" +
              "name:" + name + "\r\n\t\t" +
              "url:" + url + "\r\n\t\t" +
              "imgUrl:" + imgUrl + "\r\n\t\t")

        print("\r")
