# 提供抽取inventor数据时操作数据库的各种方法
import pymysql



# in: 专利id
# out: 专利对应的category_id和category_name字典数组(专利表追踪到company再追踪到industry_domain表)
# [{'category_id': 1506, 'category_name': 'AGV自动导引运输车'}, {'category_id': 1510, 'category_name': '导航'}, {'category_id': 1513, 'category_name': '激光导航'}, {'category_id': 1574, 'category_name': 'inside_投融资'}]
def getCategory(patent_id,cursor):
    sql_get_industry_category_id = 'SELECT industry_category from company WHERE id in ( SELECT company_id from company_patent WHERE id = "'+str(patent_id)+'" );'
    cursor.execute(sql_get_industry_category_id)
    r = cursor.fetchone() 
    print("sql_function print :",r,type(r),"patent_id:",patent_id)

    # 处理company_id无效的情况
    if r == None:
        return {}

    # 处理industry_category 值为'None'的情况
    if r[0] == 'None':
        return {}

    try:
        category_ids = eval(r[0])
    except:
        return {}
    # print(type(category_ids),category_ids)
    result= {}
    for id in category_ids:
        sql_get_category_name = 'SELECT name from industry_domain WHERE id = ' + id+';'
        cursor.execute(sql_get_category_name)
        category_name = cursor.fetchone()[0]
        result[int(id)] = {"category_name":category_name}
    return result


# in: ipc号
# out: ipc号在ipc_info数据表中对应的info列表
def getIpcinfo(ipc_num,cursor):
    sql_get_ipcinfo = 'select ipc_info from ipc_info where ipc_num="' + ipc_num + '";'
    cursor.execute(sql_get_ipcinfo)
    res_tuple = cursor.fetchall()
    # print(res_tuple)
    res = []
    for t in res_tuple:
        # print(t)
        res.append(t[0])
    return(res)

if __name__=="__main__":
    try:
        local_db = pymysql.connect(host='localhost',
                                user='root',
                                password='password',
                                database='report')
    except:
        print("connect database fail!")
    local_cursor = local_db.cursor()
    r = getIpcinfo('H',local_cursor)
    print(r)




