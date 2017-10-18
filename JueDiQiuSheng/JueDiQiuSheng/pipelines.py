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
    table_name = "JueDiQiuSheng_jdqscategory"
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
            name = item['name']
            url = item['url']
            picUrl = item['picUrl']
            categoryId = item['categoryId']
            categoryName = item['categoryName']

            sql = "INSERT INTO " + self.table_name + " (" \
                                                     "jid, name, url, picUrl, categoryId, categoryName" \
                                                     ") VALUES (" \
                                                     "%s, %s, %s, %s, %s, %s" \
                                                     ")"
            cur.execute(sql, (jid, name, url, picUrl, categoryId, categoryName))
            cur.close()
            self.conn.commit()

            return item
        except:
            print("JuediqiushengPipeline process_item 出现异常")
            pass

    def close_spider(self):
        self.conn.close()


class JDQSDetailPipeline(object):
    host = Globle.Constant.host
    port = Globle.Constant.port
    user = Globle.Constant.user
    password = Globle.Constant.password
    database_name = Globle.Constant.database_name
    table_name = "JueDiQiuSheng_jdqsdetail"
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
            artifactAuthor = item['artifactAuthor']
            content = item['content']

            sql = "INSERT INTO " + self.table_name + " (" \
                                                     "jid, artifactName, artifactAuthor, content" \
                                                     ") VALUES (" \
                                                     "%s, %s, %s, %s" \
                                                     ")"
            cur.execute(sql, (jid, artifactName, artifactAuthor, content))

            cur.close()
            self.conn.commit()

            return item
        except Exception:
            print("JDQSDetailPipeline process_item 出现异常")
            pass

    def close_spider(self):
        self.conn.close()
