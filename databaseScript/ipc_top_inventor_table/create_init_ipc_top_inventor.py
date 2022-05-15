# 创建并初始化ipc_top_inventor表，用于存储各个ipc大类内的高排名发明家
import os
import pymysql

root_dir = os.path.abspath(os.path.dirname(__file__))
create_sql_dir = root_dir + "\ipc_top_inventor_create.sql"
init_sql_dir = root_dir + "\ipc_top_inventor_init.sql"


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
with open(init_sql_dir,'r',encoding="utf-8") as f :
    init_sql = f.read()


local_cursor.execute(create_sql)
# local_db.commit()
local_cursor.execute(init_sql)
local_db.commit()



# with open('insert.sql','w',encoding="utf-8") as f:
#     f.write(insert_sql)


# 关闭数据库连接
# db.close()
local_db.close()