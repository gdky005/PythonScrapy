from scrapy import Selector
from scrapy.spiders import Spider
from selenium import webdriver


class JueDiQiuSheng(Spider):
    name = "JueDiQiuSheng"
    start_urls = [
        "http://www.gamersky.com/z/playbattlegrounds/",
    ]

    def __init__(self):
        super(JueDiQiuSheng, self).__init__()
        # self.start_urls = ['http://buluo.qq.com/p/barindex.html?bid=%s' % bid]
        # self.allowed_domain = 'buluo.qq.com'
        # self.driver = webdriver.Chrome("/Applications/Google Chrome.app/Contents/MacOS/chromedriver")
        # self.driver.set_page_load_timeout(5)  # throw a TimeoutException when thepage load time is more than 5 seconds.

    def parse(self, response):
        print(response.body.decode('utf-8'))

        # self.driver.get(response.url)
        # content = self.driver.page_source
        # print("爬取的内容如下：" + content)
        # selector = Selector(text=content)
        # # name = selector.xpath('//span[@id="headerName"]/text()').extract()
        # names = selector.xpath('//ul[@id="zl_ul"]/li/a/text()').extract()
        # ids = selector.xpath('//ul[@id="zl_ul"]/li/a/@onclick').extract()
        #
        # # 已经获取到需要的名称
        # print("我需要的名称：" + names.__str__())
