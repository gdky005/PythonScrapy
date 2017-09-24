# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import pymysql.cursors

import Constant as Globle


class DouBanPipeline(object):
    host = Globle.Constant.host
    port = Globle.Constant.port
    user = Globle.Constant.user
    password = Globle.Constant.password
    database_name = Globle.Constant.database_name
    movie_table_name = Globle.Constant.movie_table_name
    charset = Globle.Constant.charset

    def __init__(self):
        self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.password,
                                    db=self.database_name, charset=self.charset)

    def process_item(self, item, spider):
        # 给库中插入数据
        cur = self.conn.cursor()

        title = item['title']
        movieInfo = item['movieInfo']
        star = item['star']
        quote = item['quote']

        sql = "INSERT INTO " + self.movie_table_name + " (title, movieInfo, star, quote) VALUES (%s, %s, %s, %s)"
        cur.execute(sql, (title, movieInfo, star, quote))
        cur.close()
        self.conn.commit()

        return item

    def close_spider(self):
        self.conn.close()
