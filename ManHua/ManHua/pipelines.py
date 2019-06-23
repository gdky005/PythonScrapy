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
        try:

            sql = "INSERT INTO " + self.table_name + "(mid, name, author, picUrl, state, stateId, remind, time, detail, " \
                                                     "url, category, categoryIdList, tag) VALUES (" \
                                                     "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
            cur.execute(sql, (mid, name, author, picUrl, state, stateId, remind, time, detail, url, category, categoryIdList, tag))
            cur.close()
            self.conn.commit()
        except Exception as e:
            args = e.args
            errorCode = args[0]
            errorMsg = args[1]
            if 1062 == errorCode:
                print(
                    "\n『>>>>>>>>> mid 键重复，name=" + name + ", mid=" + str(
                        mid) + "无需处理：" + errorMsg + "<<<<<<< 』\n\n")
            else:
                print("异常原因：" + str(e))
            pass

        return item

    def close_spider(self,spider):
        self.cursor.close()
        self.conn.close()
