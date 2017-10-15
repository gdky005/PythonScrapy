# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import Constant as Globle
import pymysql

class JuediqiushengPipeline(object):
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

        id = item['id']
        jid = item['jid']
        url = item['url']

        sql = "INSERT INTO " + self.table_name + " (number, question, answer) VALUES (%s, %s, %s)"
        cur.execute(sql, (id, jid, url))
        cur.close()
        self.conn.commit()

        return item

    def close_spider(self):
        self.conn.close()