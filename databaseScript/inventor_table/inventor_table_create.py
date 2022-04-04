import os
import pymysql

root_dir = os.path.abspath(os.path.dirname(__file__))
create_sql_dir = root_dir + "\create_inventor.sql"

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

try:
    local_cursor.execute(create_sql)
    local_db.commit()
    print('run sql success!')
except:
    print('commit failed!!!')


# with open('insert.sql','w',encoding="utf-8") as f:
#     f.write(insert_sql)


# 关闭数据库连接
# db.close()
local_db.close()

