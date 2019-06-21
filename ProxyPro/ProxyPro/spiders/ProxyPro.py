import requests
from scrapy import Selector
from scrapy.spiders import Spider
import json


class ProxyPro(Spider):
    name = "ProxyPro"
    start_urls = [
        "https://www.xicidaili.com/nn/",
    ]

    def parse(self, response):
        content = response.body.decode('utf-8')

        print(content)

        content = content
        # print("爬取的内容如下：" + content)

        selector = Selector(text=content)
        proxyItem = selector.css("tr.odd")

        print("爬取的个数：\n" + proxyItem.__len__().__str__())

        list = []

        for item in proxyItem:
            try:
                td = item.css("td").css("td::text").extract()
                ip = td[0]
                port = td[1]
                area = td[2]
                scheme = str(td[5]).lower()

                scheme = scheme.replace("\n", "").strip()

                if scheme is None or scheme == "":
                    scheme = "http"

                print("用户 ip:" + ip + ", port:" + port + ", area:" + area + 'type: ' + scheme)

                try:
                    url = scheme + "://" + ip + ":" + port
                    obj = {"type": scheme, "url": url}

                    proxies = {scheme: url}
                    res = requests.get("http://httpbin.org/get", proxies=proxies, timeout=5)
                    print(res.text)

                    print("录入：" + obj.__str__())
                    list.append(obj)
                    print(obj)
                except requests.exceptions.Timeout as e:
                    print(str(e))
                except:
                    pass
            except:
                pass

        print("当前可用 ip 的个数是：" + list.__len__().__str__())
        listStr = str(list).replace("'", "\"")
        print(listStr)

        fileObject = open('ipList.txt', 'w')
        fileObject.write(listStr)
        fileObject.close()
