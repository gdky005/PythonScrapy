# 入门必备
from scrapy import Selector

from JueDiQiuSheng import Utils


def queryRMBBData(content, infoList):
    selector = Selector(text=content)
    # 获取大分类
    midLSelector = selector.css("div.Mid_L")[0]
    g_l_h_j = midLSelector.css("div.MidLcon.GLHJ")
    rmbb(g_l_h_j, infoList)


def rmbb(element, infoList):
    GLHJtit = element.css("span.GLHJtit")

    name = GLHJtit.css("span::text").extract()[0]
    print("小标题是：" + name)

    imgliklistElements = element.css("ul.imgliklist")
    elements = imgliklistElements.css("li.img")
    print("获取 " + name + " 带图片属性：")
    getElement(elements, infoList)

    linkElements = imgliklistElements.css("li.lik").css("div.link")
    print("获取 " + name + " link 属性：")
    getElement(linkElements, infoList)

    category_url = GLHJtit.css("a::attr('href')").extract()[0]
    addCategoryData(infoList, name, category_url)

    return infoList


# 添加分类属性
def addCategoryData(infoList, name, category_url):
    category_id = Utils.getCategoryId(category_url)
    print("获取 " + name + " category_id：" + category_id)
    for item in infoList:
        item["category_id"] = category_id
        item["category_name"] = name


# 获取相关属性
def getElement(element, infoList):
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
