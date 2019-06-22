import json
import time

import requests


def getFile(url1, header, proxies1):
    res = requests.get(url1, headers=header, proxies=proxies1, verify=False)
    if 200 == res.status_code:
        print(res.content)
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

    headers = {'Host': 'tohomh123.com',
               'Connection': 'keep-alive',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.26 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/517.36',
               'Referer': 'http://www.tohomh123.com/'}

    time.sleep(1)

    print(i)
    url = "https://www.tohomh123.com/f-1------updatetime--" + str(i) + ".html"
    # url = "http://httpbin.org/get"
    print(url)

    for ip in text:
        scheme = ip["type"]
        domain = ip["url"]

        print(domain)

        proxies = {scheme: domain}
        code = getFile(url, headers, proxies)

        if 1 == code:
            break
