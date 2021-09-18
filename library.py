# -*- coding: utf-8 -*-
import json
import re
import time
import logging
import os
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import datetime
import threading
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def get_headers(JSESSIONID,route):
    return {
        'Accept-Encoding': 'gzip, deflate',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Connection': 'keep-alive',
        'Accept-Language': 'en-us',
        'cookie' : get_cookies_str(JSESSIONID,route)
    }

def get_cookies_str(JSESSIONID,route):
    return 'JSESSIONID='+JSESSIONID+'; oa_deptid=39375; oa_enc=0ab940e4ec34a0be63feeca8268a9567; oa_name=%E6%9D%8E%E6%B6%9B; oa_uid=56255407; route='+route+'; cookie信息保密'

def func():
    url_auth = 'url信息保密'
    result_auth = requests.request(url=url_auth,method="GET",verify=False,headers=get_headers("",""),allow_redirects=False).headers

    url_seat_index = result_auth['location']
    result_seat_index = requests.request(url=url_seat_index,method="GET",verify=False,headers=get_headers("",re.findall(r"route=(.+?);", result_auth['Set-Cookie'])[0]),allow_redirects=False).headers

    url_user_login = 'url信息保密'
    result_user_login = requests.request(url=url_user_login,method="GET",verify=False,headers=get_headers(re.findall(r"JSESSIONID=(.+?);", result_seat_index['Set-Cookie'])[0],re.findall(r"route=(.+?);", result_seat_index['Set-Cookie'])[0]),allow_redirects=False).headers

    result_seat_index = requests.request(url=url_seat_index, method="GET", verify=False, headers=get_headers(re.findall(r"JSESSIONID=(.+?);", result_user_login['Set-Cookie'])[0],re.findall(r"route=(.+?);", result_user_login['Set-Cookie'])[0]),allow_redirects=False).headers
    JSESSIONID = re.findall(r"JSESSIONID=(.+?);", result_seat_index['Set-Cookie'])[0]
    route = re.findall(r"route=(.+?);", result_seat_index['Set-Cookie'])[0]

    print(JSESSIONID)
    print(route)

    choosen_time = (datetime.datetime.now() + datetime.timedelta(days=+1)).strftime("%Y-%m-%d")
    next_time = datetime.datetime.strptime(
        str(datetime.datetime.now().year) + "-" + str(datetime.datetime.now().month) + "-" + str(datetime.datetime.now().day) + " 21:00:00", "%Y-%m-%d %H:%M:%S")
    timer_start_time = (next_time - datetime.datetime.now()).total_seconds()
    print("选择时间:"+str(choosen_time))


    before_url = 'url信息保密'
    result_before = requests.request(url=before_url, method="GET", verify=False, headers=get_headers(JSESSIONID,route)).text
    token = result_before[(result_before.find('token') + 8):(result_before.find('token') + 40)]
    
    print(str(timer_start_time)+"s后开抢")
    time.sleep(timer_start_time)

    for i in range(10):
        qiangke(choosen_time,JSESSIONID,route,token).start()
        time.sleep(0.1)

    # 获取现在时间
    now_time = datetime.datetime.now()
    # 获取明天时间
    next_time = now_time + datetime.timedelta(days=+1)
    next_year = next_time.date().year
    next_month = next_time.date().month
    next_day = next_time.date().day
    # 获取明天21点时间
    next_time = datetime.datetime.strptime(str(next_year) + "-" + str(next_month) + "-" + str(next_day) + " 20:55:00",
                                           "%Y-%m-%d %H:%M:%S")
    timer_start_time = (next_time - datetime.datetime.now()).total_seconds()
    print(str(timer_start_time)+"s后运行fuc")
    # 定时器,参数为(多少时间后执行，单位为秒，执行的方法)
    timer = threading.Timer(timer_start_time, func)
    timer.start()


class qiangke(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, choosen_time,JSESSIONID,route,token):
        threading.Thread.__init__(self)
        self.choosen_time = choosen_time
        self.JSESSIONID = JSESSIONID
        self.route = route
        self.token = token

    def run(self):
        try:
            get_url = "url信息保密"
            result_get = json.loads(requests.request(url=get_url, method="GET", verify=False, headers=get_headers(self.JSESSIONID,self.route)).text)
            logger.info('运行成功' + str(result_get))
        except Exception as a:
            logger.error('运行失败' + a)
            print("错误:"+a)

if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)  # Log等级总开关

    # 第二步，创建一个handler，用于写入日志文件

    log_path = os.path.dirname(os.getcwd()) + '/logs/'
    log_name = log_path + '139' + '.log'
    logfile = log_name
    fh = logging.FileHandler(logfile, mode='a')
    fh.setLevel(logging.DEBUG)  # 输出到file的log等级的开关

    # 第三步，定义handler的输出格式
    formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    fh.setFormatter(formatter)

    # 第四步，将logger添加到handler里面
    logger.addHandler(fh)
    now_time = datetime.datetime.now()
    next_time = now_time + datetime.timedelta(days=+1)
    next_year = next_time.date().year
    next_month = next_time.date().month
    next_day = next_time.date().day
    # 获取明天20点55
    #next_time = datetime.datetime.strptime(str(next_year) + "-" + str(next_month) + "-" + str(next_day) + " 20:55:00","%Y-%m-%d %H:%M:%S")
    # 获取今晚20点55
    next_time = datetime.datetime.strptime(str(now_time.year) + "-" + str(now_time.month) + "-" + str(now_time.day) + " 20:55:00","%Y-%m-%d %H:%M:%S")

    timer_start_time = (next_time - datetime.datetime.now()).total_seconds()
    print(str(timer_start_time)+"s后运行fuc")
    # 定时器,参数为(多少时间后执行，单位为秒，执行的方法)
    timer = threading.Timer(timer_start_time, func)
    timer.start()


