import time

from scrapy import Selector

from JueDiQiuSheng import Utils
from JueDiQiuSheng.items import JDQSTJItem


def insertData(driver, content, categoryId, global_item_list):
    selector = Selector(text=content)
    itemList = selector.css("ul.titlist").css("li.li1")
    for item in itemList:
        picUrl = ""

        artifactName = item.css("a::attr(title)")[0].extract()
        artifactDate = item.css("div.time::text")[0].extract()
        artifactSourceUrl = item.css("a::attr(href)")[0].extract()

        print("当前的分类 id 是：")
        print(categoryId)
        print("当前的分类 name 是：" + artifactName)
        print("当前的分类 href 是：" + artifactSourceUrl)
        print("当前的分类 date 是：" + artifactDate)

        data = insertItemData2DB(artifactName, artifactDate, artifactSourceUrl, picUrl, categoryId)
        global_item_list.append(data)

    nextTextSelector = selector.css("a.p1.nexe::text")

    if nextTextSelector.__len__() > 0:
        nextPage = nextTextSelector[0].extract()
        nextElement = driver.find_element_by_css_selector("a.p1.nexe")
        if nextPage == "下一页" and nextElement.is_displayed():
            # 点击下一页
            nextElement.click()

            time.sleep(2)
            content = driver.page_source

            insertData(driver, content, categoryId, global_item_list)
        # else:
            # driver.quit()
    # else:
        # driver.quit()

# 模拟浏览器滚动
def driverScroll(driver, currentUrl):
    driver.get(currentUrl)
    try:
        i = 0
        while i < 10:
            driver.execute_script("window.scrollBy(0, 200)")
            time.sleep(0.3)
            i += 1
    except Exception as e:
        pass
    content = driver.page_source
    return content


# 插入数据到数据库中
def insertItemData2DB(artifactName, artifactDate, artifactSourceUrl, picUrl, categoryId):
    jid = Utils.getJid(artifactSourceUrl)

    url = '<p><a href="http://www.zkteam.cc/JueDiQiuSheng/detail.html?jid=' + jid + \
          '">http://www.zkteam.cc/JueDiQiuSheng/detail.html?jid=' + jid + "</a></p>"

    item = JDQSTJItem()
    item['jid'] = jid
    item['tjName'] = artifactName
    item['tjDate'] = artifactDate
    item['tjSourceUrl'] = artifactSourceUrl
    item['tjUrl'] = url
    item['tjPicUrl'] = picUrl
    item['categoryId'] = categoryId

    return item
