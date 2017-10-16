url1 = "http://www.gamersky.com/handbook/201706/919363-67.shtml"


def getJid(url):
    start = url.rindex("/")
    end = url.rindex(".")
    newUrl = url[(start + 1):end]
    if newUrl.__contains__("-"):
        newUrl = newUrl[0:newUrl.rindex("-")]
    return newUrl


# print("Jid=" + getJid(url1))

l1 = [1,2,3]
l2 = [4,5,6]

l1 += l2



for a in l1:
    print(a)
