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
        # "http://127.0.0.1:8081/chaojiweixin",
        "https://www.tohomh123.com/zhenhunjie/",
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

        pic = selector.css("div.cover").css("img::attr('src')").extract()[0] # 'https://mh1.zhengdongwuye.cn/pic/manhua/images/688714201872.jpg'
        title = selector.css("div.info").css("h1::text").extract()[0] #'镇魂街'
        remind = selector.css("div.info").css("em.remind").css("em::text").extract()[0] # 每月1号,11号,21号上传新章节或于隔日上午更新（注意这个隔日）

        author = selector.css("div.info").css("p::text").extract()[0] #'作者：许辰'
        author = author[author.index("：")+1:]

        state = selector.css("p.tip").css("span.block")[0].css("span::text").extract()[1] #'连载中'
        stateId = getHashCode(state)

        time = selector.css("p.tip").css("span.block")[2].css("span::text").extract()[0] #'更新时间：2019-06-21'
        time = time[time.index("：") + 1:]

        detail = selector.css("p.content").css("p::text").extract()[0] #'                                镇魂街，此乃吸纳亡灵镇压恶灵之地。这是一个人灵共存的世界，但不是每个人都能进入镇魂街，只有拥有守护灵的寄灵人才可进入。夏铃原本是一名普通的大学实习生，但一次偶然导致她的人生从此不再平凡......没有主角不主角，谁都是主角。反正，镇魂街的设定也是一个乱世了，乱世出英雄。每个人有不同喜欢的角色，都是很有个性的角色，就可以了。在这个充满恶灵的世界，你能与你的守护灵携手生存下去吗？'
        detail = detail.strip()

        category = selector.css("p.tip").css("span.block")[1].css("a::text").extract() # <class 'list'>: ['热血']
        categoryIdList = []
        for item in category:
            categoryId = getHashCode(item)
            print(item + "->" + str(categoryId))
            categoryIdList.append(categoryId)

        tag = selector.css("p.tip").css("span.block")[3].css("a::text").extract() # <class 'list'>: ['镇魂', '恶灵', '守护']

        url = response.url.replace("http://127.0.0.1:8081", "https://www.tohomh123.com")

        if url[len(url) - 1] == "/":
            urlMid = url[url.index("com/") + 4:url.rindex("/")]  # 'zhenhunjie'
            # urlMid = url[url.index("com/") + 4:url.rindex("/")] #'zhenhunjie'
        else:
            urlMid = url[url.index("com/") + 4:]  # 'zhenhunjie'


        print("当前计算的 url 是：" + urlMid)
        mid = getHashCode(urlMid)
        print("当前计算 " + urlMid + " 的 mid 是：" + str(mid))

        print("\n")
        print("pic->" + pic +
              ",\ntitle->" + title +
              ",\nmid->" + str(mid) +
              ",\nauthor->" + author +
              ",\nstate->" + state +
              ",\nstateId->" + str(stateId) +
              ",\nremind->" + remind +
              ",\ntime->" + time +
              ",\ndetail->" + detail +
              ",\nurl->" + url +
              ",\ncategory->" + category.__str__() +
              ",\ncategoryIdList->" + categoryIdList.__str__() +
              ",\ntag->" + str(tag)
              )

        yield insertData2DB(mid, title, author, pic, state, stateId, remind, time, detail, url,
                            getStringForList(category), getStringForList(categoryIdList), getStringForList(tag))

        # sort = selector.css("div.left-bar")[0].css("div.detail-list-title").css("a::text").extract()[0] # 倒序
        #
        # chapterItem = selector.css("div.left-bar")[0].css("ul.view-win-list.detail-list-select")[1].css("li")
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


# 插入数据到数据库中
def insertData2DB(mid, name, author, picUrl, state, stateId, remind, time, detail, url, category, categoryIdList, tag):
    from ManHua.items import ManHuaItem
    item = ManHuaItem()
    item['mid'] = mid
    item['name'] = name
    item['author'] = author
    item['picUrl'] = picUrl
    item['state'] = state
    item['stateId'] = stateId
    item['remind'] = remind
    item['time'] = time
    item['detail'] = detail
    item['url'] = url
    item['category'] = category
    item['categoryIdList'] = categoryIdList
    item['tag'] = tag
    return item


def getStringForList(items):
    data = ''
    for item in items:
        data += (str(item) + ",")
    return data[0:len(data)-1]
