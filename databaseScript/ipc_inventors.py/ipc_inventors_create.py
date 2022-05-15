# 创建并初始化ipc_top_inventor表，用于存储各个ipc大类内的高排名发明家
import os
import pymysql

root_dir = os.path.abspath(os.path.dirname(__file__))
create_sql_dir = root_dir + "\ipc_inventors_create.sql"


try:
    local_db = pymysql.connect(host='localhost',
                            user='root',
                            password='password',
                            database='report')
except:
    print("connect database fail!")
local_cursor = local_db.cursor()

with open(create_sql_dir,'r',encoding="utf-8") as f :
    create_sql = f.read()


local_cursor.execute(create_sql)
local_db.commit()


# 关闭数据库连接
local_db.close()