import calendar
import datetime
import json
import os
import random
import re
import time, math

import requests
from lxml import etree
import execjs
from dateutil.relativedelta import relativedelta
from dateutil.rrule import MONTHLY, rrule

cookies = dict()
basicinfo = {}


def enStr(pwd):
    js_path = "%s/enStr.js" % "/".join(os.path.abspath(__file__).split("/")[:-1])
    with open(js_path, 'r') as f:
        js_content = f.read()
        ctx = execjs.compile(js_content)
        new_pwd = ctx.call("enString", pwd)
        return new_pwd


def dnCon(con):
    js_path = "%s/enCon.js" % "/".join(os.path.abspath(__file__).split("/")[:-1])
    with open(js_path, 'r') as f:
        js_content = f.read()
        ctx = execjs.compile(js_content)
        dn_con = ctx.call("uifDecode", con)
        return dn_con


# 获取6个月的年月日
def get_ymd():
    today = datetime.date.today()
    dt_list = []
    for previous_datetime in list(
            rrule(MONTHLY, count=6, bymonthday=-1, dtstart=today + relativedelta(months=-5))):
        year = str(previous_datetime.year)
        month = str(previous_datetime.month).zfill(2)
        day = str(previous_datetime.day).zfill(2)

        dt_list.append((year + month + "01", previous_datetime.strftime("%Y%m%d")))

    # print(dt_list)
    return dt_list


# 获取6个月的年月
def get_ym():
    today = datetime.date.today()
    dt_list = []
    for previous_datetime in list(
            rrule(MONTHLY, count=6, bymonthday=-1, dtstart=today + relativedelta(months=-5))):
        year = str(previous_datetime.year)
        month = str(previous_datetime.month).zfill(2)
        dt_list.append((year + month))
    return dt_list


# 获取6个月的年月日,另一种方法
def flexible_date_range(months=6):
    """
    获取从现在开始几个月后的1号和末号，
    如2018-11-01, 2018-11-30
    :param end_date: 最低结束时间
    :param months: 获取的几个月份，默认6个月
    :return: [(2018-11-01, 2018-11-30), (2018-10-01, 2018-10-31)]
    """
    dt = datetime.date.today().replace(
        day=calendar.monthrange(datetime.date.today().year, datetime.date.today().month)[1])
    dt_list = []
    for i in range(months):
        dt_list.append((dt.strftime("%Y%m%d"), datetime.date(year=dt.year, month=dt.month, day=1).strftime("%Y%m%d")))
        if dt.month == 1:
            dt = datetime.date(year=dt.year - 1, month=12, day=31)
            dt.strftime("%Y%m%d")
        else:
            dt = datetime.date(year=dt.year, month=dt.month - 1, day=calendar.monthrange(dt.year, dt.month - 1)[1])
            dt.strftime("%Y%m%d")
    return dt_list


# 登录
def login():
    # 用户登录信息
    userid = "18855130130"
    password = "008311"

    # 第一次登录请求
    firtst_login = "https://ah.ac.10086.cn/login"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Referer": "https://ah.ac.10086.cn/"
    }
    resp = requests.get(url=firtst_login, headers=headers, verify=False)
    cookies.update(resp.cookies.get_dict())

    # # 获取跳转链接，进行请求，并获取spid
    # url = re.findall(r'replace\(\'(.*)\'\);', resp.text)[0]
    # headers = {
    #     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
    #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    #     "Referer": "https://ah.ac.10086.cn/login"
    # }
    # resp = requests.get(url=url, headers=headers, verify=False, cookies=cookies)
    # cookies.update(resp.cookies.get_dict())
    #
    # print(resp.text)
    #
    #
    # print(cookies)
    # # 获取spid
    # et = etree.HTML(resp.text)
    # spid_list = et.xpath("//*[@name='spid']/@value")
    # spid = spid_list[0]
    #
    # print(spid)

    # # 获取图片验证码
    # captcha_url = "https://ah.ac.10086.cn/common/image.jsp".format(random.random())
    # resp = requests.get(captcha_url, verify=False, cookies=cookies)
    # # cookies.update(resp.cookies.get_dict())
    # list_b64_captcha = re.compile("imageCallBack\('.*,(.*)'\);").findall(resp.text)
    # b64_captcha = list_b64_captcha[0]
    # print(b64_captcha)
    # captcha_code = input('please input captcha....')
    #
    # # 获取加密后的密码,登录
    # login_url = "https://ah.ac.10086.cn/Login"
    # login_data = {
    #     "type": "B",
    #     "formertype": "B",
    #     # "backurl": "http://service.ah.10086.cn/LoginSso",
    #     # "backurlflag": "https://ah.ac.10086.cn/4login/backPage.jsp",
    #     # "errorurl": "https://ah.ac.10086.cn/4login/errorPage.jsp",
    #     "spid": spid,
    #     # "RelayState": '',
    #     # "login_type_ah": '',
    #     "mobileNum": userid,
    #     "login_pwd_type": "2",
    #     # "loginBackurl": '',
    #     "loginType": "0",
    #     "timestamp": str(time.time() * 1000),
    #     "validCode": captcha_code,
    #     "servicePassword": enStr(password),
    #     "servicePassword_1": password,
    #     # "smsValidCode": '',
    #     "validCode_state": True
    # }
    # resp = requests.post(url=login_url, data=login_data, verify=False, cookies=cookies)
    # cookies.update(resp.cookies.get_dict())
    #
    # # 登录成功后，获取跳转链接，并获取SAMLart
    # login_headers = {
    #     "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
    #     "Host": "login.10086.cn"
    # }
    # temp_url = re.search("location.replace\('(\S+)'\);</script>", resp.text).group(1)
    # resp = requests.get(url=temp_url, headers=login_headers, verify=False, cookies=cookies)
    # SAMLart = re.search("SAMLart=(.+?)&", resp.url).group(1)
    #
    # # 刷新cookie,登录结束
    # temp_data = {
    #     'SAMLart': SAMLart,
    #     'RelayState': ''
    # }
    # resp = requests.post('http://service.ah.10086.cn/LoginSso', data=temp_data, cookies=cookies)
    # cookies.update(resp.cookies.get_dict())
    #
    # print(cookies)

    # get_info()


# 查询个人信息
def get_info():
    info_url = "http://service.ah.10086.cn/userInfo/qryUserinfo?_={}".format(time.time() * 1000)
    resp = requests.get(info_url, cookies=cookies)
    info_json_response = json.loads(resp.text)

    userStatus = dnCon(info_json_response.get('object', {}).get('run_name', ''))  # 用户状态
    openDate = dnCon(info_json_response.get('object', {}).get('open_time', ''))  # 开户时间 YY-mm-dd
    certification = dnCon(info_json_response.get('object', {}).get('user_appr_info', ''))  # 实名认证
    starLevel = dnCon(info_json_response.get('object', {}).get('star_level', ''))  # 星级
    basicinfo['userStatus'] = userStatus
    basicinfo['openDate'] = openDate
    basicinfo['certification'] = certification
    basicinfo['starLevel'] = starLevel
    print(json.dumps(basicinfo))


# 解析交费记录
def get_pay():
    dt_list = get_ymd()
    paylist = []
    for dt in dt_list:
        beginDate = dt[0]
        endDate = dt[1]
        pay_url = "http://service.ah.10086.cn/qry/qryPayHisInfo?beginDate={}&endDate={}".format(beginDate, endDate)
        resp = requests.get(pay_url, cookies=cookies)
        info_json_response = json.loads(resp.text)
        if info_json_response.get("retCode") == "000000":
            payInfoList = info_json_response.get("object").get("payInfoList")
            for payInfo in payInfoList:
                # yy-mm-dd hh:ff:ss
                paydic = {}
                payDate = payInfo['optDate']
                payFee = payInfo['chargeSum']
                payChannel = payInfo['remark']
                payType = payInfo['payPathName']

                paydic['payDate'] = payDate
                paydic['payFee'] = payFee
                paydic['payChannel'] = payChannel
                paydic['payType'] = payType
                paylist.append(paydic)

    print(json.dumps(paylist))


# 解析套餐信息
def get_taocan():
    huafei_url = "http://service.ah.10086.cn/qry/qryTaocanxx?_={}".format(time.time() * 1000)
    resp = requests.get(huafei_url, cookies=cookies)
    info_json_response = json.loads(resp.text)
    curPlanName = info_json_response.get("object").get("ordInfoList")[0].get("prodPrcName")
    basicinfo['curPlanName'] = curPlanName
    print(json.dumps(basicinfo))


# 解析话费 积分
def get_jifenhuafei():
    jifen_url = "http://service.ah.10086.cn/qry/qryMonthBillIndex?beginDate=&_={}".format(time.time() * 1000)
    resp = requests.get(jifen_url, cookies=cookies)
    info_json_response = json.loads(resp.text)

    score = info_json_response.get("balanceInfo").get("jfAcc")
    realCharge = info_json_response.get("balanceInfo").get("currAcc")
    balance = info_json_response.get("balanceInfo").get("balanceDetailInfoList")[0].get("feeNumber")
    brandName = info_json_response.get("headInfo").get("brandName")

    basicinfo['score'] = score
    basicinfo['realCharge'] = realCharge
    basicinfo['balance'] = balance
    basicinfo['brandName'] = brandName
    print(json.dumps(basicinfo))


# 解析账单
def get_zhangndan():
    dt_list = get_ym()
    billlist = []
    for dt in dt_list:
        zhangdan_url = "http://service.ah.10086.cn/qry/qryMonthBillIndex?beginDate={}&_={}".format(dt, time.time() * 1000)
        resp = requests.get(zhangdan_url, cookies=cookies)
        info_json_response = json.loads(resp.text)

        billdic = {}
        basicpackageFee = info_json_response.get("feeInfo").get("packageFee")
        voiceFee = info_json_response.get("feeInfo").get("voiceFee")
        netFee = info_json_response.get("feeInfo").get("wlanFee")
        messageFee = info_json_response.get("feeInfo").get("smsFee")
        businessFee = info_json_response.get("feeInfo").get("selfFee")
        otherFee = info_json_response.get("feeInfo").get("otherFee")
        totalFee = info_json_response.get("feeInfo").get("sumFee")

        billdic['basicpackageFee'] = basicpackageFee
        billdic['voiceFee'] = voiceFee
        billdic['netFee'] = netFee
        billdic['messageFee'] = messageFee
        billdic['businessFee'] = businessFee
        billdic['otherFee'] = otherFee
        billdic['totalFee'] = totalFee
        billlist.append(billdic)

    print(json.dumps(billlist))


# 解析详单
def get_call():
    # 发送短信验证码

    ## 先获取yzm_submitId
    yanzheng_url = "http://service.ah.10086.cn/busi/broadbandZQ/getSubmitId?type=billDetailIndex_submitId&_={}".format(time.time() * 1000)
    resp = requests.get(yanzheng_url, cookies=cookies)
    info_json_response = json.loads(resp.text)

    print(info_json_response)

    yzm_submitId = info_json_response.get("object").get("yzm_submitId")
    print(yzm_submitId)

    ## 发送短信验证码
    send_verify_url = "http://service.ah.10086.cn/pub/sendSmPass?opCode=EC20&phone_No=&type=billDetailIndex_submitId&yanzm_submitId={}".format(
        yzm_submitId)
    resp = requests.get(send_verify_url, cookies=cookies)
    info_json_response = json.loads(resp.text)
    print(resp.cookies.get_dict())
    cookies.update(resp.cookies.get_dict())
    print(info_json_response)

    ## 验证短信验证码是否正确
    smPass = input("输入短信验证码:")
    check_sms_url = "http://service.ah.10086.cn/pub/chkSmPass?smPass={}&phone_No=".format(str(smPass))
    resp = requests.get(check_sms_url, cookies=cookies)
    info_json_response = json.loads(resp.text)
    print(resp.cookies.get_dict())
    cookies.update(resp.cookies.get_dict())
    print(cookies)
    print(info_json_response)

    calllist = []

    # 获取通话详单
    dt_list = get_ymd()
    for dt in dt_list[:1]:
        beginDate = dt[0]
        endDate = dt[1]
        call_url = "http://service.ah.10086.cn/qry/qryBillDetailPage?detailType=201&startDate={}&endDate={}&nowPage=1&qryType=".format(
            str(beginDate), str(endDate))
        resp = requests.get(call_url, cookies=cookies)
        info_json_response = json.loads(resp.text)

        # 保存第一页的通话记录
        cdrList = info_json_response.get("object").get("cdrVoice").get("cdrVoiceDetailList")
        for cdr in cdrList:
            calldic = {}
            callDate = cdr.get("callDate")
            callArea = cdr.get("callPlace")
            otherMobile = cdr.get("callPhone")

            ## 这个需要转化成秒
            callDuration = cdr.get("callTime")

            ## 主叫被叫转化成数字
            callType = cdr.get("callType")


            callCost = cdr.get("callFee")
            calldic['callDate']=callDate
            calldic['callArea'] = callArea
            calldic['otherMobile'] = otherMobile
            calldic['callDuration'] = callDuration
            calldic['callType'] = callType
            calldic['callCost'] = callCost
            calllist.append(calldic)


        # 进行翻页
        totalnum = info_json_response.get("object").get("cdrVoice").get("cdrVoiceTotal")
        allpage = math.ceil(int(totalnum) / 50)

        for i in range(1, allpage):
            next_call_url = call_url.replace("nowPage=1", "nowPage={}".format(i + 1))
            resp = requests.get(next_call_url, cookies=cookies)
            info_json_response = json.loads(resp.text)

            cdrList = info_json_response.get("object").get("cdrVoice").get("cdrVoiceDetailList")
            for cdr in cdrList:
                calldic = {}
                callDate = cdr.get("callDate")
                callArea = cdr.get("callPlace")
                otherMobile = cdr.get("callPhone")

                ## 这个需要转化成秒
                callDuration = cdr.get("callTime")

                ## 主叫被叫转化成数字
                callType = cdr.get("callType")
                callCost = cdr.get("callFee")
                calldic['callDate'] = callDate
                calldic['callArea'] = callArea
                calldic['otherMobile'] = otherMobile
                calldic['callDuration'] = callDuration
                calldic['callType'] = callType
                calldic['callCost'] = callCost
                calllist.append(calldic)

    print(json.dumps(calllist))


if __name__ == '__main__':
    login()

    # get_info()
    # get_pay()
    # get_taocan()
    # get_jifenhuafei()
    # get_zhangndan()
    # get_call()
