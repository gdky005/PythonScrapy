# ScrapyPro
ScrapyPro

抓包脚本使用教程

1. 创建Scrapy项目命令
```
scrapy startproject myproject
```
2. 将 wangqing_db_config.ini 和 Constant.py 文件放入 myproject 目录下，里面包含和服务器同步的账号。
    首先设置 database_name。
3. 将  文件放入 myproject 目录下，
4. 在 myproject 目录下创建 mainDetail.py，里面：
```
from scrapy import cmdline
cmdline.execute("scrapy crawl XXX".split())
```
5. 在 第二个 XXX 的目录下的  \__init__.py 里面添加：
```
    import pymysql
    pymysql.install_as_MySQLdb()
```


6. 在 items.py 里面添加相关的数据库字段
7. 在 pipelines.py 里面添加数据库相关操作：
```
import Constant as Globle
import pymysql
class XXX(object):
    host = Globle.Constant.host
    port = Globle.Constant.port
    user = Globle.Constant.user
    password = Globle.Constant.password
    database_name = Globle.Constant.database_name
    table_name = Globle.Constant.table_name
    charset = Globle.Constant.charset

    def __init__(self):
        self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.password,
                                    db=self.database_name, charset=self.charset)

    def process_item(self, item, spider):
        # 给库中插入数据
        cur = self.conn.cursor()

        number = item['number']
        question = item['question']
        answer = item['answer']
        .......

        sql = "INSERT INTO " + self.table_name + " (number, question, answer) VALUES (%s, %s, %s)"
        cur.execute(sql, (number, question, answer))
        cur.close()
        self.conn.commit()

        return item

    def close_spider(self):
        self.conn.close()
 ```


并修改相关的数据。
8. 在 settings.py 里面添加
```
ITEM_PIPELINES = {'xxx.pipelines.xxxPipeline': 800, }
ROBOTSTXT_OBEY = False
```
9. 在 spiders 创建 爬虫文件xxx.py:
```
    from scrapy import Selector
    from scrapy.spiders import Spider
    from selenium import webdriver

    class JueDiQiuSheng(Spider):
        name = "JueDiQiuSheng"
        start_urls = [
            "http://www.gamersky.com/z/playbattlegrounds/",
        ]

        def __init__(self):
            super(JueDiQiuSheng, self).__init__()
            # self.start_urls = ['http://buluo.qq.com/p/barindex.html?bid=%s' % bid]
            # self.allowed_domain = 'buluo.qq.com'
            self.driver = webdriver.Chrome("/Applications/Google Chrome.app/Contents/MacOS/chromedriver")
            self.driver.set_page_load_timeout(5)  # throw a TimeoutException when thepage load time is more than 5 seconds.

        def parse(self, response):
            self.driver.get(response.url)
            print(response.body.decode('utf-8'))

            content = self.driver.page_source
            # print("爬取的内容如下：" + content)

            selector = Selector(text=content)
            # name = selector.xpath('//span[@id="headerName"]/text()').extract()
            names = selector.xpath('//ul[@id="zl_ul"]/li/a/text()').extract()
            ids = selector.xpath('//ul[@id="zl_ul"]/li/a/@onclick').extract()

            # 已经获取到需要的名称
            print("我需要的名称：" + names.__str__())

   ```


10. 在 编译器里面直接运行 main.py 文件，即可。