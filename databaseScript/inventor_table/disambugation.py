import pymysql
from pytest import console_main
import json

def isDisambugation(name,patent_data,cursor):

    # 查询表中是否存在同名inventor
    find_same_sql = "select inventor_id from inventors where inventor_name='" \
        + name \
        + "';"
    cursor.execute(find_same_sql)
    ids_res = cursor.fetchall()

    same_name_ids = { t[0]:-1 for t in ids_res}
    if len(same_name_ids)==0:
        return -1
    print("存在同名发明家：",name,", 同名id为：",same_name_ids)

    source_data = {
        'collaborator_names':patent_data['inventors'].copy(),
        'ipcs':patent_data['ipcs'],
        'company_ids':[patent_data['company_id']]
    }
    source_data['collaborator_names'].remove(name)
    print("&&&&source_data: ")
    for k,v in source_data.items():
        print(k,':',v)
    for same_id in same_name_ids:

        get_data_sql = "select collaborators, patents_ipcs, inventor_companys from inventors where inventor_id=" \
        + str(same_id) \
        + ";"
        cursor.execute(get_data_sql)
        target_res = cursor.fetchone()
        target_res_dic=[]
        for str_data in target_res:
            target_res_dic.append(json.loads(str_data))
        target_data={}
        target_data["collaborator_names"] = [ target_res_dic[0][col_id]["name"] for col_id in target_res_dic[0] ]
        target_data["ipcs"] = [ ipc for ipc in target_res_dic[1] ]
        target_data["company_ids"] = [ company_id for company_id in target_res_dic[2] ]
        print("&&&&target_data: ")
        for k,v in target_data.items():
            print(k,':',v)
    return same_id


def getSimilarity(source_data,target_data){
    

    return similarity
}






# patent_data = {
#     'patent_id': data_result[0],
#     'company_id': data_result[1],
#     'company_name': ast.literal_eval(data_result[2]),
#     # 将字符串数组转化为真正数组
#     'inventors': ast.literal_eval(data_result[3]) + ast.literal_eval(data_result[4]),
#     'ipcs': ast.literal_eval(data_result[5]),
#     'time': data_result[6],
#     'patent_score': data_result[7],
# }
