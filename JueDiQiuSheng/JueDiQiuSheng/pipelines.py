# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import Constant as Globle
import pymysql

from JueDiQiuSheng import Utils


class JDQSItemPipeline(object):
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
            jid = item['jid']
            artifactName = item['artifactName']
            artifactDate = item['artifactDate']
            artifactSourceUrl = item['artifactSourceUrl']
            artifactUrl = item['artifactUrl']
            picUrl = item['picUrl']
            categoryId = item['categoryId']
            artifactCollection = Utils.getCollectionTime()

            sql = "INSERT INTO " + self.table_name + " (" \
                                                     "jid, artifactName, artifactDate, artifactSourceUrl, artifactUrl, picUrl, categoryId_id, artifactCollection" \
                                                     ") VALUES (" \
                                                     "%s, %s, %s, %s, %s, %s, %s, %s" \
                                                     ")"
            cur.execute(sql, (jid, artifactName, artifactDate, artifactSourceUrl, artifactUrl, picUrl, categoryId, artifactCollection))
            cur.close()
            self.conn.commit()

            return item
        except Exception as e:
            print("JDQSContentPipeline process_item 【【【出现异常】】】:" + repr(e))

            pass

    def close_spider(self):
        self.conn.close()
