from numpy import insert
import pymysql
import os
import json
import ast

from soupsieve import select
from disambugation import isDisambugation

root_dir = os.path.abspath(os.path.dirname(__file__))

try:
    local_db = pymysql.connect(host='localhost',
                               user='root',
                               password='password',
                               database='report')
except:
    print("connect database fail!")
cursor = local_db.cursor()

# 构造sql语句查询属性部分
patent_column_prop = ['id', 'company_id', 'patenter',
                      'inventor', 'ipc', 'application_date']
patent_column_prop_sql = ''
for prop in patent_column_prop:
    patent_column_prop_sql += prop
    patent_column_prop_sql += ','
patent_column_prop_sql = patent_column_prop_sql[:-1]

t = 1  # 设置处理数据的数量
for i in range(t):
    i += 1
    # 获取本地持久化的数据库已处理的最大id值，
    with open(root_dir+'\\current_patent_id.txt', 'r', encoding="utf-8")as f:
        max_patent_id = int(f.read())
    print("table max_id is :", max_patent_id)
    sql = 'select '+patent_column_prop_sql+' from company_patent where id>' + \
        str(max_patent_id) + ' order by id limit 1;'
    cursor.execute(sql)
    data_result = cursor.fetchall()[0]

    # 构造字典，存储从company_patent一条数据中抽取的内容
    patent_data = {
        'patent_id': data_result[0],
        'company_id': data_result[1],
        'company_name': ast.literal_eval(data_result[2]),
        'inventors': ast.literal_eval(data_result[3]),  # 将字符串数组转化为真正数组
        'ipcs': ast.literal_eval(data_result[4]),
        'time': data_result[5]
    }
    # for k, v in patent_data.items():
    #     print(k, v, sep=' : ', end='\n')

    # 获取inventors表中的最大id，用以生成新的id
    max_inventor_id = 0
    find_max_inventor_id_sql = 'select max(inventor_id) from inventors;'
    cursor.execute(find_max_inventor_id_sql)
    res_inventor_id = cursor.fetchall()[0][0]
    if(res_inventor_id == None):
        max_inventor_id = 0
    else:
        max_inventor_id = res_inventor_id
    # print(max_inventor_id)

    # 构建current_inventors字典存储id和是否为新入库inventor
    current_inventors = {}
    sub_id = 0
    for inventor_name in patent_data['inventors']:
        current_inventors[inventor_name] = {}
        current_inventors[inventor_name]['inventor_id'] = -1
        current_inventors[inventor_name]['tag'] = 'no update'

        # 查询表中是否存在同名inventor
        find_same_sql = "select inventor_id from inventors where inventor_name='" \
            + inventor_name \
            + "';"
        cursor.execute(find_same_sql)
        res = cursor.fetchall()
        # print(find_same_sql, type(res), res, sep='\n')
        if not res:
            # 未找到同名inventor，直接生成新的id和数据
            sub_id += 1
            # print("name is not exist in table!")
            current_inventors[inventor_name]['tag'] = 'new'
            current_inventors[inventor_name]['inventor_id'] = max_inventor_id + sub_id
        else:
            # print("name has existed in table!")
            if (isDisambugation(inventor_name=inventor_name, cursor=cursor, table_name='inventors')):
                # 与同名inventor为不同人，生成新id
                sub_id += 1
                # print("name is not exist in table!")
                current_inventors[inventor_name]['tag'] = 'new'
                current_inventors[inventor_name]['inventor_id'] = max_inventor_id + sub_id
            else:
                # 与同名inventor为同一人，无需生成新id
                old_id = res[0][0]
                current_inventors[inventor_name]['tag'] = 'old'
                current_inventors[inventor_name]['inventor_id'] = old_id
    for k, v in current_inventors.items():
        print(k, v, sep=' : ', end='\n')
    # print('*************************')
    # print([ current_inventors[k]['inventor_id'] for k,v in current_inventors.items()])

    # 对current_inventor中的每一个inventor进行数据写入（新建或更新）
    for k, v in current_inventors.items():
        # print(k, v, sep=' : ', end='\n')

        if current_inventors[k]['tag'] == 'new':
            # 构造sql写入一条新的inventor数据
            inventor_data = {
                'inventor_id': current_inventors[k]['inventor_id'],
                'inventor_name': k,
                'patents_ids': [patent_data['patent_id']],
                'inventor_patents_totalnum': 1,
                'inventor_companys': json.dumps({
                    patent_data['company_id']: {
                        'company_name': patent_data['company_name'],
                        'patents_num': 1,
                        'times': [patent_data['time']]
                    }
                }, ensure_ascii=False),
                'patents_ipcs': json.dumps(dict(zip(patent_data['ipcs'], [[patent_data['time']]] * len(patent_data['ipcs']))), ensure_ascii=False),
                'collaborators': json.dumps(dict(
                    zip([current_inventors[kv[0]]['inventor_id'] for kv in current_inventors.items()],
                        [dict(zip(['name', 'times'], [kv[0], [patent_data['time']]]))
                         for kv in current_inventors.items()]
                        )), ensure_ascii=False)
            }
            # print('========')
            # for k, v in inventor_data.items():
            #     print(k, v, sep=' : ', end='\n')

            # 根据inventor_data数据构造insert sql语句
            cols_sql = ''
            values_sql = ''
            for k, v in inventor_data.items():
                cols_sql += str(k)
                cols_sql += ', '
                values_sql += ("\'"+str(v)+"\'")
                values_sql += ', '
            cols_sql = '( ' + cols_sql[:-2] + ' )\n'
            values_sql = '( ' + values_sql[:-2] + ' )'

            insert_sql = 'INSERT INTO inventors\n' + \
                cols_sql + 'VALUES\n' + values_sql + ';'
            print('-------------------增加数据-----------------------')
            print(insert_sql)
            # 数据插入并提交
            cursor.execute(insert_sql)
            local_db.commit()

        # 对已存在inventor数据更新
        else:
            inventors_column_prop = ['inventor_name', 'patents_ids',
                                     'inventor_patents_totalnum', 'inventor_companys', 'patents_ipcs', 'collaborators']

            # 读取表中已存在数据
            old_inventor_data={}
            for col in inventors_column_prop:
                find_sql = 'select ' + col + ' from inventors where inventor_id=' + str(current_inventors[k]['inventor_id']) + ';'
                cursor.execute(find_sql)
                # inventors_res = cursor.fetchall()[0][0]
                old_inventor_data[col] = cursor.fetchall()[0][0]
            print('---------------追加数据-------------------')
            for k, v in old_inventor_data.items():
                print(k, v, sep=' : ', end='\n')

            new_inventor_data = {
                'inventor_id': current_inventors[k]['inventor_id'],
                'inventor_name': k,
                'patents_ids': [patent_data['patent_id']],
                'inventor_patents_totalnum': 1,
                'inventor_companys': json.dumps({
                    patent_data['company_id']: {
                        'company_name': patent_data['company_name'],
                        'patents_num': 1,
                        'times': [patent_data['time']]
                    }
                }, ensure_ascii=False),
                'patents_ipcs': json.dumps(dict(zip(patent_data['ipcs'], [[patent_data['time']]] * len(patent_data['ipcs']))), ensure_ascii=False),
                'collaborators': json.dumps(dict(
                    zip([current_inventors[kv[0]]['inventor_id'] for kv in current_inventors.items()],
                        [dict(zip(['name', 'times'], [kv[0], [patent_data['time']]]))
                         for kv in current_inventors.items()]
                        )), ensure_ascii=False)
            }


            # inventor_data = {
            #     'inventor_id': current_inventors[k]['inventor_id'],
            #     'inventor_name': k,
            #     'patents_ids': [patent_data['patent_id']],
            #     'inventor_patents_totalnum': 1,
            #     'inventor_companys': json.dumps({
            #         patent_data['company_id']: {
            #             'company_name': patent_data['company_name'],
            #             'patents_num': 1,
            #             'times': [patent_data['time']]
            #         }
            #     }, ensure_ascii=False),
            #     'patents_ipcs': json.dumps(dict(zip(patent_data['ipcs'], [patent_data['time']] * len(patent_data['ipcs']))), ensure_ascii=False),
            #     'collaborators': json.dumps(dict(
            #         zip([current_inventors[kv[0]]['inventor_id'] for kv in current_inventors.items()],
            #             [dict(zip(['name', 'times'], [kv[0], [patent_data['time']]]))
            #              for kv in current_inventors.items()]
            #             )), ensure_ascii=False)
            # }
