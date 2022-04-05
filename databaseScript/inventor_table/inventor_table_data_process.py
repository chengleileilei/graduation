import pymysql
import os
import ast
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
column_prop = ['id', 'company_id', 'patenter',
               'inventor', 'ipc', 'application_date']
column_prop_sql = ''
for prop in column_prop:
    column_prop_sql += prop
    column_prop_sql += ','
column_prop_sql = column_prop_sql[:-1]

t = 1  # 设置处理数据的数量
for i in range(t):
    i += 1
    # 获取本地持久化的数据库已处理的最大id值，
    with open(root_dir+'\\current_patent_id.txt', 'r', encoding="utf-8")as f:
        max_patent_id = int(f.read())
    print("table max_id is :", max_patent_id)
    sql = 'select '+column_prop_sql+' from company_patent where id>' + \
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

    # 构建字典用于存储id和是否为新入库inventor
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

    for k, v in current_inventors.items():
        # print(k, v, sep=' : ', end='\n')

        if current_inventors[k]['tag'] == 'new':
            # 构造sql写入一条新的inventor数据
            inventor_data = {
                'inventor_id': current_inventors[k]['inventor_id'],
                'inventor_name': k,
                'patents_ids': str([patent_data['patent_id']]),
                'inventor_patents_totalnum': 1,
                'inventor_companys': {
                    patent_data['company_id']: {
                        'company_name': patent_data['company_name'],
                        'patents_num': 1,
                        'times': str([patent_data['time']])
                    }
                },
                'patent_ipcs': dict(zip(patent_data['ipcs'], [patent_data['time']] * len(patent_data['ipcs']))),
                'collaborators':dict(\
                    zip( [ current_inventors[kv[0]]['inventor_id'] for kv in current_inventors.items()],\
                        [ dict( zip( ['name','times'], [kv[0], [patent_data['time']] ] ) ) for kv in current_inventors.items()]
                        ))
            }
            print('========')
            for k, v in inventor_data.items():
                print(k, v, sep=' : ', end='\n')

        else:
            pass
            # 对已有数据进行更新
