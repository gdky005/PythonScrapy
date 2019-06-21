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

        # print(content)

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

                # print("用户 ip:" + ip + ", port:" + port + ", area:" + area + 'type: ' + scheme)

                try:
                    url = scheme + "://" + ip + ":" + port
                    obj = {"type": scheme, "url": url}

                    proxies = {scheme: url}
                    url1 = "http://httpbin.org/get"
                    res = requests.get(url1, proxies=proxies, timeout=5)
                    print("\n\n >>>>>>>>>[ 代理地址 结果 ]>>>>>>>>>>>>>>>\n  " +
                          url + "->" + str(res.status_code) +
                          "\n >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n\n"
                          )

                    print("\n\n准备针对域名校验：\n")

                    url2 = "https://www.tohomh123.com"
                    res = requests.get(url2, proxies=proxies, timeout=5)

                    print("\n\n >>>>>>>>>[ 域名地址 结果 ]>>>>>>>>>>>>>>>\n  " +
                          url2 + "->" + str(res.status_code) +
                          "\n >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n\n"
                          )

                    print("\n\n录入符合规则的 IP 地址：\n")
                    print(url)
                    list.append(obj)
                    # print(obj)
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
