# 提供抽取inventor数据时操作数据库的各种方法
from time import time
from matplotlib.pyplot import table
from numpy import insert
import pymysql
import json


# in: 专利id
# out: 专利对应的category_id和category_name字典数组(专利表追踪到company再追踪到industry_domain表)
# [{'category_id': 1506, 'category_name': 'AGV自动导引运输车'}, {'category_id': 1510, 'category_name': '导航'}, {'category_id': 1513, 'category_name': '激光导航'}, {'category_id': 1574, 'category_name': 'inside_投融资'}]
def getCategory(patent_id, cursor):
    sql_get_industry_category_id = 'SELECT industry_category from company WHERE id in ( SELECT company_id from company_patent WHERE id = "'+str(
        patent_id)+'" );'
    cursor.execute(sql_get_industry_category_id)
    r = cursor.fetchone()
    # print("sql_function print :", r, type(r), "patent_id:", patent_id)

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
    result = {}
    for id in category_ids:
        sql_get_category_name = 'SELECT name from industry_domain WHERE id = ' + id+';'
        cursor.execute(sql_get_category_name)
        category_name = cursor.fetchone()[0]
        result[int(id)] = {"category_name": category_name}
    return result


# in: ipc号
# out: ipc号在ipc_info数据表中对应的info列表
def getIpcinfo(ipc_num, cursor):
    sql_get_ipcinfo = 'select ipc_info from ipc_info where ipc_num="' + ipc_num + '";'
    cursor.execute(sql_get_ipcinfo)
    res_tuple = cursor.fetchall()
    # print(res_tuple)
    res = []
    for t in res_tuple:
        # print(t)
        res.append(t[0])
    return(res)


# in: 一个非负数表示某个发明家专利数量
# out: 0-100分数
def getPatentNumScore(n):
    if n == 0:
        return 0
    elif n <= 2:
        return 10
    elif n <= 5:
        return 20
    elif n <= 10:
        return 30
    elif n <= 20:
        return 40
    elif n <= 30:
        return 50
    elif n <= 40:
        return 60
    elif n <= 50:
        return 70
    elif n <= 70:
        return 80
    elif n <= 100:
        return 90
    else:
        return 100

# 将inventor数据写入ipc_top_inventor 和 ipc_inventor表


def writeIpcTopInventor(inventor_id, cursor):
    # print(inventor_id)
    # 构建ipc大类字典存储数量
    cursor.execute('select ipc_category from ipc_top_inventor;')
    ipc_categories = cursor.fetchall()
    num_patents_in_ipc_category = {}
    for tuple_ipc_category in ipc_categories:
        num_patents_in_ipc_category[tuple_ipc_category[0]] = 0
    # 获取发明家数据
    sql_ipc_and_tindex = 'select patents_ipcs, T_index from inventors where inventor_id = ' + \
        str(inventor_id)+';'
    cursor.execute(sql_ipc_and_tindex)
    ipc_dic, T_index = cursor.fetchone()
    ipc_dic = json.loads(ipc_dic)
    # 计算该发明家涉猎各ipc大类次数
    for ipc_num in ipc_dic:
        first_word = ipc_num[0:1]
        for dic_first_word in num_patents_in_ipc_category:
            if first_word == dic_first_word:
                num_patents_in_ipc_category[first_word] += len(
                    ipc_dic[ipc_num]['time'])
    # print(num_patents_in_ipc_category)

    # inventor在各ipc大类中的领域评分
    ipc_score = {}
    for first_word in num_patents_in_ipc_category:
        if(num_patents_in_ipc_category[first_word] != 0):
            ipc_score[first_word] = getIpcScore(
                num_patents_in_ipc_category[first_word], T_index)
        # else:
        #     ipc_score[first_word] = 0

    # 对存在得分的大类与ipc_top_inventor表中已有得分进行比较，取前10
    for first_word, score in ipc_score.items():
        # 将有得分的发明家写入ipc_inventors表中
        writeIpcInventors(first_word, inventor_id, cursor)
        sql_top_inventors = "select top_inventors from ipc_top_inventor where ipc_category='"+first_word+"';"
        cursor.execute(sql_top_inventors)
        t_res = cursor.fetchone()[0]

        # print(t_res)
        if(t_res == None):
            table_data = {}
        else:
            table_data = json.loads(t_res)
        if len(table_data) < 10:
            table_data[inventor_id] = score
        else:
            min_score_key = min(table_data, key=lambda k: table_data[k])
            if(score > table_data[min_score_key]):
                del table_data[min_score_key]
                table_data[inventor_id] = score
        update_sql = "UPDATE ipc_top_inventor SET top_inventors='" + \
            json.dumps(table_data, ensure_ascii=False) + \
            "' WHERE ipc_category='"+first_word + "';"
        cursor.execute(update_sql)
        # local_db.commit()
    # print(ipc_score)
    return


# in: 发明人在某个ipc大类的涉猎数量 + 发明人T_index指数
# out: ipc 大类领域评分
def getIpcScore(ipc_num, T_index):
    if ipc_num == 0:
        score_num = 0
    elif ipc_num <= 2:
        score_num = 10
    elif ipc_num <= 5:
        score_num = 20
    elif ipc_num <= 10:
        score_num = 30
    elif ipc_num <= 20:
        score_num = 40
    elif ipc_num <= 30:
        score_num = 50
    elif ipc_num <= 40:
        score_num = 60
    elif ipc_num <= 50:
        score_num = 70
    elif ipc_num <= 70:
        score_num = 80
    elif ipc_num <= 100:
        score_num = 90
    else:
        score_num = 100
    finall_score = score_num * 0.5 + 0.5 * T_index
    return finall_score

# 将inventor_id写入ipc_inventors表中
# in: ipc号首字母 + inventor_id


def writeIpcInventors(ipc_firt_word, invnetor_id, cursor):
    num_exist_sql = "select count(ipc_category) from ipc_inventors where ipc_category = '"+ipc_firt_word+"' and inventor_id = " + str(invnetor_id) +";"
    cursor.execute(num_exist_sql)
    num_exist = cursor.fetchone()[0]
    # print('已存在数量：',num_exist)
    if(num_exist != 0):
        # print('!000')
        return 
    insert_sql = "insert into ipc_inventors (ipc_category, inventor_id) VALUE ('" + \
        ipc_firt_word + \
        "','" + \
        str(invnetor_id) +\
        "');"
    cursor.execute(insert_sql)
    return


if __name__ == "__main__":
    try:
        local_db = pymysql.connect(host='localhost',
                                   user='root',
                                   password='password',
                                   database='report')
    except:
        print("connect database fail!")
    local_cursor = local_db.cursor()
    # r = getIpcinfo('H', local_cursor)
    # print(r)\

    # print(getPatentNumScore(22))
    writeIpcTopInventor(343, local_cursor)
    local_db.commit()
