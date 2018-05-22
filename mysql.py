import pymysql



# host = 120.27.112.240
# port = 3306
# user = root
# password = wq12345678
# database_name = zkteam_db
# movie_table_name = api_masterinfo
# charset = utf8

conn = pymysql.connect(host="120.27.112.240", port=3306, user="root", passwd="wq12345678",
                       db="xiaochengxu",
                       # db="zkteam_db",
                       charset="utf8")


# 查询库中所有的数据
def query_all_data(table_name):
    cur = conn.cursor()
    sql = "SELECT * FROM " + table_name
    cur.execute(sql)

    for row in cur.fetchall():
        print("查询的数据是: " + row.__str__())

    cur.close()



print("原始数据库的数据：")
query_all_data("hb_ad")
# insert_data(movie_table_name)
print("新数据库的数据：")
query_all_data("hb_ad")

conn.close()
