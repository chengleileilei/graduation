import pymysql
from pytest import console_main
import json


def isDisambugation(name, patent_data, cursor):

    # 查询表中是否存在同名inventor
    find_same_sql = "select inventor_id from inventors where inventor_name='" \
        + name \
        + "';"
    cursor.execute(find_same_sql)
    ids_res = cursor.fetchall()

    # 构造同名id池字典并初始化相似性评分
    same_name_ids = {t[0]: -1 for t in ids_res}
    # 无同名id直接返回-1
    if len(same_name_ids) == 0:
        return -1

    # 存在同名id
    print("***************消歧：", name, ", id：",
          same_name_ids, "*******************")
    # 构造当前发明人数据
    source_data = {
        'collaborator_names': patent_data['inventors'].copy(),
        'ipcs': patent_data['ipcs'],
        'company_ids': [str(patent_data['company_id'])]
    }
    source_data['collaborator_names'].remove(name)
    print("->source_data: ")
    for k, v in source_data.items():
        print(k, ':', v)
    for same_id in same_name_ids:

        # 获取id池中每一个同名发明家的数据并分别计算相似性指标存入same_name_ids字典中
        get_data_sql = "select collaborators, patents_ipcs, inventor_companys from inventors where inventor_id=" \
            + str(same_id) \
            + ";"
        cursor.execute(get_data_sql)
        target_res = cursor.fetchone()
        target_res_dic = []
        for str_data in target_res:
            target_res_dic.append(json.loads(str_data))
        target_data = {}
        target_data["collaborator_names"] = [target_res_dic[0]
                                             [col_id]["name"] for col_id in target_res_dic[0]]
        target_data["ipcs"] = [ipc for ipc in target_res_dic[1]]
        target_data["company_ids"] = [
            company_id for company_id in target_res_dic[2]]
        print("->target_data: ")
        for k, v in target_data.items():
            print(k, ':', v)
        same_name_ids[same_id] = getSimilarity(source_data, target_data)
    
    # 获取相似性评分最高的id值
    highest_score = 0
    most_similar_id = -1
    for id,score in same_name_ids.items():
        if score > highest_score:
            highest_score = score
            most_similar_id = id
    # 设置相似性消歧阈值（需要优化计算阈值和权重）
    if( highest_score >= 0.2):
        print("消歧结果：与已存在同名发明家是同一人,id为：",most_similar_id)
        return most_similar_id
    else:
        print("消歧结果：与已存在同名发明家非同一人")

        return -1


def getSimilarity(source_data, target_data):
    weight = {
        'collaborator_names': 0.5,
        'ipcs': 0.3,
        'company_ids': 0.2
    }
    similarity_dic = {}
    res = 0 
    for k, v in source_data.items():
        list1 = source_data[k]
        list2 = target_data[k]
        common_num = getCommonNum(list1, list2)
        similarity_dic[k] = (common_num/(len(list1)+len(list2)-common_num) +
                             common_num/len(list1) +
                             common_num/len(list2)) / 3
        res += similarity_dic[k] *weight[k]
    print("similarity_dic:",similarity_dic)
    print("res:",res)
    return res


# 返回两个列表公共元素数量
def getCommonNum(list1, list2):
    commonList = [x for x in list1 if x in list2]
    return len(commonList)


if __name__ == '__main__':
    n = getCommonNum(['覃文飞', '王永锟', '栾云博', '韩笑'], ['付小康', '韩笑', '覃文飞'])
    print(n)


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
