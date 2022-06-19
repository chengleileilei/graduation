import pymysql
import datetime
import os
import json
import ast
from sql_functions import getCategory,getIpcinfo,getPatentNumScore,writeIpcTopInventor,getCompanyName

# 设置计算T_index指标专利数量和专利平均分的权重
w_patent_score= 0.5
w_patent_num= 0.5

from disambugation import isDisambugation

root_dir = os.path.abspath(os.path.dirname(__file__))

try:
    local_db = pymysql.connect(host='localhost',
                               user='root',
                               password='password',
                               database='report')
except:
    print("connect database fail!")
local_cursor = local_db.cursor()

try:
    remote_db = pymysql.connect(host='120.27.209.14',
                                port=22936,
                                user='junshi',
                                password='junshi_suwen',
                                database='Report')
except:
    print("connect database fail!")
remote_cursor = remote_db.cursor()



# 构造sql语句查询属性部分
patent_column_prop = ['id', 'company_id', 'patenter',
                      'inventor', 'designer', 'ipc', 'application_date', 'patent_score']
patent_column_prop_sql = ''
for prop in patent_column_prop:
    patent_column_prop_sql += prop
    patent_column_prop_sql += ','
patent_column_prop_sql = patent_column_prop_sql[:-1]


# 计时
starttime = datetime.datetime.now()


t = 10000  # 设置处理数据的数量
for i in range(t):

    i += 1
    # 获取本地持久化的数据库已处理的最大id值
    with open(root_dir+'\\current_patent_id.txt', 'r', encoding="utf-8")as f:
        max_patent_id = int(f.read())
    # print("table max_id is :", max_patent_id)
    sql = 'select '+patent_column_prop_sql+' from company_patent where id>' + \
        str(max_patent_id) + ' order by id limit 1;'
    remote_cursor.execute(sql)
    data_result = remote_cursor.fetchall()[0]

    # 构造字典，存储从company_patent一条数据中抽取的内容
    patent_data = {
        'patent_id': data_result[0],
        'company_id': data_result[1],
        'company_name': [getCompanyName(data_result[1],remote_cursor)],
        # 将字符串数组转化为真正数组
        'inventors': ast.literal_eval(data_result[3]) + ast.literal_eval(data_result[4]),
        'ipcs': ast.literal_eval(data_result[5]),
        'time': data_result[6],
        'patent_score': data_result[7],
    }
    # for k, v in patent_data.items():
    #     print(k, v, sep=' : ', end='\n')

    # 获取inventors表中的最大id，用以生成新的id
    max_inventor_id = 0
    find_max_inventor_id_sql = 'select max(inventor_id) from inventors;'
    local_cursor.execute(find_max_inventor_id_sql)
    res_inventor_id = local_cursor.fetchall()[0][0]
    if(res_inventor_id == None):
        max_inventor_id = 0
    else:
        max_inventor_id = res_inventor_id
    # print(max_inventor_id)

    # 构建current_inventors字典存储id和是否为新入库inventor
    current_inventors = {}
    sub_id = 0
    # print("inventor names in one patent:" ,patent_data['inventors'])
    for inventor_name in patent_data['inventors']:
        current_inventors[inventor_name] = {}
        current_inventors[inventor_name]['inventor_id'] = -1
        current_inventors[inventor_name]['tag'] = ''

        # 查询表中是否存在同名inventor
        # find_same_sql = "select inventor_id from inventors where inventor_name='" \
        #     + inventor_name \
        #     + "';"
        # local_cursor.execute(find_same_sql)
        # res = local_cursor.fetchall()
        # print(find_same_sql, type(res), res, sep='\n')

        disambugation_res_id = isDisambugation(
            name=inventor_name, cursor=local_cursor, patent_data=patent_data)
        if (disambugation_res_id == -1):
            # 未找到同名inventor，或与同名inventor为不同人，生成新id和数据
            sub_id += 1
            # print("name is not exist in table!")
            current_inventors[inventor_name]['tag'] = 'new'
            current_inventors[inventor_name]['inventor_id'] = max_inventor_id + sub_id
        else:
            # 与同名inventor为同一人，无需生成新id
            # old_id = res[0][0]
            current_inventors[inventor_name]['tag'] = 'old'
            current_inventors[inventor_name]['inventor_id'] = disambugation_res_id
    # print("inventor names in one patent:" ,patent_data['inventors'])

    print("----------------------抽取专利id：",
          patent_data['patent_id'], "得到发明人基础信息如下---------------------------")
    for k, v in current_inventors.items():
        print(k, v, sep=' : ', end='\n')
    # print('*************************')
    # print([ current_inventors[k]['inventor_id'] for k,v in current_inventors.items()])

    # 对current_inventor中的每一个inventor进行数据写入（新建或更新）
    for ck, cv in current_inventors.items():
        # print(k, v, sep=' : ', end='\n')
        # 计时开始
        # starttime = datetime.datetime.now()

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
            'patents_ipcs': dict( zip( patent_data['ipcs'], [{'time':[patent_data['time']]}] * len(patent_data['ipcs']) ) ),
            'collaborators': dict(
                zip([current_inventors[kv[0]]['inventor_id'] for kv in current_inventors.items()],
                    [dict(zip(['name', 'patent_ids', 'times'], [kv[0], [patent_data['patent_id']], [patent_data['time']]]))
                        for kv in current_inventors.items()
                     ]
                    )),
            'average_score': patent_data['patent_score'],
            'num_with_score': 0,
            'inventor_categories': getCategory(patent_data['patent_id'], remote_cursor),
            'T_index':0
        }

        # endtime = datetime.datetime.now()
        # print (endtime - starttime)

        # 构造当前inventor数据

        # 在合作者中删除本人，并将数据json化
        del new_inventor_data["collaborators"][new_inventor_data['inventor_id']]
        new_inventor_data["collaborators"] = json.dumps(
            new_inventor_data["collaborators"], ensure_ascii=False)
        # 判断是否为有评分专利
        if new_inventor_data['average_score'] != None:
            new_inventor_data['num_with_score'] = 1
            new_inventor_data['T_index'] = w_patent_num * getPatentNumScore(new_inventor_data['num_with_score']) + w_patent_score *new_inventor_data['average_score']
        # else:
        #     new_inventor_data['average_score'] =-1

        # 为inventor_categories添加time信息
        for category_id, category_data in new_inventor_data['inventor_categories'].items():
            new_inventor_data['inventor_categories'][category_id]['time'] = [
                patent_data['time']]
        new_inventor_data["inventor_categories"] = json.dumps(
            new_inventor_data["inventor_categories"], ensure_ascii=False)
        # 为patent_ipc添加ipc_info中具体信息
        for ipc_num in new_inventor_data['patents_ipcs']:
            # print(new_inventor_data['patents_ipcs'][ipc_num])
            new_inventor_data['patents_ipcs'][ipc_num]['ipc_info'] = getIpcinfo(ipc_num,local_cursor)
        new_inventor_data["patents_ipcs"] = json.dumps(
            new_inventor_data["patents_ipcs"], ensure_ascii=False)


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
            print('--写入新inventor：', ck)
            insert_sql = insert_sql.replace("'None'", "null")
            # print(insert_sql.replace("'None'", "null"))
            # 数据插入并提交
            local_cursor.execute(insert_sql)
            local_db.commit()

        # 对已存在inventor数据更新
        else:
            # inventors_column_prop = ['inventor_name', 'patents_ids',
            #                          'inventor_patents_totalnum', 'inventor_companys', 'patents_ipcs', 'collaborators']

            # 读取表中已存在的inventor数据
            old_inventor_data = {}
            for kv in new_inventor_data.items():
                find_sql = 'select ' + kv[0] + ' from inventors where inventor_id=' + str(
                    current_inventors[ck]['inventor_id']) + ';'
                local_cursor.execute(find_sql)
                inventors_res = local_cursor.fetchall()[0][0]
                old_inventor_data[kv[0]] = inventors_res

            # 创建update_inventor_data存储更新后的数据
            update_inventor_data = {}

            # 更新 patents_ids 和 inventor_patents_totalnum 和 average_score 以及 num_with_score及T_index
            old_patents_ids = ast.literal_eval(
                old_inventor_data['patents_ids'])
            new_patent_id = new_inventor_data['patents_ids']
            if new_patent_id[0] not in old_patents_ids:
                update_inventor_data['patents_ids'] = old_patents_ids + \
                    new_patent_id
                update_inventor_data['inventor_patents_totalnum'] = old_inventor_data['inventor_patents_totalnum'] + 1
                # print(new_inventor_data['num_with_score'], '**************')
                if new_inventor_data['num_with_score'] != 0:
                    if old_inventor_data['num_with_score'] != 0:
                        update_inventor_data['num_with_score'] = old_inventor_data['num_with_score'] + 1
                        update_inventor_data['average_score'] = (
                            old_inventor_data['average_score'] * old_inventor_data['num_with_score'] + new_inventor_data['average_score']) / update_inventor_data['num_with_score']
                    else:
                        update_inventor_data['num_with_score'] = old_inventor_data['num_with_score'] + 1
                        update_inventor_data['average_score'] = new_inventor_data['average_score']
                    # 更新T_index
                    update_inventor_data['T_index'] = w_patent_num * getPatentNumScore(update_inventor_data['num_with_score']) + w_patent_score *update_inventor_data['average_score']
            


            # 更新 inventor_companys
            old_inventor_company = json.loads(
                old_inventor_data['inventor_companys'])
            update_inventor_data['inventor_companys'] = old_inventor_company
            new_inventor_company = json.loads(
                new_inventor_data['inventor_companys'])
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
            update_inventor_data['inventor_companys'] = json.dumps(
                update_inventor_data['inventor_companys'], ensure_ascii=False)

            # 更新 patents_ipcs
            old_patents_ipcs = json.loads(old_inventor_data['patents_ipcs'])
            update_inventor_data['patents_ipcs'] = old_patents_ipcs

            new_patents_ipcs = json.loads(new_inventor_data['patents_ipcs'])
            for ipc in new_patents_ipcs:
                if ipc not in old_patents_ipcs:
                    update_inventor_data['patents_ipcs'][ipc] = new_patents_ipcs[ipc]
                else:
                    update_inventor_data['patents_ipcs'][ipc]['time'] += new_patents_ipcs[ipc]['time']
            update_inventor_data['patents_ipcs'] = json.dumps(
                update_inventor_data['patents_ipcs'], ensure_ascii=False)

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
            update_inventor_data['collaborators'] = json.dumps(
                update_inventor_data['collaborators'], ensure_ascii=False)

            # 更新 inventor_categories
            old_inventor_categories = json.loads(
                old_inventor_data['inventor_categories'])
            update_inventor_data['inventor_categories'] = old_inventor_categories
            new_inventor_categories = json.loads(
                new_inventor_data['inventor_categories'])
            # print(new_inventor_categories)
            for category_id in new_inventor_categories:
                if category_id not in old_inventor_categories:
                    # 增加一个新company
                    update_inventor_data['inventor_categories'][category_id] = new_inventor_categories[category_id]
                else:
                    update_inventor_data['inventor_categories'][category_id]['time'] += new_inventor_categories[category_id]['time']
            update_inventor_data['inventor_categories'] = json.dumps(
                update_inventor_data['inventor_categories'], ensure_ascii=False)

            # 构造并执行更新sql语句
            # print('更新数据如下：')
            # for k, v in update_inventor_data.items():
            #     print(k, v, sep=' : ', end='\n')

            update_kv = ''
            for k, v in update_inventor_data.items():
                update_kv += (str(k) + '=\'' + str(v) + '\', ')
            update_kv = update_kv[:-2]

            update_sql = 'update inventors set ' + update_kv + \
                ' where inventor_id=' + \
                str(current_inventors[ck]['inventor_id']) + ';'
            # print(update_sql,sep='\n')
            local_cursor.execute(update_sql)
            local_db.commit()
            print('**更新旧inventor：', ck)
        # 更新ipc_top_inventor各个大类排名
        # writeIpcTopInventor(new_inventor_data['inventor_id'],local_cursor)

        local_db.commit()


    current_patent_id = patent_data['patent_id']
    with open(root_dir+'\\current_patent_id.txt', 'w', encoding="utf-8")as f:
        f.write(str(current_patent_id))
endtime = datetime.datetime.now()
print (endtime - starttime)

