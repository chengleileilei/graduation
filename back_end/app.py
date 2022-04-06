# coding=utf-8
import pymysql
from flask import Flask,render_template,request,jsonify
from flask_cors import CORS


app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False
CORS(app, resources=r'/*')

@app.route('/')
def index():
    try:
        local_db = pymysql.connect(host='localhost',
                                user='root',
                                password='password',
                                database='report')
    except:
        print("connect database fail!")
    cursor = local_db.cursor()
    find_sql = "select * from inventors where inventor_id=74 limit 1"
    cursor.execute(find_sql)
    res = cursor.fetchall()[0]
    print(res)


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
    app.run()
