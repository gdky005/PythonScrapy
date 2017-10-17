from parsel import SelectorList
from scrapy import Selector
from scrapy.spiders import Spider
from selenium import webdriver

from JueDiQiuSheng.items import JuediqiushengItem


class JueDiQiuShengDetail(Spider):
    name = "JueDiQiuShengDetail"
    start_urls = [
        "http://www.gamersky.com/handbook/201705/906915.shtml",
    ]

    def __init__(self):
        super(JueDiQiuShengDetail, self).__init__()

    def parse(self, response):
        content = response.body.decode("utf-8")
        # print(content)

        subString = ""

        selector = Selector(text=content)

        word = selector.css("div.Mid2L_tit")
        articleName = word.css("h1::text")[0].extract()
        articleAuthor = word.css("div.detail::text")[0].extract().strip()

        print("文章名称：\r\n\t" + articleName)
        print("文章作者：\r\n\t" + articleAuthor)
        print("\r\n\t下面是正文：\r\n\t")

        subString += "<h1><p align=\"center\">" + articleName + "</p></h1>\r\n"
        subString += "<h5><p align=\"right\">" + articleAuthor + "</p></h5>"

        # // 以下
        # 获取了总页数地址
        # Elements
        # pageElements = document.select("div.page_css");
        # Elements
        # elements1 = pageElements.select("a");

        # pageElements = selector.css("div.page_css")
        #
        # elements = pageElements.select("a");

        wordDetail = selector.css("div.Mid2L_con")
        elements = wordDetail.xpath("p")

        subString += getContent(elements)

        print(subString)


# 获取文章中的主要内容
def getContent(elements):
    subString = ""
    for i in range(len(elements)):

        if i >= (len(elements) - 2):
            break

        text = elements[i].extract()
        if "data-src" in text:
            text = text.replace("src=\"http://image.gamersky.com/webimg13/zhuanti/common/blank.png\" data-", "")
        subString += text
        subString += "\n"
    return subString


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
    category_id = getCategoryId(category_url)
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


# 根据 Url 获取 Jid
def getJid(url):
    try:
        start = url.rindex("/")
        end = url.rindex(".")
        newUrl = url[(start + 1):end]
        if newUrl.__contains__("-"):
            newUrl = newUrl[0:newUrl.rindex("-")]
    except:
        newUrl = url
        pass

    return newUrl


# 获取对应的 category_id
def getCategoryId(url):
    url = url[0: url.__len__() - 1]
    print(url)

    start = url.rindex("_")
    categoryId = url[(start + 1):url.__len__()]
    if categoryId.__contains__("-"):
        categoryId = categoryId[0:categoryId.rindex("-")]
    return categoryId


# 插入数据到数据库中
def insertData2DB(name, url, pic_url, category_id, category_name):
    jid = getJid(url)

    item = JuediqiushengItem()
    item['jid'] = jid
    item['name'] = name
    item['url'] = url
    item['picUrl'] = pic_url
    item['categoryId'] = category_id
    item['categoryName'] = category_name

    return item
