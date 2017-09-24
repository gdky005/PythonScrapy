import re
import json
from scrapy.spiders import Spider


class DouYin(Spider):
    name = "DouYin"

    start_urls = [
        "https://aweme.snssdk.com/aweme/v1/nearby/feed/?max_cursor=0&min_cursor=20&count=40",
    ]

    def parse(self, response):
        content = response.body.decode('utf-8')
        # print("爬取的内容如下：" + content)

        # json1 = json.load(content)

        # print(json1.get("has_more"))

        data = {
            'no': 1,
            'name': 'Runoob',
            'url': 'http://www.runoob.com'
        }

        # json_str = json.dumps(content)
        json_str = json.loads(content)
        # print(json_str["extra"]["now"])
        print(json_str["aweme_list"][0]["video"]["play_addr"]["url_list"][0])
        # print("Python 原始数据：", repr(data))
        # print("JSON 对象：", json_str)





        # selector = Selector(text=content)
        # # name = selector.xpath('//span[@id="headerName"]/text()').extract()
        # names = selector.xpath('//ul[@id="zl_ul"]/li/a/text()').extract()
        # ids = selector.xpath('//ul[@id="zl_ul"]/li/a/@onclick').extract()
        #
        # # 已经获取到需要的名称
        # print("我需要的名称：" + names.__str__())
        # print("我需要的原始ID：" + ids.__str__())





