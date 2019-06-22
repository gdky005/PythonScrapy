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
        name = item['name']
        author = item['author']
        picUrl = item['picUrl']
        state = item['state']
        time = item['time']
        detail = item['detail']
        category = item['category']
        tag = item['tag']

        stateId = item['stateId']
        remind = item['remind']
        url = item['url']
        categoryIdList = item['categoryIdList']

        sql = "INSERT INTO " + self.table_name + "(mid, name, author, picUrl, state, stateId, remind, time, detail, " \
                                                 "url, category, categoryIdList, tag) VALUES (" \
                                                 "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
        cur.execute(sql, (mid, name, author, picUrl, state, stateId, remind, time, detail, url, category, categoryIdList, tag))
        cur.close()
        self.conn.commit()

        return item

    def close_spider(self):
        self.conn.close()
