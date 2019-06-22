import json
import time

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning


def getFile(url1, header, proxies1):
    res = requests.get(url1, headers=header, proxies=proxies1, verify=False)
    if 200 == res.status_code:
        print(res.content)
        return 1
    else:
        return 0


def getFile1(url1, header):
    res = requests.get(url1, headers=header, verify=False)
    if 200 == res.status_code:
        content = res.content.decode("utf-8")

        print(content)

        fileName = url1[url1.rindex("/") + 1:]

        fileObject = open(fileName, 'w+')
        fileObject.write(content + "\n")
        fileObject.close()


        return 1
    else:
        return 0


ipListPath = "/Users/WangQing/PycharmProjects/ScrapyPro/ProxyPro/ipList_nima.txt"
f = open(ipListPath)
data = f.read()
text = json.loads(data)

for i in range(1, 2):
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
    getFile1(url, headers)

    # for ip in text:
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
