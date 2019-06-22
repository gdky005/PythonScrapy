import json
import time

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning


def getFile1(url1, header):
    return getFile(url1, header, None)


def getFile(url1, header, proxies1):
    try:
        if proxies1 is None:
            res = requests.get(url1, headers=header, verify=False)
        else:
            res = requests.get(url1, headers=header, timeout=5, proxies=proxies1, verify=False)

        if 200 == res.status_code:
            content = res.content.decode("utf-8")

            # print(content)

            fileName = url1[url1.rindex("/") + 1:]

            print("获取文件内容成功，准备写入到文件中：" + fileName)

            fileObject = open("/Users/WangQing/PycharmProjects/ScrapyPro/ProxyPro/manhua/" + fileName, 'w+')
            fileObject.write(content + "\n")
            fileObject.close()
            return 1
        else:
            return 0
    except:
        print("超时")
        return 0


def getJson(ipListPath):
    global text
    f = open(ipListPath)
    data = f.read()
    text = json.loads(data)
    return text


ipListPath1 = "/Users/WangQing/PycharmProjects/ScrapyPro/ProxyPro/ipList_nima.txt"
ipListPath2 = "/Users/WangQing/PycharmProjects/ScrapyPro/ProxyPro/ipList_xici.txt"
ipListPath3 = "/Users/WangQing/PycharmProjects/ScrapyPro/ProxyPro/manhua/new_avilable_ip.txt"
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
for i in range(301, 376):
    # ipIndex = text[random.randint(0, len(text) - 1)]
    ipIndex = text[i % len(text)]

    headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166  Safari/535.19'}

    print(i)
    url = "https://www.tohomh123.com/f-1------updatetime--" + str(i) + ".html"
    # url = "http://httpbin.org/get"
    print(url)

    # 禁用安全请求警告
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    # getFile1(url, headers)

    print("可用的 ip 列表是：" + getStr(jsonListNew) + "/" + getStr(jsonList))

    # for ip in jsonList:
    #     scheme = ip["type"]
    #     domain = ip["url"]
    #
    #     print(domain)
    #
    #     proxies = {scheme: domain}
    #     code = getFile(url, headers, proxies)
    #
    #     if 1 == code:
    #         break
    #     else:
    #         jsonListNew.remove(ip)

    ip = jsonList[i % len(jsonList)]
    scheme = ip["type"]
    domain = ip["url"]

    print(domain)

    proxies = {scheme: domain}
    code = getFile(url, headers, proxies)

    if 1 == code:
        continue
    else:
        jsonListNew.remove(ip)

        for ip in jsonList:
            scheme = ip["type"]
            domain = ip["url"]

            print(domain)

            proxies = {scheme: domain}
            code = getFile(url, headers, proxies)

            if 1 == code:
                break
            else:
                jsonListNew.remove(ip)

print("可用的 ip 列表是：" + getStr(jsonListNew) + "/" + getStr(jsonList))

fileName = "new_avilable_ip.txt"
fileObject = open("/Users/WangQing/PycharmProjects/ScrapyPro/ProxyPro/manhua/" + fileName, 'w+')
fileObject.write(str(jsonListNew).replace("'", "\"") + "\n")
fileObject.close()
