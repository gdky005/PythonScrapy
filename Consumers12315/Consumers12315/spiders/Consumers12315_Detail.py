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

    def parse(self, response):

        selector = Selector(response)

        # 换新方式获取

        answerContent = selector.css('div.WordSection1')[0].select("p").select("string(.)").extract()
        names = selector.css("p.MsoNormal > span[style='font-size:16.0pt;font-family:仿宋_GB2312;color:black']::text").extract()
        titleList = []

        currentLineNumber = 0

        titleReplaceState = False
        for line in names:
            if titleReplaceState:
                titleList.append("%d.%s"%(currentLineNumber, line))
                titleReplaceState = False
                continue

            try:
                lineNumber = int(line.split(".")[0])
                currentLineNumber = lineNumber
                titleReplaceState = True
            except:
                titleReplaceState = False

        # for name in titleList:
        #     print(name)


        answer = []

        qIndex = 0
        newAnswer = []

        for t in answerContent:
            if qIndex < len(titleList):

                if t == titleList[qIndex]:

                    # if (i == 0) {
                    # System.out.println("Continue");
                    # qIndex++;
                    # continue;
                    # }

                    if qIndex == 0:
                        qIndex += 1
                        continue

                    newAnswer.append("".join(answer))
                    answer = []
                    qIndex += 1

                else:
                    answer.append(t + "\r\n")

            else:
                answer.append(t + "\r\n")

        newAnswer.append("".join(answer))

        i = 0
        for a in titleList:
            print("问题：" + titleList[i].__str__())
            print("答案：" + newAnswer[i].__str__())
            i += 1

























        # bigTitle = selector.xpath('//div[@class="hd"]/h2/text()').extract()
        #
        # myContent = selector.xpath('//div[@class="WordSection1"]/p[@class="MsoNormal"]/span//text()').extract()
        #
        # # self.getBigTitle(selector)
        # # self.getSmallTitle(selector)
        # # yield from self.insertData2DB(myContent)
        #
        #
        #
        # # self.getBigTitle(selector)
        # # self.getSmallTitle(selector)
        #
        # currentNumber = 0
        #
        # i = 0
        # isTitle = False
        # space = "\r\n\n\t"
        # space1 = "\r\n"
        # content1 = ""
        # text = ""
        # for line in myContent:
        #
        #     if isTitle:
        #         content1 += "^^^^^^^^^^^^^^^^^^^^^^^^^^^^" + space1
        #         content1 += "当前的问题是：" + line + space1
        #         content1 += "^^^^^^^^^^^^^^^^^^^^^^^^^^^^" + space
        #
        #         isTitle = False
        #         continue
        #
        #     if Utils.matchTitle(line):
        #         i += 1
        #         # if i > 10:
        #         #     break
        #
        #             # //把 line 转成成 数字存储起来
        #         lineNumber = int(line.split(".")[0])
        #         # print("下面是 lineNumber：")
        #         # print(lineNumber)
        #
        #         if lineNumber < currentNumber:
        #             content1 += line
        #             continue
        #
        #         currentNumber = lineNumber
        #         print("currentNumber:")
        #         print(currentNumber)
        #
        #         content1 += "______________________" + space1
        #         content1 += line + "---------------" + space1
        #         content1 += "______________________" + space1
        #
        #         isTitle = True
        #         continue
        #
        #     if ~isTitle:
        #         l = line
        #         # for l in line:
        #
        #         if Utils.matchTitle(l):
        #             # content1 += line
        #             content1 += space
        #             continue
        #
        #         content1 += l
        #         text = l
        #
        #         endChar = l[len(l) - 1]
        #         if Utils.isEndChar(endChar):
        #             content1 += space
        # print(content1)








    # 插入单条数据到数据库中
    def insertData2DB(self, myContent):
        i = 0
        isTitle = False
        space = "\r\n\n\t"
        space1 = "\r\n"
        content1 = ""
        text = ""
        # self.singleText(content1, i, isTitle, myContent, space)
        from Consumers12315.items import Consumers12315Item
        item = Consumers12315Item()
        for line in myContent:

            if isTitle:
                content1 += "^^^^^^^^^^^^^^^^^^^^^^^^^^^^" + space1
                content1 += "当前的问题是：" + line + space1
                content1 += "^^^^^^^^^^^^^^^^^^^^^^^^^^^^" + space

                item['question'] = line
                isTitle = False
                continue

            if Utils.matchTitle(line):
                i += 1
                if i > 10:
                    break

                content1 += "______________________" + space1
                content1 += line + "---------------" + space1
                content1 += "______________________" + space1

                item['number'] = line

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
                text = l

                endChar = l[len(l) - 1]
                if Utils.isEndChar(endChar):
                    content1 += space
        print(content1)
        item['answer'] = text
        yield item

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









