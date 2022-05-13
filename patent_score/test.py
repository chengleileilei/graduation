#!/usr/bin/python
# author kingbone
import pandas as pd
import numpy as np
import pickle
import time
import MySQLdb
import json
import re
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
from sklearn.linear_model import Ridge, Lasso

status2onehot = {'无效': -1, '失效': -1, '审中-实审': 0, '审中-公开': 0, '有权': 1}


def get_score(scaler, model, status, inventor, ipc, pub_date, application_date, claims):
    # print(claims, type(claims))
    try:
        claim_len = len(re.findall(r'\d+\.', claims)) if claims else 0
    except:
        claim_len = 0
    weight = 1 + status2onehot[status] * 0.1
    ipc_num = len(ipc)
    inventor_num = len(inventor)
    maintain = 12 * (time.localtime().tm_year - int(pub_date[:4])) + time.localtime().tm_mon - int(
        pub_date[5:7])
    if maintain > 200:
        maintain = 200
    applied = 12 * (int(pub_date[:4]) - int(application_date[:4])) + int(pub_date[5:7]) - int(
        application_date[5:7])
    status_onehot = status2onehot[status]
    x = [[claim_len, ipc_num, inventor_num, maintain, applied, status_onehot]]
    x = scaler.transform(x)
    predict = model.predict(x)
    return predict[0] * weight


def read_db():
    db = MySQLdb.connect(host='120.27.209.14', user='root', passwd="SW_MySQL_231", port=22936, db='Report',
                         charset='utf8mb4')
    cursor = db.cursor()
    company_list = ['1418467', '197372', '1418963', '1418597', '1393699']
    sql_head = "SELECT id,name,status,num,inventor,ipc,public_date,application_date,claims,structure_node FROM company_patent WHERE patent_type != '外观设计' AND industry = 'ele_car' AND company_guogao_id = '"
    sql_tail = "' LIMIT 1000"
    results = tuple()
    try:
        for company in company_list:
            cursor.execute(sql_head + company + sql_tail)
            results += cursor.fetchall()
    except:
        pass
    return results


if __name__ == '__main__':

    scaler = pickle.load(open('saved_model/scaler_ridge0.7725261496583674.pkl', 'rb'))
    ridge = pickle.load(open('saved_model/ridge0.7725261496583674.pickle', 'rb'))

    re_db = read_db()
    count = 0
    for id, name, status, num, inventor, ipc, public_date, application_date, claims, structure_node in re_db:
        count += 1
        if count % 10 in [2, 3, 4, 6, 8, 9]:
            continue
        try:
            ipc = eval(ipc)
        except:
            ipc = []
        try:
            inventor = eval(inventor)
        except:
            inventor = []
        score = get_score(scaler, ridge, status, inventor, ipc, public_date, application_date, claims)
