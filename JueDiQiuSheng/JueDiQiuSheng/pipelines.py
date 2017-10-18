# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import Constant as Globle
import pymysql


class JDQSCategoryPipeline(object):
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
        try:
            # 给库中插入数据
            cur = self.conn.cursor()

            id = item['id']
            categoryName = item['categoryName']
            categoryUrl = item['categoryUrl']

            sql = "INSERT INTO " + self.table_name + " (" \
                                                     "id, categoryName, categoryUrl" \
                                                     ") VALUES (" \
                                                     "%s, %s, %s" \
                                                     ")"
            cur.execute(sql, (id, categoryName, categoryUrl))

            cur.close()
            self.conn.commit()

            return item
        except Exception:
            print("JDQSCategoryPipeline process_item 出现异常")
            pass

    def close_spider(self):
        self.conn.close()
