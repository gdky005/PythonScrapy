url1 = "http://www.gamersky.com/handbook/201706/919363-67.shtml"


def getJid(url):
    start = url.rindex("/")
    end = url.rindex(".")
    newUrl = url[(start + 1):end]
    if newUrl.__contains__("-"):
        newUrl = newUrl[0:newUrl.rindex("-")]
    return newUrl


def getCategoryId(url):
    url = url[0: url.__len__() - 1]
    print(url)

    start = url.rindex("_")
    categoryId = url[(start + 1):url.__len__()]
    if categoryId.__contains__("-"):
        categoryId = categoryId[0:categoryId.rindex("-")]
    return categoryId


#
# # print("Jid=" + getJid(url1))
#
# l1 = [1,2,3]
# l2 = [4,5,6]
#
# l1 += l2
#
#
#
# for a in l1:
#     print(a)


categoryUrl = "http://www.gamersky.com/z/playbattlegrounds/862094_64754/"

print(getCategoryId(categoryUrl))
