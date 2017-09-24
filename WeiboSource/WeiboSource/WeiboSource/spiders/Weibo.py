from scrapy import FormRequest
from scrapy import Selector
from scrapy.spiders import CrawlSpider

from WeiboSource.items import WeibosourceItem


class Weibo(CrawlSpider):
    name = "Weibo"  # 爬虫命名
    # start_urls = ['http://weibo.cn/pub']  # 要爬取的页面地址
    # start_urls = ['http://movie.douban.com/top250']  # 要爬取的页面地址
    # start_urls = ['http://weibo.com/p/10050583018062']  # 要爬取的页面地址
    # start_urls = ['http://www.gdky005.com/']  # 要爬取的页面地址
    start_urls = ['http://blog.csdn.net/singwhatiwanna?viewmode=contents',
                  'http://blog.csdn.net/gdky005?viewmode=contents']  # 要爬取的页面地址

    def start_requests(self):
        cookies = {"SUB": "_2A2513xyfDeThGeBP41cV9CvOyjmIHXVWrQlXrDV8PUNbmtBeLXHskW9Kvq37pvWg2BLy07rlZ2AI2zjHhg.."}
        return [FormRequest(self.start_urls[0], cookies=cookies, callback=self.parse)]

    def parse(self, response):
        print(response.body.decode('utf-8'))

        item = WeibosourceItem()

        selector = Selector(response)

        csdn_name = selector.xpath('//span/a[@class="user_name"]/text()').extract()  # 用户名
        address = selector.xpath('//span[@class="link_title"]/a/@href').extract()  # 地址
        blog_list = selector.xpath('//span[@class="link_title"]/a/text()').extract()  # 博客目录
        user_img = selector.xpath('//div[@id="blog_userface"]/a/img/@src').extract()  # 用户图像
        # response.url          #当前 url

        print(csdn_name)

        for i in range(len(address)):
            item['id'] = 1
            item['name'] = csdn_name[0]
            item['address'] = 'http://blog.csdn.net' + address[i]
            item['blog_list'] = blog_list[i + 1].strip()
            item['img'] = user_img[0]

            yield item







            # for add in blog_list:
            #     item['id'] = 1
            #     item['name'] = csdn_name
            #     item['address'] = address
            #     item['blog_list'] = add
            #     item['img'] = user_img
            #
            #     yield item





            #
            # Movies = selector.xpath('//div[@class="info"]')
            #
            # for eachMovie in Movies:
            #     title = eachMovie.xpath('div[@class="hd"]/a/span/text()').extract()
            #     full_title = ''
            #     for each in title:
            #         full_title += each
            #
            #     movieInfo = eachMovie.xpath('div[@class="bd"]/p/text()').extract()
            #     movieDetail = ''
            #     for movieInfo in movieInfo:
            #         movieDetail += movieInfo
            #
            #     start = eachMovie.xpath('div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()').extract()[
            #         0]
            #
            #     quote = eachMovie.xpath('div[@class="bd"]/p[@class="quote"]/span/text()').extract()
            #     if quote:
            #         quote = quote[0]
            #     else:
            #         quote = ""
            #
            #     print(full_title + "\n")
            #     print(movieDetail + "\n")
            #     print(start + "\n")
            #     print("\n""\n""\n经常绝伦的言论： " + quote + "\n""\n""\n")
            #
            #     break  #先显示一个，如果要全部显示，可以注释这个 break
