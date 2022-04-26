import configparser,os
from numpy import insert
import pymysql
import copytable

root_dir = os.path.abspath(os.path.dirname(__file__))
cf_dir = root_dir + "\sql_config.ini"

cf = configparser.ConfigParser()
cf.read(cf_dir)
db_info = {
    'database':'',
    'host':'',
    'port':'',
    'user':'',
    'password':''
}

for key in db_info:
    db_info[key] = cf.get('db',key)

try:
    db = pymysql.connect(host=db_info['host'],
                            port=int(db_info['port']),
                            user=db_info['user'],
                            password=db_info['password'],
                            database=db_info['database'])
except:
    print("connect database fail!")
cursor = db.cursor()



try:
    local_db = pymysql.connect(host='localhost',
                            user='root',
                            password='password',
                            database='report')
except:
    print("connect database fail!")
local_cursor = local_db.cursor()


# 在目标数据库中创建与原表结构相同的表
# copytable.copy_table(cursor,local_cursor,'company_patent')




# 两个数据库相同结构表的数据拷贝，根据id或其他主键增量式拷贝
times = 3000
# 每个times对应10条数据
maxid = 0
for i in range(times):
    i+=1
    local_cursor.execute('select max(id) from company_patent;')
    res_id = local_cursor.fetchone()
    print(res_id,type(res_id))
    if(res_id == (None,)):
        maxid = 0
    else:
        maxid = res_id[0]
    sql = 'select * from company_patent where id>' + str(maxid) + ' order by id limit 10;'
    print(sql)
    cursor.execute(sql)
    cols_name = cursor.description
    result = cursor.fetchall()
    # print(cols_name)
    # print(result)


    cols_sql = ''
    for col_name in cols_name:
        cols_sql += ( col_name[0] + ', ' )
    cols_sql = '( ' + cols_sql[:-2] + ' ) \n'

    # print(cols_sql)

    values_sql = ''
    for value in result:
        value_sql = ''
        for item in value:
            if(item == None):
                value_sql += ( 'NULL' + ',\n' )
            else:
                value_sql += ('\'' + str(item).replace('\'','\"') + '\'' + ',\n')
        value_sql = '( ' + value_sql[:-2] + ' ),\n'
        values_sql += value_sql
    values_sql = values_sql[:-2]
    # print( values_sql)

    insert_sql = 'insert into company_patent\n' + cols_sql + 'VALUES\n' + values_sql + ';' 

    local_cursor.execute(insert_sql)
    local_db.commit()
    print('insert items:',i*10)


# with open('insert.sql','w',encoding="utf-8") as f:
#     f.write(insert_sql)


# 关闭数据库连接
db.close()
local_db.close()

