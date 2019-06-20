from scrapy import Selector
from scrapy.spiders import Spider
from selenium import webdriver


class ProxyPro(Spider):
    name = "ProxyPro"
    start_urls = [
        "https://www.xicidaili.com/",
    ]

    def parse(self, response):
        content = response.body.decode('utf-8')

        print(content)

        content = content
        # print("爬取的内容如下：" + content)

        selector = Selector(text=content)
        proxyItem = selector.css("tr.odd")

        for item in proxyItem:
            try:
                td = item.css("td").css("td::text").extract()
                ip = td[0]
                port = td[1]
                area = td[2]
                type = td[4]

                print("用户 ip:" + ip + ", port:" + port + ", area:" + area + 'type: ' + type)
            except:
                pass