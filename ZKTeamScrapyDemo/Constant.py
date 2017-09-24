import configparser


class Constant:
    config = configparser.ConfigParser()
    config.read("wangqing_db_config.ini")
    host = config.get("global", "host")
    port = config.getint("global", "port")
    user = config.get("global", "user")
    password = config.get("global", "password")
    database_name = config.get("global", "database_name")
    movie_table_name = config.get("global", "movie_table_name")
    charset = config.get("global", "charset")