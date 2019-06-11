from scrapy import Selector
from scrapy.spiders import Spider
import re


def getPic(selector):
    # 获取图片
    picList = selector.css("a").css("p::attr('style')").extract()
    for pic in picList:
        pic = pic.replace("background-image: url(", "")
        pic = pic.replace(")", "")

        print("pic: " + pic)
        return pic


def getNewPageName(selector):
    # 获取最新一集
    newList = selector.css("p").css("a::text").extract()
    for new in newList:
        print("最新章节是: " + new)
        return new


def getTitle(selector):
    # 获取标题
    titleList = selector.css("h2").css("a").css("a::attr('title')").extract()
    for title in titleList:
        print("title: " + title)
        return title


class ManHua(Spider):
    name = "ManHua"
    start_urls = [
        "https://www.tohomh123.com/zhegedashutailengao/83.html",
        # "https://www.tohomh123.com/zhegedashutailengao/",
        # "https://www.tohomh123.com/f-1------updatetime--1.html",
        # "https://www.tohomh123.com/f-1-1-----hits--1.html",
        # "https://www.tohomh123.com",
        # "http://www.gamersky.com/z/playbattlegrounds/",
    ]

    def __init__(self):
        super(ManHua, self).__init__()

    def parse(self, response):
        content = response.body.decode("utf-8")
        # print(content)

        selector = Selector(text=content)

        chapterItem = selector.css("div.mCustomScrollBox").css("li")

        for chapter in chapterItem:

            pic = chapter.css("a::attr('href')").extract()[0]
            picTitle = chapter.css("a::text").extract()[0]
            picTitle_p = chapter.css("a").css("span::text").extract()[0]

            print("\n")
            print("pic->" + pic +
                  ",\npicTitle->" + picTitle +
                  ",\npicTitle_p->" + picTitle_p)

        chapterItem = selector.css("script::text")[4].extract()
        pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')  # 匹配模式
        pic = chapterItem.split(";")[9]
        pic = re.findall(pattern, pic)[0]
        pic = pic[0:len(pic)-1]

        count = chapterItem.split(";")[5]
        count = count[count.index("= "):len(count)]

        print("首张图片地址是：" + pic + ", 总共：" + count + " P")


        # title = selector.css("div.info").css("h1::text").extract()[0]
        # author = selector.css("div.info").css("p::text").extract()[0]
        # state = selector.css("p.tip").css("span.block")[0].css("span::text").extract()[1]
        # time = selector.css("p.tip").css("span.block")[2].css("span::text").extract()[0]
        # detail = selector.css("p.content").css("p::text").extract()[0]
        #
        # category = selector.css("p.tip").css("span.block")[1].css("a::text").extract()
        # tag = selector.css("p.tip").css("span.block")[3].css("a::text").extract()
        #
        # print("\n")
        # print("pic->" + pic +
        #       ",\ntitle->" + title +
        #       ",\nauthor->" + author +
        #       ",\nstate->" + state +
        #       ",\ntime->" + time +
        #       ",\ndetail->" + detail +
        #       ",\ncategory->" + category.__str__() +
        #       ",\ntag->" + tag.__str__()
        #       )
        #
        # sort = selector.css("div.left-bar")[0].css("div.detail-list-title").css("a::text").extract()[0] # 倒序
        #
        # # todo 这里需要去重处理
        # chapterItem = selector.css("div.left-bar")[0].css("ul.view-win-list.detail-list-select").css("li")
        #
        # for chapter in chapterItem:
        #     chapterName = chapter.css("a::text").extract()[0]
        #     chapterName_p = chapter.css("a").css("span::text").extract()[0]
        #     chapterUrl = "https://www.tohomh123.com" + chapter.css("a::attr(href)").extract()[0]
        #
        #     print("\n")
        #     print("chapterName->" + chapterName +
        #       ",\nchapterName_p->" + chapterName_p +
        #       ",\nchapterUrl->" + chapterUrl
        #       )


# # 获取文章中的主要内容
# def getContent(elements):
#     subString = ""
#     for i in range(len(elements)):
#
#         if i >= (len(elements) - 2):
#             break
#
#         text = elements[i].extract()
#         if "data-src" in text:
#             text = text.replace("src=\"http://image.gamersky.com/webimg13/zhuanti/common/blank.png\" data-", "")
#         subString += text
#         subString += "\n"
#     return subString

# 插入数据到数据库中
def insertData2DB(mid, url, name):
    from ManHua.items import ManHuaItem
    item = ManHuaItem()
    item['mid'] = mid
    item['url'] = url
    item['name'] = name
    return item