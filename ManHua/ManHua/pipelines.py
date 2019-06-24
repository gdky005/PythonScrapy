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
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):

        # 给库中插入数据
        cur = self.conn.cursor()

        mid = item['mid']
        mid2 = item['mid2']
        picUrl = item['picUrl']
        count = item['count']
        sourceUrl = item['sourceUrl']
        try:
            sql = "INSERT INTO " + self.table_name + " (mid, mid2, picUrl, count, sourceUrl) VALUES (%s, %s, %s, %s, %s)"
            cur.execute(sql, (mid, mid2, picUrl, count, sourceUrl))
            cur.close()
            self.conn.commit()

            return item
        except Exception as e:
            args = e.args
            errorCode = args[0]
            errorMsg = args[1]
            if 1062 == errorCode:
                print(
                    "\n『>>>>>>>>> mid 键重复， mid2=" + mid2 + ", mid=" + str(
                        mid) + "无需处理：" + errorMsg + "<<<<<<< 』\n\n")
            else:
                print("异常原因：" + str(e))
            pass

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()