# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import Constant as Globle
import pymysql


class JDQSContentPipeline(object):
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

            # id = item['id']
            artifactName = item['artifactName']
            artifactAuthor = item['artifactAuthor']
            artifactContent = item['artifactContent']
            jid_id = item['jid_id']
            artifactSourceUrl = item['artifactSourceUrl']
            artifactUrl = item['artifactUrl']
            artifactCollection = item['artifactCollection']

            sql = "INSERT INTO " + self.table_name + " (" \
                                                     "artifactName, artifactAuthor, artifactContent, jid_id, " \
                                                     "artifactSourceUrl, artifactUrl, artifactCollection" \
                                                     ") VALUES (" \
                                                     "%s, %s, %s, %s, %s, %s, %s" \
                                                     ")"
            cur.execute(sql, (artifactName, artifactAuthor, artifactContent, jid_id, artifactSourceUrl, artifactUrl, artifactCollection))

            cur.close()
            self.conn.commit()

            return item
        except Exception as e:
            print("JDQSContentPipeline process_item 【【【出现异常】】】:" + repr(e))

            pass

    def close_spider(self):
        self.conn.close()
