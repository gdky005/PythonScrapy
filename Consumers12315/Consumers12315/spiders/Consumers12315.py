from scrapy import Selector
from scrapy.spiders import Spider
from selenium import webdriver

from Consumers12315 import Utils


class Consumers12315(Spider):
    name = "Consumers12315"
    start_urls = [
        "http://www.12315.cn/knowledge/rights_knowledge",
    ]

    def __init__(self):
        super(Consumers12315, self).__init__()
        # self.start_urls = ['http://buluo.qq.com/p/barindex.html?bid=%s' % bid]
        # self.allowed_domain = 'buluo.qq.com'
        self.driver = webdriver.Chrome("/Applications/Google Chrome.app/Contents/MacOS/chromedriver")
        self.driver.set_page_load_timeout(5)  # throw a TimeoutException when thepage load time is more than 5 seconds.

    def parse(self, response):
        self.driver.get(response.url)
        # time.sleep(5)

        content = self.driver.page_source
        # print("爬取的内容如下：" + content)

        selector = Selector(text=content)
        # name = selector.xpath('//span[@id="headerName"]/text()').extract()
        names = selector.xpath('//ul[@id="zl_ul"]/li/a/text()').extract()
        ids = selector.xpath('//ul[@id="zl_ul"]/li/a/@onclick').extract()

        # 已经获取到需要的名称
        print("我需要的名称：" + names.__str__())
        print("我需要的原始ID：" + ids.__str__())

        startStr = "('"
        endStr = "')"

        for index, id in enumerate(ids):
            name = names[index]

            currentId = Utils.sliptStr(id, startStr, endStr)
            print("处理后的ID：" + currentId + ", 名称是：\t\t\t" + name + ", 对应的访问地址是："
                  + "http://www.12315.cn/knowledge/knowledgeView?zlcode=" + currentId)





