import json
import time

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning


def getFile1(url1, header):
    return getFile(url1, header, None, 0)


def getFile(url1, header, proxies1, id):
    try:
        if proxies1 is None:
            res = requests.get(url1, headers=header, timeout=5, verify=False)
        else:
            res = requests.get(url1, headers=header, timeout=5, proxies=proxies1, verify=False)

        if 200 == res.status_code:
            content = res.content.decode("utf-8")

            # print(content)

            url2 = url1[0: len(url1) - 1]

            idStr = str(id)
            id = idStr.zfill(5)
            fileName = id + "_" + url1[url2.rindex("/") + 1: len(url1) - 1]

            print("获取文件内容成功，准备写入到文件中：" + fileName)

            fileObject = open("/Users/WangQing/PycharmProjects/ScrapyPro/ProxyPro/manhuaDetail/" + fileName, 'w+')
            fileObject.write(content + "\n")
            fileObject.close()
            return 1
        else:
            return 0
    except:
        print("超时")
        return 0


def getJson(ipListPath):
    try:
        global text
        f = open(ipListPath)
        data = f.read()
        text = json.loads(data)
        return text
    except:
        pass

    return None


ipListPath1 = "/Users/WangQing/PycharmProjects/ScrapyPro/ProxyPro/ipList_nima.txt"
ipListPath2 = "/Users/WangQing/PycharmProjects/ScrapyPro/ProxyPro/ipList_xici.txt"
ipListPath3 = "/Users/WangQing/PycharmProjects/ScrapyPro/ProxyPro/new_detail_avilable_ip.txt"
json1 = getJson(ipListPath1)
json2 = getJson(ipListPath2)
json3 = getJson(ipListPath3)

jsonList = []

if json3 is not None:
    for obj in json1:
        jsonList.append(obj)
else:
    for obj in json1:
        jsonList.append(obj)

    for obj in json2:
        jsonList.append(obj)

print(jsonList.__len__())


def getStr(data):
    return str(len(data))


jsonListNew = jsonList

page = 2
pageCount = 200
urlSource = "http://zkteam.cc/ManHua/jsonMHAllData?page=" + str(page) + "&pageCount=" + str(pageCount)

res = requests.get(urlSource)
resultList = res.json()['result']

i = 0
for data in resultList:
    # ipIndex = text[random.randint(0, len(text) - 1)]
    # ipIndex = text[i % len(text)]

    headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/4.0 (Linux; Android 5.1.1; Nexus 6 Build/JRO03D) AppleWebKit/536.19 (KHTML, like Gecko) Chrome/17.0.1025.166  Safari/532.19'}

    url = data['mhUrl']
    id = data['id']
    print(url)

    # 禁用安全请求警告
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    print("可用的 ip 列表是：" + getStr(jsonListNew) + "/" + getStr(jsonList))

    ip = jsonList[i % len(jsonListNew)]
    i = i + 1
    scheme = ip["type"]
    domain = ip["url"]

    print(domain)

    proxies = {scheme: domain}
    code = getFile(url, headers, proxies, id)

    if 1 == code:
        continue
    else:
        jsonListNew.remove(ip)

        for ip in jsonListNew:
            scheme = ip["type"]
            domain = ip["url"]

            print(domain)

            proxies = {scheme: domain}
            code = getFile(url, headers, proxies, id)

            if 1 == code:
                break
            else:
                jsonListNew.remove(ip)

            print("可用的 ip 列表是：" + getStr(jsonListNew) + "/" + getStr(jsonList))
    print("可用的 ip 列表是：" + getStr(jsonListNew) + "/" + getStr(jsonList))
print("可用的 ip 列表是：" + getStr(jsonListNew) + "/" + getStr(jsonList))

fileName = "new_detail_avilable_ip.txt"
fileObject = open("/Users/WangQing/PycharmProjects/ScrapyPro/ProxyPro/" + fileName, 'w+')
fileObject.write(str(jsonListNew).replace("'", "\"") + "\n")
fileObject.close()
