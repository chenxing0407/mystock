#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json
# import pymysql
import pandas as pd
import time
from datetime import date
from datetime import datetime
from datetime import timedelta

HOST='192.168.1.116'
VALVE_AMOUNT = 5000 * 10000
STEP_AMOUNT= 100*10000

NOW = datetime.now()
KP = NOW.replace(hour=9, minute=25)
LUNCH = NOW.replace(hour=11, minute=30)
KP2 = NOW.replace(hour=13, minute=0)
TEN = NOW.replace(hour=10, minute=15)
THREE = NOW.replace(hour=15, minute=1)

send_map = {}

Gtoken = ''
token_get_time = ''
def get_token():
    global Gtoken, token_get_time
    now = datetime.now()
    if not Gtoken or (token_get_time+timedelta(seconds=7100) < now):

        #微信公众号上应用的CropID和Secret
        CropID='wx3b381e28fa3192c4'
        Secret='pdCl8v48qRM3XjzzHEnmwGnXcLuKliFoZhq-I7PtALo'

        #获取access_token
        GURL="https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=%s&corpsecret=%s" % (CropID, Secret)
              # https: //qyapi.weixin.qq.com/cgi-bin/message / send?access_token = ACCESS_TOKEN
        res = requests.get(GURL, verify=False)
        dict_result = json.loads(res.text)
        Gtoken=dict_result['access_token']
        token_get_time = datetime.now()
        return Gtoken
    else:
        return Gtoken

def send_msg(code, valve):
    PURL = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s" % get_token()

    # 企业号中的应用id
    AppID = 1
    # 部门成员id，微信接收者
    UserID = 1
    # 部门id，定义可接收消息的成员范围
    PartyID = 1

    # 生成post请求信息
    post_data = {}
    msg_content = {}
    # msg_content['content'] = getMsg()
    post_data['touser'] = 'eagle'
    # post_data['toparty'] = PartyID
    post_data['msgtype'] = 'text'
    post_data['agentid'] = 1
    post_data['text'] = {'content': '%s diff greate than %s, please note!!' % (code, valve)}
    post_data['safe'] = '0'
    # 由于字典格式不能被识别，需要转换成json然后在作post请求
    # 注：如果要发送的消息内容有中文的话，第三个参数一定要设为False
    json_post_data = json.dumps(post_data)

    # 通过requests.urlopen()方法发送post请求
    request_post = requests.post(PURL, json_post_data, verify=False)
    # read()方法查看请求的返回结果
    # print (request_post.read())

def calc(data):
    res = {}
    for index, row in data.iterrows():
        amount = row.s
        t = row.type
        code = row.code
        if code not in res:
            res[code] = {}
            res[code]['diff'] = 0
            if t == 'B':
                res[code]['diff'] += amount
            else:
                res[code]['diff'] -= amount
            res[code][t] = amount
        else:
            if t == 'B':
                res[code]['diff'] += amount
            else:
                res[code]['diff'] -= amount
            res[code][t] = amount

    # print(res)
    final_res = {}
    for x in res:
        if res[x]['diff'] > 0:
            final_res[x] = res[x]['diff']

    sr = sorted(final_res.items(), key=lambda d: -d[1])
    now = datetime.now()
    for x in sr:
        if x[1] > VALVE_AMOUNT and x[0] not in send_map:
            send_msg(x[0], x[1])
            print(x[0], x[1])
            send_map[x] = {}
            send_map[x]['send_at'] = datetime.now()
            send_map[x]['diff'] = x[1]
        elif x[0] in send_map:
            if (now - timedelta(minutes=2)) < send_map[x]['send_at'] or (x[1] - send_map[x]['diff'] > STEP_AMOUNT):
                send_msg(x[0], x[1])
                print(x[0], x[1])
                send_map[x]['send_at'] = datetime.now()
                send_map[x]['diff'] = x[1]


def calc_fun():
    from sqlalchemy import create_engine
    con = create_engine("mysql://admin:admin@%s/stock" % HOST)
    sql_cmd = 'select sum(count*price) as s ,type,code from stock_dadan_history where date="%s" group by type, code order by code, s desc;' % date.today().strftime('%Y-%m-%d')
    # sql_cmd = 'select sum(count*price) as s ,type,code from stock_dadan_history where date="2017-06-27"  group by type, code order by code, s desc;'
    while True:
        try:
            now = datetime.now()
            while now < KP:
                time.sleep(10)
                now = datetime.now()

            while now > LUNCH and now < KP2:
                time.sleep(10)
                now = datetime.now()
            if now > THREE:
                time.sleep(3600)
            print('sleep in sql %s' % datetime.now())
            df_mysql = pd.read_sql(sql_cmd, con=con)
            calc(df_mysql)
            time.sleep(5)
        except Exception as e:
            print(e)
            con = create_engine("mysql://admin:admin@%s/stock" % HOST)
            time.sleep(5)
            continue


if __name__ == '__main__':
    calc_fun()
