# coding=utf-8
import pymysql
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS


app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False
CORS(app, resources=r'/*')


@app.route('/')
def index():
    cursor = local_db.cursor()
    find_sql = "select * from inventors where inventor_id=74 limit 1"
    cursor.execute(find_sql)
    res = cursor.fetchall()[0]
    print(res)
    return jsonify(res)


# 返回ipc_top_inventor表中全部信息
# http://127.0.0.1:5000/ipc_category_info
@app.route('/ipc_category_info')
def getIpcCategoryInfo():
    # ipc_word = request.args.get("ipc_category")
    cursor = local_db.cursor(cursor=pymysql.cursors.DictCursor)
    sql = 'select * from ipc_top_inventor'
    cursor.execute(sql)
    res = cursor.fetchall()
    return jsonify(res)


# 返回ipc_category大类下全部inventor_id列表
# http://127.0.0.1:5000/ipc_category_all_inventors?ipc_category=A
@app.route('/ipc_category_all_inventors')
def getIpcCategoryAllInventors():
    ipc_category = request.args.get("ipc_category")
    cursor = local_db.cursor()
    sql = "select inventor_id from ipc_inventors where ipc_category = '" + ipc_category + "';"
    cursor.execute(sql)
    res_tuple = cursor.fetchall()
    res = []
    for t in res_tuple:
        res.append(t[0])

    return jsonify(res)


# 返回对应inventor的简要信息
# http://127.0.0.1:5000/inventor_info_brief?id=1
@app.route('/inventor_info_brief')
def getInventorInfoBrief():
    inventor_id = request.args.get("id")
    # print(inventor_id)

    try:
        brief_db = pymysql.connect(host='localhost',
                                   user='root',
                                   password='password',
                                   database='report')
    except:
        print("connect database fail!")

    cursor = brief_db.cursor(cursor=pymysql.cursors.DictCursor)
    column_names = ['inventor_id', 'inventor_name', 'inventor_companys',
                    'inventor_patents_totalnum', 'average_score', 'T_index']
    sql_column = ''
    for colunm_name in column_names:
        sql_column += (colunm_name+', ')
    sql_column = sql_column[0:-2]

    sql_brief = "select " + sql_column + \
        " from inventors where inventor_id = "+str(inventor_id) + ";"
    print(sql_brief)
    cursor.execute(sql_brief)
    inventor_brief_info = cursor.fetchone()
    # print(inventor_brief_info)

    return inventor_brief_info


# 返回inventor全部信息
# http://127.0.0.1:5000/inventor_info_all?id=1
@app.route('/inventor_info_all')
def getInventorInfoAll():
    inventor_id = request.args.get("id")
    # print(inventor_id)

    cursor = local_db.cursor(cursor=pymysql.cursors.DictCursor)
    column_names = ['inventor_id', 'inventor_name', 'patents_ids', 'patents_ipcs', 'inventor_companys', 'collaborators', 'inventor_categories',
                    'inventor_patents_totalnum', 'average_score', 'T_index']
    sql_column = ''
    for colunm_name in column_names:
        sql_column += (colunm_name+', ')
    sql_column = sql_column[0:-2]

    sql_brief = "select " + sql_column + \
        " from inventors where inventor_id = "+str(inventor_id) + ";"
    print(sql_brief)
    cursor.execute(sql_brief)
    inventor_brief_info = cursor.fetchone()
    # print(inventor_brief_info)

    return jsonify(inventor_brief_info)


# 根据patent_id返回专利信息
# http://127.0.0.1:5000/patent_info?id=77735
@app.route('/patent_info')
def getPatentInfo():
    patent_id = request.args.get("id")
    # print(inventor_id)

    cursor = remote_db.cursor(cursor=pymysql.cursors.DictCursor)
    column_names = ['id', 'company_id', 'name', 'status', 'patent_type', 'num', 'patenter',
                    'patenter_now', 'inventor', 'designer','ipc','info','public_date','application_date','address','patent_score']
    sql_column = ''
    for colunm_name in column_names:
        sql_column += (colunm_name+', ')
    sql_column = sql_column[0:-2]

    sql = "select " + sql_column + \
        " from company_patent where id = "+str(patent_id) + ";"
    print(sql)
    cursor.execute(sql)
    patent_info = cursor.fetchone()
    # print(patent_info)

    return jsonify(patent_info)



# 根据发明家姓名返回对应id列表
# http://127.0.0.1:5000/search_inventors?name=张元
@app.route('/search_inventors')
def getInventorsByName():
    name = request.args.get('name')
    sql = "select inventor_id from inventors where inventor_name = '" + name + "';"
    cursor = local_db.cursor()
    cursor.execute(sql)
    res_tuple = cursor.fetchall()
    res = []
    for t in res_tuple:
        res.append(t[0])
    return jsonify(res)


# @app.route('/classifiction_alexnet.html')
# def alexnet():
#     return render_template('classifiction_alexnet.html')

# @app.route('/classifiction_efficientnet.html')
# def efficientnet():
#     return render_template('classifiction_efficientnet.html')

# @app.route('/classifiction_regnet.html')
# def regnet():
#     return render_template('classifiction_regnet.html')

# @app.route('/classifiction_resnet.html')
# def resnet():
#     return render_template('classifiction_resnet.html')

# @app.route('/classifiction_resnext.html')
# def resnext():
#     return render_template('classifiction_resnext.html')


# @app.route('/imageprocess_equalize_hist.html')
# def equalize_hist():
#     return render_template('imageprocess_equalize_hist.html')


# @app.route('/upload/upimage',methods=['GET','POST'])
# def uploadimage():

#     #生成随机字符串，防止图片名字重复
#     ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 16))
#     #获取图片文件 name = upload
#     img = request.files.get('attrName')
#     #定义一个图片存放的位置 存放在static下面
#     path = basedir+"/static/source_images/"
#     #图片名称 给图片重命名 为了图片名称的唯一性
#     imgName = ran_str+img.filename
#     #图片path和名称组成图片的保存路径
#     file_path = path+imgName
#     cur_image.dir = file_path
#     print(cur_image.dir)

#     #保存图片
#     img.save(file_path)
#     #这个是图片的访问路径，需返回前端（可有可无）
#     url = '/static/source_images/'+imgName
#     #返回图片路径 到前端
#     return url

# @app.route('/upload/submit',methods=['GET'])
# def submit():
#     classname = request.args.get('classname')
#     demoname = request.args.get('demoname')
#     demoparams = request.args.get('demoparams')
#     demoparams_str = ''
#     if(demoparams != ''):
#         arr_p = demoparams.split('+')
#         for p in arr_p:
#             p = p.split(':')
#             demoparams_str += '--' +p[0] + ' ' + p[1] + ' '
#     print(demoparams_str)

#     res = run_model(classname,demoname,cur_image.dir,demoparams_str)
#     print(res)
#     return jsonify(res)

# @app.route('/upload/clear',methods=['GET'])
# def clear():
#     current_image_dir = ''
#     return 'clear success'

if __name__ == '__main__':

    try:
        local_db = pymysql.connect(host='localhost',
                                   user='root',
                                   password='password',
                                   database='report')
    except:
        print("connect database fail!")


    try:
        remote_db = pymysql.connect(host='120.27.209.14',
                                    port=22936,
                                    user='junshi',
                                    password='junshi_suwen',
                                    database='Report')
    except:
        print("connect database fail!")
    app.run()
