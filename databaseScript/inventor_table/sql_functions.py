# 提供抽取inventor数据时操作数据库的各种方法
import pymysql



# in: 专利id
# out: 专利对应的category_id和category_name字典数组(专利表追踪到company再追踪到industry_domain表)
# [{'category_id': 1506, 'category_name': 'AGV自动导引运输车'}, {'category_id': 1510, 'category_name': '导航'}, {'category_id': 1513, 'category_name': '激光导航'}, {'category_id': 1574, 'category_name': 'inside_投融资'}]
def getCategory(patent_id):
    try:
        remote_db = pymysql.connect(host='120.27.209.14',
                                    port=22936,
                                    user='junshi',
                                    password='junshi_suwen',
                                    database='Report')
    except:
        print("connect database fail!")
        return
    cursor = remote_db.cursor()
    sql_get_industry_category_id = 'SELECT industry_category from company WHERE id in ( SELECT company_id from company_patent WHERE id = "'+str(patent_id)+'" );'
    cursor.execute(sql_get_industry_category_id)
    r = cursor.fetchone()
    print("sql_function print :",r,"patent_id:",patent_id)
    category_ids = eval(r[0])
    # print(category_ids)
    result= []
    for id in category_ids:
        sql_get_category_name = 'SELECT name from industry_domain WHERE id = ' + id+';'
        cursor.execute(sql_get_category_name)
        category_name = cursor.fetchone()[0]
        result.append({"category_id":int(id),"category_name":category_name})
    return result


print(getCategory("77735"))
