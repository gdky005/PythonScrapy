import requests
import time
from scrapy import Selector, Request
from scrapy.spiders import Spider
from selenium import webdriver
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher

from JueDiQiuSheng.items import JDQSItem

from JueDiQiuSheng import Utils, JDQSDriverUtils, JDQSRMBBUtils


class JueDiQiuSheng(Spider):
    name = "JueDiQiuSheng"
    start_urls = [
        # Bug问题
        # "http://www.gamersky.com/z/playbattlegrounds/862094_34425/",
        # 新手必备
        # "http://www.gamersky.com/z/playbattlegrounds/",
        # 武器和装备
        "http://www.gamersky.com/z/playbattlegrounds/862094_6792/"
    ]

    def __init__(self):
        super(JueDiQiuSheng, self).__init__()
        self.driver = webdriver.Chrome("/Users/WangQing/opt/chrome/chromedriver")
        self.driver.maximize_window()
        # dispatcher.connect(self.spider_closed, signals.spider_closed)
        print("当前运行时间是：" + Utils.getCollectionTime())

    def start_requests(self):
        params = {'pageCount': '100'}
        # 分类接口
        content = requests.get('http://zkteam.cc/JueDiQiuSheng/categoryJson', params)
        json = content.json()
        resultJson = json["result"]

        for result in resultJson:
            newUrl = result["categoryUrl"]
            print("当前抓取的 Url 是：" + newUrl)
            yield Request(newUrl)

    def parse(self, response):
        content = response.body.decode("utf-8")
        # print(content)

        currentUrl = response.url

        # 入门必备的 category_id 是：10001
        if currentUrl == "http://www.gamersky.com/z/playbattlegrounds/":
            infoList = []
            JDQSRMBBUtils.queryRMBBData(content, infoList)

            for e in infoList:
                artifactName = e["name"]
                url = e["url"]
                picUrl = e["picUrl"]
                yield insertItemData2DB(artifactName, Utils.getCollectionTime(), url, picUrl, 10001)
            return

        content = JDQSDriverUtils.driverScroll(self.driver, currentUrl)

        global_item_list = []

        JDQSDriverUtils.insertData(self.driver, content, Utils.getCategoryId(currentUrl), global_item_list)

        for item in global_item_list:
            yield item

        # time.sleep(2)
        # self.driver.close()

    def close(self, reason):
        self.driver.close()
        print("当前结束时间是：" + Utils.getCollectionTime())


# 插入数据到数据库中
def insertItemData2DB(artifactName, artifactDate, artifactSourceUrl, picUrl, categoryId):
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
