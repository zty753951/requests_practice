
# -*- coding: utf-8 -*-
"""
@author: Zhaoty
"""

import requests
from bs4 import BeautifulSoup
import json
import re
from package_methods.sql_orm import ALMSSQL
import time
import numpy as np

class CHEAT_REASON_REQUEST(object):
        def __init__(self,headers,session_requests):
            self.headers = headers
            self.session_requests = session_requests

        #定义基本请求
        def request_get(self,request_url):
            request_content = self.session_requests.get(
                request_url,
                headers = self.headers
            )
            return request_content

        def request_post(self,request_url,data):
            request_content = self.session_requests.post(
                request_url,
                headers = self.headers,
                data=data
            )
            return request_content
# 主函数

def main():

# 初始化类
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
        # 'Cookie': 'JSESSIONID_COOKIE=a34e4093-9730-4074-ae08-143553368632; td_cookie=160924521'
    }
    session_requests = requests.session()
    req = CHEAT_REASON_REQUEST(header,session_requests)

# 1、初始请求
    url_initial = "http://xinshen.yingu.com/loan/user/toLoginReal?errorInfo=" #初始登陆界面URL
    req.request_get(
        url_initial
    )
# 2、获取验证码
    url_image =  "http://xinshen.yingu.com" + "/loan//api/appImageCode1/img/validate?timestamp=" + str(int(round(time.time() * 1000))) #验证码图片URL
    result_identifying_ = req.request_get(
        url_image
    )

    with open('D:/identifying_code_img/identifiedcode.jpg', 'wb')  as f:
        f.write(result_identifying_.content)

# 3、登陆页面
    url_login = "http://xinshen.yingu.com/loan/user/login" #登陆求取URL
    data = {
        "username": "PC0004273",
        "password": "69m7MIZ7VNMsIkT6",
        "imageCode": input("请输入验证码 : ")
    }
    req.request_post(
        url_login,
        data
    )

# 4、获取子原因为空的进件编号
    ms = ALMSSQL()
    ms.ExecNonQuery("[get_cheat_intoid]")
    sqlrequest = ms.ExecQuery("SELECT  进件编号 FROM 欺诈拒绝子原因表 WHERE 拒绝子原因 IS NULL")
    # print(sqlrequest)
    into_list = np.array(sqlrequest).ravel(order='C')

# 5、请求查询，获取ID等基本信息
    url_maininfo="http://xinshen.yingu.com/loan/workfile/queryCreditIntoInfo"  #获取进件基本信息URL
    for into_app_id in into_list:
        data = {
                    'pageIndex': '1',
                    'pageSize': '15',
                    'selectRowIndex': ' undefined',
                    'intoId': into_app_id
                }

        try:
            result_main = req.request_post(
                url_maininfo,
                data
            )
            soup_main = BeautifulSoup(result_main.content)
            json_main = str(soup_main.find_all('p', )[0])[3:-4]
            dict_main = json.loads(json_main)
            custId = dict_main["data"][0]['custId']
            intoId = dict_main["data"][0]['intoId']
            prodId = dict_main["data"][0]['appProductType']
            custCode = dict_main["data"][0]['custCode']

# 6、获取欺诈子原因

            url_result = 'http://xinshen.yingu.com/loan//antifraudLog/prepareExecute/toQueryPage?operate=hide&processInsId=&custId='+custId+'&intoId='+intoId+'&prodId='+prodId+'&ifshow=hide&bizType=&isUpload=NO&custCode='+custCode #子原因URL
            result_detail = req.request_get(
                url_result
            )
            refuse_lable = BeautifulSoup(result_detail.content).find_all('option', selected="selected")[0]
            result = re.match(r"<[\s\S]+>(\w+)<[\s\S]+>", str(refuse_lable)).group(1)
            updatesql = "update 欺诈拒绝子原因表 set 拒绝子原因='%s' where 进件编号='%s' " % (result, into_app_id)
            ms.ExecNonQuery(updatesql)
            print("进件号 ： %s 抓取成功    ;   原因 ： %s" % (into_app_id, result))
        except:
            pass


if __name__=='__main__':
    main()




