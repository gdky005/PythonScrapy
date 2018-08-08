import requests
import scrapy
from scrapy import Selector, FormRequest
from scrapy.spiders import Spider
from DBHelper import insertSubInfoItem2DB, insertSubMovieDownloadItem2DB, insertSubMovieLastestItem2DB


class SubProFor6v(Spider):
    name = "SubProFor6v"
    # start_urls = [
    #     # "http://www.hao6v.com/dlz/2018-06-19/31337.html",
    #     # "http://www.hao6v.com/dlz/2018-08-03/31584.html",
    #     # "http://www.hao6v.com/dy/2018-07-30/ZQSRHTS.html",
    #     "http://www.hao6v.com/dlz/2018-07-20/31520.html",
    #     "http://www.hao6v.com/dlz/2018-08-03/31584.html",
    # ]

    # 开启后，默认爬取接口中的 url, 参考：https://www.v2ex.com/t/433791
    def start_requests(self):
        result = requests.get("http://zkteam.cc/Subscribe/jsonQueryInfo/?des=hao6v")
        resultData = result.json()["result"]

        for data in resultData:
            url = data["url"]
            yield scrapy.Request(url=url, callback=self.parse)

    def __init__(self):
        super(SubProFor6v, self).__init__()

    def parse(self, response):
        content = response.body.decode("gb18030")
        # print("爬取的内容如下：" + content)

        url = response.url
        pid = url[url.rindex("/") + 1:url.rindex(".")]
        print("影片的 Url是：" + response.url + ", pid 是：" + pid)

        selector = Selector(text=content)

        # 影片图片：
        movie_name = selector.xpath('//div[@class="box"]/h1/text()').extract()[0].strip()

        #
        # 影片图片：
        movie_pic = selector.xpath('//div[@id="endText"]/p/img').css("img::attr(src)").extract()[0].strip()

        # #
        # # 影片介绍：
        des = ''
        movie_intro = selector.xpath('//div[@id="endText"]/p/text()').extract()
        try:
            indexIntro = movie_intro.index("◎简　　介")

            for index in range(len(movie_intro)):
                if indexIntro < index < movie_intro.__len__() - 1:
                    des += movie_intro[index]
        except:
            pass

        movie_intro = des

        #
        # # 影片截图：
        movie_intro_pic = selector.xpath('//div[@id="endText"]/p/img').css("img::attr(src)").extract()

        if movie_intro_pic.__len__() > 1:
            movie_intro_pic = movie_intro_pic[movie_intro_pic.__len__() - 1].strip()
        else:
            movie_intro_pic = ""

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
            "影片介绍：<" + movie_intro + ">, \n" +
            "影片截图：<" + movie_intro_pic + ">。 \n"
        )

        yield insertSubInfoItem2DB(pid, movie_name, movie_pic, url, movie_update_time, movie_intro, movie_intro_pic)

        downloadInfo = selector.xpath('//tbody/tr/td/a')

        numberIndex = 0
        for index, downloadData in enumerate(downloadInfo):
            # 影片名称：
            movie_fj_name = downloadData.css("a::text").extract()[0].strip()
            # 磁力链接：
            download_url = downloadData.css("a::attr(href)").extract()[0].strip()

            number = movie_fj_name[0:movie_fj_name.index(".")]

            if index == 0 and ".html" in movie_fj_name:
                continue

            try:
                if int(number) > numberIndex:
                    numberIndex = int(number)

                print("\n分集名字是：" + movie_fj_name
                      + ", \n分集集数: " + number
                      + ", \n磁力链接：<" + download_url + ">。\n")
            except:
                continue



            yield insertSubMovieDownloadItem2DB(pid, movie_fj_name, number, download_url)

        yield insertSubMovieLastestItem2DB(pid, numberIndex)