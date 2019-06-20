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

        list = []

        for item in proxyItem:
            try:
                td = item.css("td").css("td::text").extract()
                ip = td[0]
                port = td[1]
                area = td[2]
                type = str(td[5]).lower()

                print("用户 ip:" + ip + ", port:" + port + ", area:" + area + 'type: ' + type)

                obj = {"type": type, "url": type + "://" + ip + ":" + port}

                list.append(obj)

                print(obj)

            except:
                pass

        listStr = str(list).replace("'", "\"")
        print(listStr)

        fileObject = open('ipList.txt', 'w')
        fileObject.write(listStr)
        fileObject.close()
