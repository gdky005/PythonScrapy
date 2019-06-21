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

        mid2 = item['mid2']
        name = item['name']
        picUrl = item['picUrl']
        newPageName = item['newPageName']
        mhUrl = item['mhUrl']
        mhNewUrl = item['mhNewUrl']

        sql = "INSERT INTO " + self.table_name + " (mid2, name, picUrl, newPageName, mhUrl, mhNewUrl) VALUES (%s, %s, %s, %s, %s, %s)"
        # todo 请根据这里适配你自己的数据
        cur.execute(sql, (mid2, name, picUrl, newPageName, mhUrl, mhNewUrl))
        cur.close()
        self.conn.commit()

        return item

    def close_spider(self):
        self.conn.close()
