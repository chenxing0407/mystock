#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
import requests
import json
import urllib

import ssl

ssl._create_default_https_context = ssl._create_unverified_context

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


if __name__ == '__main__':
    # calc_fun()
    send_msg('001', 1000)