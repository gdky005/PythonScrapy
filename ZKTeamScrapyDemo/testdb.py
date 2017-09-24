import pymysql
import Constant as Globle

host = Globle.Constant.host
port = Globle.Constant.port
user = Globle.Constant.user
password = Globle.Constant.password
database_name = Globle.Constant.database_name
movie_table_name = Globle.Constant.movie_table_name
charset = Globle.Constant.charset

print(host)
print(port)
print(user)
print(password)
print(database_name)
print(movie_table_name)
print(charset)

conn = pymysql.connect(host=host, port=port, user=user, passwd=password, db=database_name, charset=charset)


# 查询库中所有的数据
def query_all_data(table_name):
    cur = conn.cursor()
    sql = "SELECT * FROM " + table_name
    cur.execute(sql)

    for row in cur.fetchall():
        print("查询的数据是: " + row.__str__())

    cur.close()


def insert_data(table_name):
    # 给库中插入数据
    cur = conn.cursor()

    # data
    title = "title1"
    movieInfo = "movieInfo1"
    star = "2"
    quote = "值得推荐一把"

    sql = "INSERT INTO " + table_name + " (title, movieInfo, star, quote) VALUES (%s, %s, %s, %s)"
    cur.execute(sql, (title, movieInfo, star, quote))
    cur.close()
    conn.commit()


print("原始数据库的数据：")
query_all_data(movie_table_name)
insert_data(movie_table_name)
print("新数据库的数据：")
query_all_data(movie_table_name)

conn.close()
