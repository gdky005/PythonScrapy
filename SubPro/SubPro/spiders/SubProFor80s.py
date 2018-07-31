from scrapy import Selector
from scrapy.spiders import Spider

from DBHelper import insertSubInfoItem2DB, insertSubMovieDownloadItem2DB, insertSubMovieLastestItem2DB


class SubProFor80s(Spider):
    name = "SubProFor80s"
    start_urls = [
        "https://www.80s.tw/dm/23093",
    ]

    def __init__(self):
        super(SubProFor80s, self).__init__()

    def parse(self, response):
        content = response.body.decode("utf-8")
        # print("爬取的内容如下：" + content)

        url = response.url
        pid = url[url.rindex("/") + 1:len(url)]
        print("影片的 Url是：" + response.url + ", pid 是：" + pid)

        selector = Selector(text=content)

        # 影片图片：
        movie_name = selector.xpath('//h1[@class="font14w"]/text()').extract()[0].strip()

        # 影片图片：
        movie_pic = "http:" + selector.xpath('//div[@id="minfo"]/div[@class="img"]').css("img::attr(src)").extract()[
            0].strip()

        # 影片介绍：
        movie_intro = selector.xpath('//div[@id="movie_content"]/text()')[1].extract()

        # 影片截图：
        movie_intro_pic = "http:" + selector.xpath('//div[@class="noborder block1"]').css("img::attr(src)").extract()[
            0].strip()

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

        yield insertSubInfoItem2DB(pid, movie_name, movie_pic, url, movie_update_time, movie_intro, movie_intro_pic)

        downloadInfo = selector.xpath('//form[@name="myform"]/ul[@class="dllist1"]/li/span[@class="dlname nm"]/span/a')

        numberIndex = 0
        for index, downloadData in enumerate(downloadInfo):
            # 影片分集名称：
            movie_fj_name = downloadData.css("a::text").extract()[0].strip()
            # 磁力链接：
            download_url = downloadData.css("a::attr(href)").extract()[0].strip()

            number = movie_fj_name[(movie_fj_name.index("第") + 1):movie_fj_name.index("集")]

            if int(number) > numberIndex:
                numberIndex = int(number)

            numberStr = str(number)

            if len(numberStr) < 3:
                if len(numberStr) == 1:
                    numberStr = "00" + numberStr
                elif len(numberStr) == 2:
                    numberStr = "0" + numberStr

            number = numberStr

            print("\n分集名字是：" + movie_fj_name
                  + ", \n分集集数: " + number
                  + ", \n磁力链接：<" + download_url + ">。\n")

            yield insertSubMovieDownloadItem2DB(pid, movie_fj_name, number, download_url)

        yield insertSubMovieLastestItem2DB(pid, numberIndex)

