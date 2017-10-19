# 获取当前的时间
def getCollectionTime():
    import datetime
    now = datetime.datetime.now()
    return now.strftime('%Y-%m-%d %H:%M:%S')


# 通过 Url 获得 jid
def getJid(url):
    start = url.rindex("/")
    end = url.rindex(".")
    newUrl = url[(start + 1):end]
    if newUrl.__contains__("-"):
        newUrl = newUrl[0:newUrl.rindex("-")]
    return newUrl


# 通过 Url 获得 categoryId
def getCategoryId(url):
    url = url[0: len(url) - 1]

    start = url.rindex("_")
    categoryId = url[(start + 1):url.__len__()]
    if categoryId.__contains__("-"):
        categoryId = categoryId[0:categoryId.rindex("-")]
    return categoryId
