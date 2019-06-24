import requests
import json
from scrapy import Selector
from scrapy.spiders import Spider

from Utils import getHashCode


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
        # "https://www.tohomh123.com/zhenhunjie/",
        "http://127.0.0.1:8081/1-2000/00001_chaojiweixin",
        # "https://www.tohomh123.com/f-1------updatetime--1.html",
        # "https://www.tohomh123.com/f-1-1-----hits--1.html",
        # "https://www.tohomh123.com",
        # "http://www.gamersky.com/z/playbattlegrounds/",
    ]

    def start_requests(self):

        page = 6
        # pageCount = 2
        pageCount = 2000
        urlSource = "http://zkteam.cc/ManHua/jsonMHAllData?page=" + str(page) + "&pageCount=" + str(pageCount)

        res = requests.get(urlSource)
        resultList = res.json()['result']

        start = (page - 1) * pageCount
        if start <= 0:
            start = 1
        end = page * pageCount

        if end < 2000:
            end = 2000

        dir = str(start) + "-" + str(end)

        i = 0
        for data in resultList:
            i = i+1

            url = data['mhUrl']
            id = data['id']
            idStr = str(id)
            id = idStr.zfill(5)

            fileName = url[url.rindex("com/") + 4: len(url) - 1]
            baseUrl = "http://127.0.0.1:8081/" + dir + "/" + id + "_" + fileName
            print(baseUrl)
            yield self.make_requests_from_url(baseUrl)

    def __init__(self):
        super(ManHua, self).__init__()

    def parse(self, response):
        content = response.body.decode("utf-8")
        # print(content)

        selector = Selector(text=content)

        pic = selector.css("div.cover").css("img::attr('src')").extract()[0]
        title = selector.css("div.info").css("h1::text").extract()[0]
        author = selector.css("div.info").css("p::text").extract()[0]
        state = selector.css("p.tip").css("span.block")[0].css("span::text").extract()[1]
        time = selector.css("p.tip").css("span.block")[2].css("span::text").extract()[0]
        detail = selector.css("p.content").css("p::text").extract()[0]

        category = selector.css("p.tip").css("span.block")[1].css("a::text").extract()
        tag = selector.css("p.tip").css("span.block")[3].css("a::text").extract()

        url = response.url
        # url = url[url.index("com/") + 4:url.rindex("/")]
        url = url[url.index("_") + 1:]

        print("当前计算的 url 是：" + url)
        mid = getHashCode(url)

        sort = selector.css("div.left-bar")[0].css("div.detail-list-title").css("a::text").extract()[0] # 倒序

        chapterItem = selector.css("div.left-bar")[0].css("ul.view-win-list.detail-list-select")[1].css("li")

        data_json = []
        for chapter in chapterItem:
            chapterName = chapter.css("a::text").extract()[0]
            chapterName_p = chapter.css("a").css("span::text").extract()[0]
            chapterUrl = chapter.css("a::attr(href)").extract()[0]

            chapterId = chapterUrl[chapterUrl.rindex("/") + 1: chapterUrl.rindex(".")]
            chapterId = chapterId.zfill(3)
            chapterId = str(mid) + chapterId

            chapterUrl = "https://www.tohomh123.com" + chapterUrl

            count = chapterName_p[chapterName_p.index("（") + 1:chapterName_p.index("P")]

            print("\n")
            print("chapterName->" + chapterName +
                  ",\nchapterName_p->" + chapterName_p +
                  ",\nchapterUrl->" + chapterUrl +
                  ",\nmid->" + str(mid)
                  )
            # yield insertData2DB(mid, chapterName, chapterUrl, chapterName_p, count, chapterId)

            data_json.append({
                "name": chapterName,
                "pCount": chapterName_p,
                "url": chapterUrl})

        url = 'http://zkteam.cc/ManHua/setJsonMHChapterData'
        # url = 'http://127.0.0.1:8001/ManHua/setJsonMHChapterData'
        # data_json = {'name': 'cuiyongyuan', 'job': 'hero'}
        # [{
        #     "name": "01 第一话  百鬼夜行 2010-02-03",
        #     "pCount": "（26P）",
        #     "url": "https://www.tohomh123.com/zhenhunjie/1.html"
        # }, {
        #     "name": "02 第二话  火将军 2010-02-18",
        #     "pCount": "（17P）",
        #     "url": "https://www.tohomh123.com/zhenhunjie/2.html"
        # },
        #     {
        #         "name": "第三话 地狱道 内容预告 2010-03-17",
        #         "pCount": "（10P）",
        #         "url": "https://www.tohomh123.com/zhenhunjie/3.html"
        #     }
        # ]

        data_json = json.dumps(data_json)
        resp = requests.post(url, data_json)

        if resp.status_code == 200:
            print("请求成功")
        else:
            print("访问失败")


# 插入数据到数据库中
def insertData2DB(mid, name, url, pCount, count, pid):
    from ManHua.items import ManHuaItem
    item = ManHuaItem()
    item['mid'] = mid
    item['name'] = name
    item['url'] = url
    item['pCount'] = pCount
    item['count'] = count
    item['pid'] = pid
    return item


def getStringForList(items):
    data = ''
    for item in items:
        data += (item + ",")
    return data[0:len(data)-1]
