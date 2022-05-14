# 此脚本根据当前目录下的excel表格文件构建ipc_info数据库，将各表中的数据汇总到一个数据库表中
import pandas as pd
import pymysql
import os
from sqlalchemy import create_engine  
root_dir = os.path.abspath(os.path.dirname(__file__))
pymysql.install_as_MySQLdb()

file_names = ['A-人类生活必需品.xlsx', 'B--作业；运输.xlsx', 'C-- 化学；冶金.xlsx', 'D部——纺织；造纸.xlsx',
              'E--固定建筑物.xlsx', 'F--机械工程；照明；加热；武器；爆破.xlsx', 'G--物理.xlsx', 'H--电学.xlsx']

for file_name in file_names:
    table_name = 'ipc_'+file_name[0:1]
    df = pd.read_excel(root_dir+'/'+file_name, header=None, names=["ipc_num", "ipc_info"])

    # 向下填充空白格并去重
    df = df.ffill().drop_duplicates()

    conn = create_engine('mysql+mysqldb://root:password@localhost:3306/report?charset=utf8')  
    df.to_sql('ipc_info',con=conn,if_exists='append',index=False)
    print('写入数据库表ipc_info：',file_name)

