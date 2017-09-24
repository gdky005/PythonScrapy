from scrapy.spiders import CrawlSpider
from scrapy import Selector
from DouBan.items import DoubanItem
from scrapy import Request


class Douban(CrawlSpider):
    name = "DouBan"
    start_urls = ['http://movie.douban.com/top250']
    # start_urls = ['http://www.6vhao.com/']

    def parse(self, response):

        selector = Selector(response)

        item = DoubanItem()

        Movies = selector.xpath('//div[@class="info"]')

        for eachMovice in Movies:
            title = eachMovice.xpath('div[@class="hd"]/a/span/text()').extract()
            full_title = ''
            for each in title:
                full_title += each

            # movieInfo = eachMovice.xpath('div[@class="bd"]/p/text()').extract()
            moviceInfos = eachMovice.xpath('div[@class="bd"]/p/text()').extract()
            moviceDetail = ''
            for moviceInfo in moviceInfos:
                moviceDetail += moviceInfo

            start = eachMovice.xpath('div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()').extract()[0]

            quote = eachMovice.xpath('div[@class="bd"]/p[@class="quote"]/span/text()').extract()
            if quote:
                quote = quote[0]
            else:
                quote = ""

            # print(full_title + "\n")
            # print(moviceDetail + "\n")
            # print(start + "\n")
            # print("\n""\n""\n经常绝伦的言论： " + quote + "\n""\n""\n")

            item['title'] = full_title
            item['movieInfo'] = moviceDetail
            item['star'] = start
            item['quote'] = quote

            # item.title = full_title
            # item.movieInfo = ';'.join(moviceDetail)
            # item.star = start
            # item.quote = quote
            yield item

            nextLink = eachMovice.xpath('//span[@class="next"]/link/@href').extract()
            if nextLink:
                nextLink = nextLink[0]
                # print(nextLink)
                url = "https://movie.douban.com/top250"
                yield Request(url + nextLink, callback=self.parse)

