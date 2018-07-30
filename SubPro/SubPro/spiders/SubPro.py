from scrapy import Selector
from scrapy.spiders import Spider
from selenium import webdriver


class SubPro(Spider):
    name = "SubPro"
    start_urls = [
        "https://www.80s.tw/dm/23173",
    ]

    def __init__(self):
        super(SubPro, self).__init__()

    def parse(self, response):
        content = response.body.decode("utf-8")
        print("爬取的内容如下：" + content)

        selector = Selector(text=content)

        # 影片名称：
        movie_name = selector.xpath('//form[@name="myform"]/ul[@class="dllist1"]/li/span[@class="dlname nm"]/span/a').css(
            "a::text").extract()[0].strip()

        # 磁力链接：
        download_url = selector.xpath('//form[@name="myform"]/ul[@class="dllist1"]/li/span[@class="dlname nm"]/span/a').css(
            "a::attr(href)").extract()[0].strip()

        # 影片图片：
        movie_pic = "http:" + selector.xpath('//div[@id="minfo"]/div[@class="img"]').css("img::attr(src)").extract()[0].strip()

        # 影片介绍：
        movie_intr = selector.xpath('//div[@id="movie_content"]/text()')[1].extract()

        # .select("string(.)").extract() #表示获取标签内所有的文字，不分组。

        # 更新日期：
        movie_update_time = selector.xpath('//span[@class="span_block"]/text()')[6].extract()

        # 已经获取到需要的名称
        print(
            "影片名称：<" + movie_name + ">, " +
            "磁力链接：<" + download_url + ">, " +
            "影片图片：<" + movie_pic + ">, " +
            "影片介绍：<" + movie_intr + ">, " +
            "更新日期：<" + movie_update_time + ">。 ")
