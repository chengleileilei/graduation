import pymysql
import os
import json
import ast

from soupsieve import select
from sqlalchemy import null
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
                      'inventor', 'designer', 'ipc', 'application_date','patent_score']
patent_column_prop_sql = ''
for prop in patent_column_prop:
    patent_column_prop_sql += prop
    patent_column_prop_sql += ','
patent_column_prop_sql = patent_column_prop_sql[:-1]

t = 10000  # 设置处理数据的数量
for i in range(t):
    i += 1
    # 获取本地持久化的数据库已处理的最大id值
    with open(root_dir+'\\current_patent_id.txt', 'r', encoding="utf-8")as f:
        max_patent_id = int(f.read())
    # print("table max_id is :", max_patent_id)
    sql = 'select '+patent_column_prop_sql+' from company_patent where id>' + \
        str(max_patent_id) + ' order by id limit 1;'
    cursor.execute(sql)
    data_result = cursor.fetchall()[0]

    # 构造字典，存储从company_patent一条数据中抽取的内容
    patent_data = {
        'patent_id': data_result[0],
        'company_id': data_result[1],
        'company_name': ast.literal_eval(data_result[2]),
        'inventors': ast.literal_eval(data_result[3]) + ast.literal_eval(data_result[4]),  # 将字符串数组转化为真正数组
        'ipcs': ast.literal_eval(data_result[5]),
        'time': data_result[6],
        'patent_score':data_result[7],
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
        current_inventors[inventor_name]['tag'] = ''

        # 查询表中是否存在同名inventor
        find_same_sql = "select inventor_id from inventors where inventor_name='" \
            + inventor_name \
            + "';"
        cursor.execute(find_same_sql)
        res = cursor.fetchall()
        # print(find_same_sql, type(res), res, sep='\n')
        if (not res) or (isDisambugation(inventor_name=inventor_name, cursor=cursor, table_name='inventors')):
            # 未找到同名inventor，或与同名inventor为不同人，生成新id和数据
            sub_id += 1
            # print("name is not exist in table!")
            current_inventors[inventor_name]['tag'] = 'new'
            current_inventors[inventor_name]['inventor_id'] = max_inventor_id + sub_id
        else:
            # 与同名inventor为同一人，无需生成新id
            old_id = res[0][0]
            current_inventors[inventor_name]['tag'] = 'old'
            current_inventors[inventor_name]['inventor_id'] = old_id
    

    print("----------------------抽取专利",patent_data['patent_id'],"---------------------------")
    for k, v in current_inventors.items():
        print(k, v, sep=' : ', end='\n')
    # print('*************************')
    # print([ current_inventors[k]['inventor_id'] for k,v in current_inventors.items()])

    # 对current_inventor中的每一个inventor进行数据写入（新建或更新）
    for ck, cv in current_inventors.items():
        # print(k, v, sep=' : ', end='\n')

        # 构造当前inventor数据
        new_inventor_data = {
            'inventor_id': current_inventors[ck]['inventor_id'],
            'inventor_name': ck,
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
            'collaborators': dict(
                zip([current_inventors[kv[0]]['inventor_id'] for kv in current_inventors.items()],
                    [dict(zip(['name','patent_ids', 'times'], [kv[0], [patent_data['patent_id']] ,[patent_data['time']]]))
                        for kv in current_inventors.items()]
                    )),
            'average_score':patent_data['patent_score'],
            'num_with_score':0
        }

        # 在合作者中删除本人，并将数据json化
        del new_inventor_data["collaborators"][new_inventor_data['inventor_id']]
        new_inventor_data["collaborators"] = json.dumps(new_inventor_data["collaborators"], ensure_ascii=False)
        #判断是否为有评分专利
        if new_inventor_data['average_score'] != None:
            new_inventor_data['num_with_score'] = 1
        # else:
        #     new_inventor_data['average_score'] =0
            
        
        



        if current_inventors[ck]['tag'] == 'new':
            # 构造sql写入一条新的inventor数据
            # for k, v in new_inventor_data.items():
            #     print(k, v, sep=' : ', end='\n')
            # new_inventor_data['num_with_score'] +=1

            # 根据inventor_data数据构造insert sql语句
            cols_sql = ''
            values_sql = ''
            for k, v in new_inventor_data.items():
                cols_sql += str(k)
                cols_sql += ', '
                values_sql += ("\'"+str(v)+"\'")
                values_sql += ', '
            cols_sql = '( ' + cols_sql[:-2] + ' )\n'
            values_sql = '( ' + values_sql[:-2] + ' )'

            insert_sql = 'INSERT INTO inventors\n' + \
                cols_sql + 'VALUES\n' + values_sql + ';'
            print('--写入新inventor：',ck)
            insert_sql = insert_sql.replace("'None'","null")
            print(insert_sql.replace("'None'","null"))
            # 数据插入并提交
            cursor.execute(insert_sql)
            local_db.commit()

        # 对已存在inventor数据更新
        else:
            # inventors_column_prop = ['inventor_name', 'patents_ids',
            #                          'inventor_patents_totalnum', 'inventor_companys', 'patents_ipcs', 'collaborators']

            # 读取表中已存inventor数据
            old_inventor_data = {}
            for kv in new_inventor_data.items():
                find_sql = 'select ' + kv[0] + ' from inventors where inventor_id=' + str(
                    current_inventors[ck]['inventor_id']) + ';'
                cursor.execute(find_sql)
                inventors_res = cursor.fetchall()[0][0]
                old_inventor_data[kv[0]] = inventors_res

            # 创建update_inventor_data存储更新后的数据
            update_inventor_data = {}

            # 更新 patents_ids 和 inventor_patents_totalnum 和 average_score 以及 num_with_score
            old_patents_ids = ast.literal_eval(
                old_inventor_data['patents_ids'])
            new_patent_id = new_inventor_data['patents_ids']
            if new_patent_id[0] not in old_patents_ids:
                update_inventor_data['patents_ids'] = old_patents_ids + new_patent_id
                update_inventor_data['inventor_patents_totalnum'] = old_inventor_data['inventor_patents_totalnum'] + 1
                print(new_inventor_data['num_with_score'],'**************')
                if new_inventor_data['num_with_score']  != 0:
                    if old_inventor_data['num_with_score'] != None:
                        update_inventor_data['num_with_score'] = old_inventor_data['num_with_score'] + 1
                        update_inventor_data['average_score'] = ( old_inventor_data['average_score'] * old_inventor_data['num_with_score'] +new_inventor_data['average_score'] ) / update_inventor_data['num_with_score']
                    else:
                        update_inventor_data['num_with_score'] = old_inventor_data['num_with_score'] + 1
                        update_inventor_data['average_score'] = new_inventor_data['average_score']


            # 更新 inventor_companys
            old_inventor_company = json.loads(
                old_inventor_data['inventor_companys'])
            update_inventor_data['inventor_companys'] = old_inventor_company
            new_inventor_company = json.loads(new_inventor_data['inventor_companys'])
            # print(new_inventor_company)
            for company_id in new_inventor_company:
                if company_id not in old_inventor_company:
                    # 增加一个新company
                    update_inventor_data['inventor_companys'][company_id] = new_inventor_company[company_id]
                else:
                    # 同一company,更新times和patents_num
                    update_inventor_data['inventor_companys'][company_id]['patents_num'] += 1
                    # if new_inventor_company[company_id]['times'][0] not in old_inventor_company[company_id]['times']: # 时间不重复再进行更新
                    update_inventor_data['inventor_companys'][company_id]['times'] += new_inventor_company[company_id]['times']
            update_inventor_data['inventor_companys'] = json.dumps(update_inventor_data['inventor_companys'] , ensure_ascii=False)
            
            # 更新 patents_ipcs
            old_patents_ipcs = json.loads(old_inventor_data['patents_ipcs'])
            update_inventor_data['patents_ipcs'] = old_patents_ipcs

            new_patents_ipcs = json.loads(new_inventor_data['patents_ipcs'])
            for ipc in new_patents_ipcs:
                if ipc not in old_patents_ipcs:
                    update_inventor_data['patents_ipcs'][ipc] = new_patents_ipcs[ipc]
                else:
                    update_inventor_data['patents_ipcs'][ipc] += new_patents_ipcs[ipc]
            update_inventor_data['patents_ipcs'] = json.dumps(update_inventor_data['patents_ipcs'] , ensure_ascii=False)
            
            # 更新 collaborators
            old_collaborators = json.loads(
                old_inventor_data['collaborators'])
            update_inventor_data['collaborators'] = old_collaborators
            new_collaborators = json.loads(new_inventor_data['collaborators'])
            # print(new_collaborators)
            for col_id in new_collaborators:
                if col_id not in old_collaborators:
                    # 增加一个新company
                    update_inventor_data['collaborators'][col_id] = new_collaborators[col_id]
                else:
                    update_inventor_data['collaborators'][col_id]['times'] += new_collaborators[col_id]['times']
                    update_inventor_data['collaborators'][col_id]['patent_ids'] += new_collaborators[col_id]['patent_ids']
            update_inventor_data['collaborators'] = json.dumps(update_inventor_data['collaborators'], ensure_ascii=False)


            # print('更新数据如下：')
            # for k, v in update_inventor_data.items():
            #     print(k, v, sep=' : ', end='\n')
            
            update_kv = ''
            for k, v in update_inventor_data.items():
                update_kv += ( str(k) + '=\'' + str(v) + '\', ' )
            update_kv = update_kv[:-2]
            
            update_sql = 'update inventors set ' + update_kv + ' where inventor_id=' + str(current_inventors[ck]['inventor_id']) + ';'
            # print(update_sql,sep='\n')
            cursor.execute(update_sql)
            local_db.commit()
            print('**更新旧inventor：',ck)

    current_patent_id = patent_data['patent_id']
    with open(root_dir+'\\current_patent_id.txt', 'w', encoding="utf-8")as f:
        f.write(str(current_patent_id))    
