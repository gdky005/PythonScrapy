# 使用指南

## items

```
import scrapy
from scrapy import Field


class ManHuaItem(scrapy.Item):
    # define the fields for your item here like:
    mid = Field()
    url = Field()
    name = Field()
    pass
```

请根据实际情况修改上面的 bean.

## pipelines

```
import Constant as Globle
import pymysql


class ManhuaPipeline(object):
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

        # todo 请根据这里适配你自己的数据
        mid = item['mid']
        url = item['url']
        name = item['name']

        # todo 请根据这里适配你自己的数据
        sql = "INSERT INTO " + self.table_name + " (mid, url, name) VALUES (%s, %s, %s)"
        # todo 请根据这里适配你自己的数据
        cur.execute(sql, (mid, url, name))
        cur.close()
        self.conn.commit()

        return item

    def close_spider(self):
        self.conn.close()

```

## settings

全部替换如下：

```
BOT_NAME = 'ManHua'

SPIDER_MODULES = ['ManHua.spiders']
NEWSPIDER_MODULE = 'ManHua.spiders'
ITEM_PIPELINES = {'ManHua.pipelines.ManhuaPipeline': 800, }
ROBOTSTXT_OBEY = False
```

## 配置 wangqing_db_config.ini 文件

将配置 wangqing_db_config.ini 文件拷贝进来，必须修改里面的 table_name 表名，否则会填充错误。

## ManHua

主文件里面添加如下：
```
# 插入数据到数据库中
def insertData2DB(mid, url, name):
    from ManHua.items import ManHuaItem
    item = ManHuaItem()
    item['mid'] = mid
    item['url'] = url
    item['name'] = name
    return item

```

根据实际情况添加需要使用的字段。