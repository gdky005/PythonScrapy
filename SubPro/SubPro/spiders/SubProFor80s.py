from scrapy import Selector
from scrapy.spiders import Spider
from selenium import webdriver


class SubProFor80s(Spider):
    name = "SubProFor80s"
    start_urls = [
        "https://www.80s.tw/ju/23161",
    ]

    def __init__(self):
        super(SubProFor80s, self).__init__()

    def parse(self, response):
        content = response.body.decode("utf-8")
        # print("爬取的内容如下：" + content)

        selector = Selector(text=content)

        # 影片图片：
        movie_name = selector.xpath('//h1[@class="font14w"]/text()').extract()[0].strip()

        # 影片图片：
        movie_pic = "http:" + selector.xpath('//div[@id="minfo"]/div[@class="img"]').css("img::attr(src)").extract()[0].strip()

        # 影片介绍：
        movie_intro = selector.xpath('//div[@id="movie_content"]/text()')[1].extract()

        # 影片截图：
        movie_intro_pic = "http:" + selector.xpath('//div[@class="noborder block1"]').css("img::attr(src)").extract()[0].strip()

        # .select("string(.)").extract() #表示获取标签内所有的文字，不分组。

        # 更新日期：
        movie_update_time = selector.xpath('//span[@class="span_block"]/text()')[6].extract().strip()

        if movie_update_time is "":
            movie_update_time = selector.xpath('//span[@class="span_block"]/text()')[10].extract().strip()


        # 已经获取到需要的名称
        print(
            "影片名字：<" + movie_name + ">, \n" +
            "影片图片：<" + movie_pic + ">, \n" +
            "更新日期：<" + movie_update_time + ">。 \n" +
            "影片介绍：<" + movie_intro + ">, \n" +
            "影片截图：<" + movie_intro_pic + ">。 \n"
        )

        downloadInfo = selector.xpath('//form[@name="myform"]/ul[@class="dllist1"]/li/span[@class="dlname nm"]/span/a')

        for downloadData in downloadInfo:
            # 影片名称：
            movie_fj_name = downloadData.css("a::text").extract()[0].strip()
            # 磁力链接：
            download_url =downloadData.css("a::attr(href)").extract()[0].strip()

            # 已经获取到需要的名称
            print(
                "影片名称：<" + movie_fj_name + ">, \n" +
                "磁力链接：<" + download_url + ">。\n")






