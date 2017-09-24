# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import Constant as Globle
import pymysql
import pymysql.cursors


class WeibosourcePipeline(object):
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

        id = item['id']
        csdn_name = item['name']
        address = item['address']
        blog_list = item['blog_list']
        user_img = item['img']

        sql = "INSERT INTO " + self.movie_table_name + " (name, info, img) VALUES (%s, %s, %s)"
        cur.execute(sql, (csdn_name, blog_list, user_img))
        cur.close()
        self.conn.commit()

        return item

    # def close_spider(self):
    #     self.conn.close()
