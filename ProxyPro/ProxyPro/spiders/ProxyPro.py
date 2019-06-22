import requests
import scrapy
from scrapy import Selector
from scrapy.spiders import Spider
import json


class ProxyPro(Spider):
    name = "ProxyPro"
    start_urls = [
        "https://www.xicidaili.com/nn/",
        # "http://www.xiladaili.com/gaoni/",
        # "https://www.kuaidaili.com/free/",
        "http://www.nimadaili.com/gaoni/",
    ]

    # def start_requests(self):
    #     for i in range(1, 2):
    #         # url = "https://www.xicidaili.com/nn/" + str(i)
    #         # url = "https://www.xicidaili.com/nt/" + str(i)
    #         url = "https://www.xicidaili.com/wt/" + str(i)
    #         url = "https://www.xicidaili.com/" + str(i)
    #         print(url)
    #         yield scrapy.Request(url=url,  callback=self.parse)

    def parse(self, response):
        content = response.body.decode('utf-8')
        url = response.url
        print(url)
        # print(content)

        content = content
        # print("爬取的内容如下：" + content)
        list = []

        selector = Selector(text=content)

        proxyItem = selector.css("tbody").css("tr")
        if self.isXiCi(url):
            proxyItem = selector.css("tr.odd")

        print("爬取的个数：\n" + proxyItem.__len__().__str__())

        availableIpCount = 0
        count = 0

        countList = []
        countList.append(availableIpCount)
        countList.append(count)

        fileName = ""
        for item in proxyItem:
            countList[1] = countList[1] + 1
            td = item.css("td::text").extract()

            # if 2 == countList[1]:
            #     break

            if "nimadaili" in url:
                fileName = "ipList_nima.txt"
                self.getNiMa(list, td, countList)
            if "kuaidaili" in url:
                fileName = "ipList_kuai.txt"
                self.getKuai(list, td, countList)
            if self.isXiCi(url):
                fileName = "ipList_xici.txt"
                self.getXiCi(list, td, countList)

        print("当前可用 ip 的个数是：" + list.__len__().__str__())
        listStr = str(list).replace("'", "\"")
        print(listStr)
        fileObject = open(fileName, 'w+')
        fileObject.write(listStr + "\n")
        fileObject.close()

    def isXiCi(self, url):
        return "xicidaili" in url

    def getXiCi(self, list, td, countList):
        ip = td[0]
        port = td[1]
        area = td[2]
        scheme = str(td[5]).lower()

        scheme = scheme.replace("\n", "").strip()

        if scheme is None or scheme == "":
            scheme = "http"

            # print("用户 ip:" + ip + ", port:" + port + ", area:" + area + 'type: ' + scheme)

        url = scheme + "://" + ip + ":" + port
        return self.getCommon(list, countList, scheme, url)

    def getKuai(self, list, td, countList):
        ip = td[0]
        port = td[1]
        area = td[4]
        scheme = str(td[3]).lower()

        scheme = scheme.replace("\n", "").strip()

        if scheme is None or scheme == "":
            scheme = "http"

        # print("用户 ip:" + ip + ", port:" + port + ", area:" + area + 'type: ' + scheme)

        url = scheme + "://" + ip + ":" + port

        return self.getCommon(list, countList, scheme, url)

    def getNiMa(self, list, td, countList):
        ip = td[0]
        port = td[1]
        area = td[3]
        scheme = str(td[1]).lower()

        scheme = scheme.replace("\n", "").strip()

        if scheme is not None and "https" in scheme:
            scheme = "https"
        else:
            scheme = "http"
        url = scheme + "://" + ip
        # print("用户 ip:" + ip + ", port:" + port + ", area:" + area + 'type: ' + scheme)

        return self.getCommon(list, countList, scheme, url)

    def getCommon(self, list, countList, scheme, url):
        try:
            obj = {"type": scheme, "url": url}

            proxies = {scheme: url}
            # 检测功能
            url1 = "http://httpbin.org/get"
            res = requests.get(url1, proxies=proxies, timeout=3)
            print("\n\n >>>>>>>>>[ 代理地址 结果 ]>>>>>>>>>>>>>>>\n  " +
                  url + "->" + str(res.status_code) +
                  "\n >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n"
                  )

            # # 可以使用就录入，否则放弃
            # print("准备针对域名校验：\n")
            #
            # url2 = "https://www.tohomh123.com"
            # res = requests.get(url2, proxies=proxies, timeout=5)

            errorCode = res.status_code

            if 200 == errorCode:
                print("\n >>>>>>>>>[ 域名地址 结果 ]>>>>>>>>>>>>>>>\n  " +
                      url + "->" + str(res.status_code) +
                      # url2 + "->" + str(res.status_code) +
                      "\n >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n\n"
                      )

                countList[0] = countList[0] + 1
                availableIpCount = countList[0]
                count = countList[1]

                print("录入符合规则的 IP 地址： " + str(availableIpCount) + "/" + str(count) + "\n\n\n")
                print(url)
                list.append(obj)
        except requests.exceptions.Timeout as e:
            print(str(e))
        except Exception as e:
            print(str(e))

        return list
