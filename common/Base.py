from config.conf import ConfigYml
from utils.MysqlUtil import Mysql

#1、定义init_db
def init_db(db_alias):
#2、初始数据库信息，通过配置文件
    db_info = ConfigYml().get_db_conf_info(db_alias)
    host = db_info["db_host"]
    user = db_info["db_user"]
    password = db_info["db_password"]
    db_name = db_info["db_name"]
    charset = db_info["db_charset"]
    port = db_info["db_port"]
#3、初始化mysql对象
    conn = Mysql(host,user,password,db_name,charset,port)
    print(conn)
    return conn

if __name__ == '__main__':
    init_db("db_pre")