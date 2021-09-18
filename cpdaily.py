# -*_coding:utf8-*-
import json
import smtplib
import time
from email.header import Header
from email.mime.text import MIMEText
import requests

receivers = ''
Cpdaily_Extension = "64JITpWPkKtjP5T9L7UUY4Y/six++si3w2LaF+yPT3afebfNHamukIeeF5tc kit/x6domXkwn70Q8VbsNUfTMQsGR/rHLAZ095BEAg2STpHVXFq2CsuoIdgg wFhEuB+EP8MIzC8MSPHIVv1I8DCh7vvwllvxJ6JkXxe47V6AsnACgR8NW47H UTv08SJCQbGMaKGVVYmeTJi4bEV5/xNk2WdJNoGLfaO/6/PTK43Sc6aVFDU2 lmSODKybeZyfNyNg/zkYtXssz2eFpia4h4u0fjHhGhhu2A3D"
cookies = {
    'HWWAFSESID' : '',
    'MOD_AUTH_CAS': ''
}
title = ['']
address = "地址保密"

smtp_server = 'smtp.qq.com'
host = ''
sender = ''
password1 = ''
def submit():
    while True:
        server = requests.session()
        # 携带cookie查询最新待提交表单
        queryCollectWidUrl = host+'/wec-counselor-collector-apps/stu/collector/queryCollectorProcessingList'
        headers = {
            'Content-Type': 'application/json;charset=UTF-8'
        }
        keepUrl = host+'/portal/index.html'
        server.get(keepUrl,cookies=cookies)
        params = {
            'pageSize': 6,
            'pageNumber': 1
        }
        res = server.post(queryCollectWidUrl, headers=headers, cookies=cookies, data=json.dumps(params))
        if len(res.json()['datas']['rows']) < 1:
            print("当前暂无问卷提交任务(是否已完成)"+res.text)
            time.sleep(1*60*60)
            continue
        row = res.json()['datas']['rows'][0]
        if row['isHandled'] == 1:
            print("今日已经填写")
            #time.sleep(1 * 60 * 60)
            #continue
        collectWid = res.json()['datas']['rows'][0]['wid']
        formWid = res.json()['datas']['rows'][0]['formWid']
        res = requests.post(url=host+'/wec-counselor-collector-apps/stu/collector/detailCollector',
                            headers=headers, cookies=cookies, data=json.dumps({"collectorWid": collectWid}))
        schoolTaskWid = res.json()['datas']['collector']['schoolTaskWid'] # 这里也可抓包获取
        res = requests.post(url=host+'/wec-counselor-collector-apps/stu/collector/getFormFields',
                            headers=headers, cookies=cookies, data=json.dumps(
                {"pageSize": 30, "pageNumber": 1, "formWid": formWid, "collectorWid": collectWid})) # 当前我们需要问卷选项有21个，pageSize可适当调整
        print(res.json())
        form = res.json()['datas']['rows']
        for i in range(len(form)):
            if len(title)==len(form) and title[i] == form[i]['title']:
                if len(form[i]['fieldItems']) != 0:
                    cur = [form[i]['fieldItems'][0]]
                    form[i]['fieldItems'] = cur
                    form[i]['value'] = form[i]['fieldItems'][0]['itemWid']
                    form[i]['fieldItems'][0]['isSelected'] = 1
                else:
                    form[i]['value'] = '36.6'
            else:
                print(str(i)+"今天问题和昨天的问题不一样，为防止出错，请联系")
                time.sleep(1 * 60 * 60)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.4; OPPO R11 Plus Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/33.0.0.0 Safari/537.36 okhttp/3.12.4',
            'CpdailyStandAlone': '0',
            'extension': '1',
            'Cpdaily-Extension': Cpdaily_Extension,
            'Content-Type': 'application/json; charset=utf-8',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip'
        }
        # 地址根据学校要求填写即可
        params = {"formWid": formWid, "address": address,
                  "collectWid": collectWid, "schoolTaskWid": schoolTaskWid,
                  "form": form,"uaIsCpadaily":"true"
        }

        r = server.post(host+"/wec-counselor-collector-apps/stu/collector/submitForm",
                        headers=headers, cookies=cookies, data=json.dumps(params))
        msg = r.json()['message']

        if msg == 'SUCCESS':
            print('今日提交成功！24小时后，脚本将再次自动提交')
            message = '今日提交成功！24小时后，脚本将再次自动提交'
            mail(message)
            time.sleep(1 * 60 * 60)
            continue
        else:
            print('失败' + r.text)
            message = '出错了，请联系，错误如下 ' + r.text
            mail(message)
            time.sleep(1 * 60 * 60)
            continue
def mail(msg):
    message = MIMEText(msg, 'plain', 'utf-8')
    message['From'] = Header(sender, 'utf-8')  # 发送者
    message['To'] = Header(receivers, 'utf-8')  # 接收者
    message['Subject'] = Header("今日校园打卡情况推送-"+time.strftime('%m-%d %H:%M', time.localtime(time.time())), 'utf-8')
    server = smtplib.SMTP_SSL(smtp_server, 465)
    server.login(sender, password1)
    server.sendmail(sender, receivers, message.as_string())
    server.quit()
if __name__ == '__main__':
    try:
        submit()
    except Exception as e:
        print(e)
        mail("程序异常%s"%e)
        exit(-1)
