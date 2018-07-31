# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from abc import abstractmethod, ABCMeta

import Constant as Globle
import pymysql
from SubPro.items import SubInfoItem, SubMovieDownloadInfoItem, SubMovieLastestInfoItem


class BaseSubProPipeline(object):
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
            if self.is_this_obj(item, self.getChildItem()):
                return item

            # 给库中插入数据
            cur = self.conn.cursor()

            self.executeSql(item, cur)

            cur.close()
            self.conn.commit()

            return item
        except Exception as e:
            print(self.getClassName().__name__ + " process_item 出现异常:" + e.__str__())
            return item

    @abstractmethod
    def executeSql(self, item, cur):
        print("初始化 sql 相关数据")

    @abstractmethod
    def getChildItem(self):
        return "getChildItem"

    @abstractmethod
    def getClassName(self):
        return BaseSubProPipeline

    def close_spider(self, spider):
        self.conn.close()

    def is_this_obj(self, item, object):
        if item is None or item is bool or item._class != object._class:
            return True


class SubInfoPipeline(BaseSubProPipeline):
    table_name = "Subscribe_submovieinfo"

    def getChildItem(self):
        return SubInfoItem

    def getClassName(self):
        return SubInfoPipeline

    def executeSql(self, item, cur):
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


class SubMovieDownloadPipeline(BaseSubProPipeline):
    table_name = "Subscribe_submoviedownload"

    def getChildItem(self):
        return SubMovieDownloadInfoItem

    def getClassName(self):
        return SubMovieDownloadPipeline

    def executeSql(self, item, cur):
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


class SubMovieLastestPipeline(BaseSubProPipeline):
    table_name = "Subscribe_submovielastestinfo"

    def getChildItem(self):
        return SubMovieLastestInfoItem

    def getClassName(self):
        return SubMovieLastestPipeline

    def executeSql(self, item, cur):
        pid = item['pid']
        id = pid
        fj_number = item['fj_number']

        sql = "INSERT INTO " + self.table_name + " (" \
                                                 "id, pid_id, fj_number" \
                                                 ") VALUES (" \
                                                 "%s, %s, %s" \
                                                 ")"
        cur.execute(sql, (id, pid, fj_number))
