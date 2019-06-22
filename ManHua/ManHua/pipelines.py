# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

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

        mid = item['mid']
        mid2 = item['mid2']
        url = item['url']
        name = item['name']

        sql = "INSERT INTO " + self.table_name + " (mid, mid2, url, name) VALUES (%s, %s, %s, %s)"
        cur.execute(sql, (mid, mid2, url, name))
        cur.close()
        self.conn.commit()

        return item

    def close_spider(self):
        self.conn.close()
