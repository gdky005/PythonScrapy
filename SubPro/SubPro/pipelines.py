# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import Constant as Globle
import pymysql
from SubPro.items import SubInfoItem, SubMovieDownloadInfoItem, SubMovieLastestInfoItem


class SubInfoPipeline(object):
    host = Globle.Constant.host
    port = Globle.Constant.port
    user = Globle.Constant.user
    password = Globle.Constant.password
    database_name = Globle.Constant.database_name
    table_name = "Subscribe_submovieinfo"
    charset = Globle.Constant.charset

    def __init__(self):
        self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.password,
                                    db=self.database_name, charset=self.charset)

    def process_item(self, item, spider):
        try:
            if item is None or item is bool or item._class != SubInfoItem._class:
                return item

            # 给库中插入数据
            cur = self.conn.cursor()

            id = item['pid']
            name = item['name']
            pic = item['pic']
            url = item['url']
            update_time = item['update_time']
            intro = item['intro']
            capture_pic = item['capture_pic']

            sql = "INSERT INTO " + self.table_name + " (" \
                                                     "id, name, pic, url, update_time, intro, capture_pic" \
                                                     ") VALUES (" \
                                                     "%s, %s, %s, %s, %s, %s, %s" \
                                                     ")"
            cur.execute(sql, (id, name, pic, url, update_time, intro, capture_pic))
            cur.close()
            self.conn.commit()

            return item
        except Exception as e:
            print("SubInfoPipeline process_item 出现异常:" + e.__str__())
            return item

    def close_spider(self, spider):
        self.conn.close()


class SubMovieDownloadPipeline(object):
    host = Globle.Constant.host
    port = Globle.Constant.port
    user = Globle.Constant.user
    password = Globle.Constant.password
    database_name = Globle.Constant.database_name
    table_name = "Subscribe_submoviedownload"
    charset = Globle.Constant.charset

    def __init__(self):
        self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.password,
                                    db=self.database_name, charset=self.charset)

    def process_item(self, item, spider):
        # if item is None  or item == True or item == False or (item._class != SubMovieDownloadInfoItem):
        #     return item

        try:
            if item is None or item is bool or item._class != SubMovieDownloadInfoItem._class:
                return item

            # 给库中插入数据
            cur = self.conn.cursor()

            pid = item['pid']
            fj_name = item['fj_name']
            fj_number = item['fj_number']

            id = pid + fj_number

            fj_download_url = item['fj_download_url']

            sql = "INSERT INTO " + self.table_name + " (" \
                                                     "id, pid_id, fj_name, fj_download_url" \
                                                     ") VALUES (" \
                                                     "%s, %s, %s, %s" \
                                                     ")"
            cur.execute(sql, (id, pid, fj_name, fj_download_url))
            cur.close()
            self.conn.commit()

            return item
        except Exception as e:
            print("SubMovieDownloadPipeline process_item 出现异常:" + e.__str__())
            return item

    def close_spider(self, spider):
        self.conn.close()


class SubMovieLastestPipeline(object):
    host = Globle.Constant.host
    port = Globle.Constant.port
    user = Globle.Constant.user
    password = Globle.Constant.password
    database_name = Globle.Constant.database_name
    table_name = "Subscribe_submovielastestinfo"
    charset = Globle.Constant.charset

    def __init__(self):
        self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.password,
                                    db=self.database_name, charset=self.charset)

    def process_item(self, item, spider):
        # if item is None or item == True or item ==False or (item._class != SubMovieLastestInfoItem) :
        #     return item

        try:
            if item is None or item is bool or item._class != SubMovieLastestInfoItem._class:
                return item

            # 给库中插入数据
            cur = self.conn.cursor()

            pid = item['pid']
            id = pid
            fj_number = item['fj_number']

            sql = "INSERT INTO " + self.table_name + " (" \
                                                     "id, pid_id, fj_number" \
                                                     ") VALUES (" \
                                                     "%s, %s, %s" \
                                                     ")"
            cur.execute(sql, (id, pid, fj_number))
            cur.close()
            self.conn.commit()

            return item
        except Exception as e:
            print("SubMovieLastestPipeline process_item 出现异常:" + e.__str__())
            return item

    def close_spider(self, spider):
        self.conn.close()
