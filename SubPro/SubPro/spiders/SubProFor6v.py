from scrapy import Selector
from scrapy.spiders import Spider
from selenium import webdriver


class SubProFor6v(Spider):
    name = "SubProFor6v"
    start_urls = [
        "http://www.hao6v.com/dlz/2018-06-19/31337.html",
        # "http://www.hao6v.com/dy/2018-07-30/ZQSRHTS.html",
    ]

    def __init__(self):
        super(SubProFor6v, self).__init__()

    def parse(self, response):
        content = response.body.decode("gb18030")
        # print("爬取的内容如下：" + content)

        selector = Selector(text=content)

        # 影片图片：
        movie_name = selector.xpath('//div[@class="box"]/h1/text()').extract()[0].strip()

        #
        # 影片图片：
        movie_pic = selector.xpath('//div[@id="endText"]/p/img').css("img::attr(src)").extract()[0].strip()


        # #
        # # 影片介绍：
        movie_intr = selector.xpath('//div[@id="endText"]/p/text()').extract()
        if movie_intr.__len__() > 25:
            movie_intr = movie_intr[31]
        else:
            movie_intr = movie_intr[22]

        #
        # # 影片截图：
        movie_intr_pic = selector.xpath('//div[@id="endText"]/p/img').css("img::attr(src)").extract()

        if movie_intr_pic.__len__() > 1:
            movie_intr_pic = movie_intr_pic[movie_intr_pic.__len__() - 1].strip()
        else:
            movie_intr_pic = ""

        #
        # # .select("string(.)").extract() #表示获取标签内所有的文字，不分组。
        #
        # ◎上映日期：
        movie_update_time = selector.xpath('//div[@id="endText"]/p/text()').extract()[10].strip()


        # 已经获取到需要的名称
        print(
            "影片名字：<" + movie_name + ">, \n" +
            "影片图片：<" + movie_pic + ">, \n" +
            "更新日期：<" + movie_update_time + ">。 \n" +
            "影片介绍：<" + movie_intr + ">, \n" +
            "影片截图：<" + movie_intr_pic + ">。 \n"
        )

        downloadInfo =selector.xpath('//tbody/tr/td/a')

        for downloadData in downloadInfo:
            # 影片名称：
            movie_fj_name = downloadData.css("a::text").extract()[0].strip()
            # 磁力链接：
            download_url =downloadData.css("a::attr(href)").extract()[0].strip()

            # 已经获取到需要的名称
            print(
                "影片名称：<" + movie_fj_name + ">, \n" +
                "磁力链接：<" + download_url + ">。\n")






