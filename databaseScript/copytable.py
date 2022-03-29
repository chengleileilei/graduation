import pymysql

def run_sql(cursor,sql):
    try:
        # 执行SQL语句
        cursor.execute(sql)
        print("copy table success!!!")
        # 获取所有记录列表
        return cursor.fetchall()
    except:
        print ("run sql \"" + sql + "\" failed!!!")


def get_table_stru(cursor,table_name):
    sql = 'desc ' + table_name + ';'
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        return cursor.fetchall()
    except:
        print ("Error: unable to desctable data")

dic = {
    'NO':'NOT NULL',
    'YES':'NULL',
    None:'',
    'PRI':'PRIMARY KEY',
    'MUL':'',
    '':'',
    'CURRENT_TIMESTAMP':'DEFAULT CURRENT_TIMESTAMP',
    '0':''
}


def copy_table(source_cursor,target_cursor,table_name):
    table_info = get_table_stru(source_cursor,table_name)
    colume_sql = ''
    for col in table_info:
        colume_sql += '`'+ col[0] + '` ' + col[1] + ' ' + dic[col[2]] + ' ' + dic[col[3]] + ' ' + dic[col[4]] + ' ' + col[5] + ',' +'\n'
    create_sql = "create table if not exists `" + table_name + "` ( \n" + colume_sql[:-2] + "\n) ENGINE=InnoDB DEFAULT CHARSET=utf8;"
    print("create_sql is : ",create_sql,sep='\n')
    res = run_sql(target_cursor,create_sql)
    return res

        

    # create_sql = """CREATE TABLE `income` (
    # `id` int(11) NOT NULL AUTO_INCREMENT,
    # `datetime` varchar(20) DEFAULT NULL,
    # `ironincome` decimal(20,2) DEFAULT NULL,
    # `generalincome` decimal(20,2) DEFAULT NULL,
    # `baiincome` decimal(20,2) DEFAULT NULL,
    # PRIMARY KEY (`id`)
    # ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
    # """
