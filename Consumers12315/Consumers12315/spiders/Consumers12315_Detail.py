import re

from scrapy import Selector
from scrapy.spiders import Spider
from selenium import webdriver

from Consumers12315 import Utils


class Consumers12315_Detail(Spider):
    name = "Consumers12315_Detail"
    start_urls = [
        # 可以替换这个 ID，目前是健身服务：410b2db796184a6082317c3032b331d2
        "http://www.12315.cn/knowledge/knowledgeView?zlcode=410b2db796184a6082317c3032b331d2",
        # "http://www.12315.cn/knowledge/knowledgeView?zlcode=9eaa794b186548c186ff5ae9ed5e71ae",
    ]

    def __init__(self):
        super(Consumers12315_Detail, self).__init__()
        # self.start_urls = ['http://buluo.qq.com/p/barindex.html?bid=%s' % bid]
        # self.allowed_domain = 'buluo.qq.com'
        self.driver = webdriver.Chrome("/Applications/Google Chrome.app/Contents/MacOS/chromedriver")
        self.driver.set_page_load_timeout(5)  # throw a TimeoutException when thepage load time is more than 5 seconds.

    def parse(self, response):
        self.driver.get(response.url)
        # time.sleep(5)

        # content = self.driver.page_source
        # print("爬取的内容如下：" + content)

        # selector = Selector(text=content)
        selector = Selector(response)

        # bigTitle = selector.xpath('//div[@class="hd"]/h2/text()').extract()


        # self.getBigTitle(selector)
        # self.getSmallTitle(selector)



        myContent = selector.xpath('//div[@class="WordSection1"]/p[@class="MsoNormal"]/span//text()').extract()

        i = 0
        isTitle = False

        space = "\r\n\n\t"
        space1 = "\r\n"
        content1 = ""

        # self.singleText(content1, i, isTitle, myContent, space)

        for line in myContent:

            if isTitle:
                content1 += "^^^^^^^^^^^^^^^^^^^^^^^^^^^^" + space1
                content1 += "当前的问题是：" + line + space1
                content1 += "^^^^^^^^^^^^^^^^^^^^^^^^^^^^" + space

                isTitle = False
                continue

            if Utils.matchTitle(line):
                i += 1
                if i > 10:
                    break

                content1 += "______________________" + space1
                content1 += line + "---------------" + space1
                content1 += "______________________" + space1

                isTitle = True
                continue

            if ~isTitle:
                l = line
                # for l in line:

                if Utils.matchTitle(l):
                    # content1 += line
                    content1 += space
                    continue

                content1 += l
                endChar = l[len(l) - 1]

                if Utils.isEndChar(endChar):
                    content1 += space
        print(content1)






    def singleText(self, content1, i, isTitle, myContent, space):
        for line in myContent:

            if isTitle:
                print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
                print("当前的问题是：" + line)
                print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^")

                isTitle = False
                continue

            if Utils.matchTitle(line):
                i += 1
                if i > 1:
                    break

                print("______________________")
                print(line + "---------------")
                print("______________________")

                isTitle = True
                continue

            if ~isTitle:
                l = line
                # for l in line:

                if Utils.matchTitle(l):
                    # content1 += line
                    content1 += space
                    continue

                content1 += l
                endChar = l[len(l) - 1]

                if Utils.isEndChar(endChar):
                    content1 += space
        print(content1)

    # 获取当前的大标题
    def getBigTitle(self, selector):
        bigTitle = selector.xpath('//div[@class="hd"]/h2/text()').extract()
        print("当前的大标题是： " + bigTitle[0])

    # 获取当前的 所有问题
    def getSmallTitle(self, selector):
        myTile = selector.xpath(
            '//div[@class="WordSection1"]/p[@class="MsoNormal"]/span[@style="font-size:16.0pt;font-family:仿宋_GB2312;color:black"]/text()').extract()
        for t in myTile:
            print("___ " + t)
        print("下面只获取标题：")
        questList = []
        state = False
        for t in myTile:
            if state and not Utils.matchTitle(t) and not t.strip() == "":
                print("_A_ " + t)
                questList.append(t)
                state = False
                continue

            if Utils.matchTitle(t):
                state = True
                continue
        print("当前的总共有：" + len(questList).__str__())









