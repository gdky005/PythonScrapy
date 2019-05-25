import requests
import time
from scrapy import Selector, Request
from scrapy.spiders import Spider
from selenium import webdriver

from JueDiQiuSheng import Utils


class JDQSPicUrl(Spider):
    name = "JueDiQiuSheng"
    start_urls = [
        # 图库分类接口
        # "http://www.zkteam.cc/JueDiQiuSheng/picCateogyJson",
        # "http://pic.gamersky.com/content/201709/954151.shtml",
        # "http://pic.gamersky.com/content/201707/933756.shtml",
        "http://pic.gamersky.com/content/201705/901183.shtml",
        # "http://pic.gamersky.com/content/201705/901185.shtml",
    ]

    def __init__(self):
        super(JDQSPicUrl, self).__init__()
        # http://blog.csdn.net/cz9025/article/details/70160273

        options = webdriver.ChromeOptions()
        options.add_argument('lang=zh_CN.UTF-8')
        options.add_argument('start-maximized')

        self.driver = webdriver.Chrome("/Users/WangQing/opt/chrome/chromedriver", chrome_options=options)
        # self.driver.maximize_window()

    def start_requests(self):
        params = {'pageCount': '100'}
        # 图库分类接口
        content = requests.get('http://zkteam.cc/JueDiQiuSheng/picCategoryJson', params)
        json = content.json()
        resultJson = json["result"]

        for result in resultJson:
            newUrl = result["picCategoryUrl"]
            print("当前抓取的 Url 是：" + newUrl)
            yield Request(newUrl)

    def parse(self, response):
        # content = response.body.decode("utf-8")
        # print(content)

        currentUrl = response.url
        content = self.dirverScroll(currentUrl)

        selector = Selector(text=content)
        # # 获取大分类
        contSelector = selector.css("div.cont")

        print("当前的 Url 是：" + currentUrl)
        for i in range(len(contSelector)):
            contItem = contSelector[i]
            picUrl = contItem.css("div.img").css("img::attr(src)")[0].extract()
            picUrl = picUrl.replace("_tiny.jpg", ".jpg")

            picName = contItem.css("div.con").css("span::text")[0].extract()

            print("picUrl-> " + picUrl + ", picName-> " + picName)
            print("当前 Count:")
            print(i + 1)

            yield insertData2DB(Utils.getJid(currentUrl), picName, picUrl)

    # 模拟浏览器滚动
    def dirverScroll(self, currentUrl):
        self.driver.get(currentUrl)
        try:
            i = 0
            while i < 10:
                self.driver.execute_script("window.scrollBy(0, 200)")
                time.sleep(1)
                i += 1
        except Exception as e:
            pass
        content = self.driver.page_source
        return content

    def close(self, reason):
        self.driver.close()


# 插入数据到数据库中
def insertData2DB(picCategoryId_id, picName, picUrl):
    jid = Utils.getJid(picUrl)

    picZKUrl = '<p><a href="' + picUrl + '">' + picUrl + '</a></p>'
    picTinyUrl = picUrl.replace(".jpg", "_tiny.jpg")
    picSmallUrl = picUrl.replace(".jpg", "_small.jpg")

    from JueDiQiuSheng.items import JDQSDPicUrlItem
    item = JDQSDPicUrlItem()

    item['picId'] = jid
    item['picUrl'] = picUrl
    item['picTinyUrl'] = picTinyUrl
    item['picSmallUrl'] = picSmallUrl
    item['picZKUrl'] = picZKUrl
    item['picName'] = picName
    item['picCategoryId_id'] = picCategoryId_id
    item['picCollection'] = Utils.getCollectionTime()

    return item
