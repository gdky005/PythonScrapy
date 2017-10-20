import requests
import time
from parsel import SelectorList
from scrapy import Selector, Request
from scrapy.spiders import Spider
from selenium import webdriver

from JueDiQiuSheng.items import JDQSItem

from JueDiQiuSheng import Utils
from JueDiQiuSheng import Constant_JDQS


class JueDiQiuSheng(Spider):
    name = "JueDiQiuSheng"
    start_urls = [
        "http://www.gamersky.com/z/playbattlegrounds/news/",
    ]

    def __init__(self):
        super(JueDiQiuSheng, self).__init__()
        self.driver = webdriver.Chrome("/Users/WangQing/opt/chrome/chromedriver")
        self.driver.maximize_window()

    def parse(self, response):
        # content = response.body.decode("utf-8")
        # print(content)

        # 表示资讯
        categoryId = "10000"

        currentUrl = response.url
        content = self.driverScroll(currentUrl)

        self.insertData(content, categoryId)

        for item in Constant_JDQS.global_item_list:
            yield item

    def insertData(self, content, categoryId):
        selector = Selector(text=content)
        itemList = selector.css("ul.titlist").css("li.li1")
        for item in itemList:
            picUrl = ""

            artifactName = item.css("a::attr(title)")[0].extract()
            artifactDate = item.css("div.time::text")[0].extract()
            artifactSourceUrl = item.css("a::attr(href)")[0].extract()

            # print("当前的分类 id 是：" + categoryId)
            print("当前的分类 name 是：" + artifactName)
            print("当前的分类 href 是：" + artifactDate)
            print("当前的分类 date 是：" + artifactSourceUrl)

            data = insertData2DB(artifactName, artifactDate, artifactSourceUrl, picUrl, categoryId)
            Constant_JDQS.global_item_list.append(data)

        nextPage = selector.css("a.p1.nexe::text")[0].extract()

        nextElement = self.driver.find_element_by_css_selector("a.p1.nexe")

        if nextPage == "下一页" and nextElement.is_displayed():
            # 点击下一页
            nextElement.click()

            time.sleep(2)
            content = self.driver.page_source

            self.insertData(content, categoryId)
        else:
            self.driver.quit()

    # 模拟浏览器滚动
    def driverScroll(self, currentUrl):
        self.driver.get(currentUrl)
        try:
            i = 0
            while i < 10:
                self.driver.execute_script("window.scrollBy(0, 200)")
                time.sleep(0.3)
                i += 1
        except Exception as e:
            pass
        content = self.driver.page_source
        return content


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
