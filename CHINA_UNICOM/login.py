import re
import copy, time

# import execjs
import requests

login_headers = {
    "Host": "uac.10010.com",
    "Upgrade-Insecure-Requests": "1",
    "Accept": "text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01",
    "X-Requested-With":"XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    "Referer": "https://uac.10010.com/portal/homeLoginNew",
    "Accept-Encoding":"gzip, deflate, br",
}


def login():
    """登录函数"""
    mobile = '18680325804'
    inputcode = '116016'

    cookies = dict()

    # 1
    url = 'https://uac.10010.com/portal/mallLogin.jsp'
    cookies["_n3fa_cid"] = 'af0460c93c204049b8cbef2710750ac8'
    cookies["_n3fa_ext"] = 'ft=1547022112'
    cookies["ckuuid"] = '92248ef2de3da7af95f20d7708d7b3af'
    resp = requests.get(url, headers=login_headers, cookies=cookies, verify=False)
    cookies.update(resp.cookies.get_dict())
    print("第一步结束，cookies为：" + str(cookies))

    # 2
    time_random1 = int(time.time())
    cookies['_n3fa_lvt_a9e72dfe4a54a20c3d6e671b3bad01d9'] = str(time_random1)
    cookies["_n3fa_lpvt_a9e72dfe4a54a20c3d6e671b3bad01d9"] = str(time_random1)
    url = f'https://uac.10010.com/oauth2/genqr?timestamp={time_random1}'
    resp = requests.get(url, headers=login_headers, cookies=cookies, verify=False)
    set_cookie = resp.headers['Set-Cookie']
    unisecid = re.match(r"unisecid=(.*?);", set_cookie).group(1)
    cookies["unisecid"] = unisecid
    cookies.update(resp.cookies.get_dict())
    print("第二步结束，cookies为：" + str(cookies))

    # 3
    time_random1 = int(round(time.time() * 1000))
    time_random2 = int(round(time.time() * 1000))
    url = f'https://uac.10010.com/portal/Service/CheckNeedVerify?callback=jQuery172008324740139230613_{time_random1}&userName={mobile}&pwdType=02&_={time_random2}'
    resp = requests.get(url, headers=login_headers, cookies=cookies, verify=False)
    cookies.update(resp.cookies.get_dict())
    print("第三步结束，cookies为：" + str(cookies))

    # 4
    time_random1 = int(round(time.time() * 1000))
    url = f"https://uac.10010.com/portal/Service/CreateImage?t={time_random1}"
    resp = requests.get(url, headers=login_headers, cookies=cookies, verify=False)
    set_cookie = resp.headers['Set-Cookie']
    uacverifykey = re.match(r"uacverifykey=(.*?);", set_cookie).group(1)
    cookies["uacverifykey"] = uacverifykey
    cookies.update(resp.cookies.get_dict())
    imgcode = input('please input code....')
    print("第四步结束，cookies为：" + str(cookies))

    # 5 发送短信
    time_random1 = int(round(time.time() * 1000))
    time_random2 = int(round(time.time() * 1000))
    url = f"https://uac.10010.com/portal/Service/SendMSG?callback=jQuery17208646775143324394_{time_random1}&req_time=1569386404395&mobile={mobile}&_={time_random2}"
    resp = requests.get(url, headers=login_headers, cookies=cookies, verify=False)
    cookies.update(resp.cookies.get_dict())
    smscode = input('please input code....')
    print("第五步结束，cookies为：" + str(cookies))

    # 6 验证登录
    time_random1 = int(round(time.time() * 1000))
    time_random2 = int(round(time.time() * 1000))
    time_random3 = int(round(time.time() * 1000))
    url = f"https://uac.10010.com/portal/Service/MallLogin?callback=jQuery172023822205245500538_{time_random1}&req_time={time_random2}&redirectURL=http%3A%2F%2Fwww.10010.com&userName={mobile}&password={smscode}&pwdType=02&productType=01&verifyCode={imgcode}&uvc={uacverifykey}&redirectType=01&rememberMe=1&_={time_random3}"
    resp = requests.get(url, headers=login_headers, cookies=cookies, verify=False)
    cookies.update(resp.cookies.get_dict())
    print("第六步结束，cookies为：" + str(cookies))

    # # 5 电话详单
    # url = "https://iservice.10010.com/e3/static/check/checklogin/?_=1570502413393"
    # resp = requests.post(url, headers=login_headers, cookies=cookies, verify=False)
    # cookies.update(resp.cookies.get_dict())
    # print("第五步结束，cookies为：" + str(cookies))
    #
    # # 6
    # url = "https://iservice.10010.com/e3/static/query/verificationSms?_=1569386602280&accessURL=https://iservice.10010.com/e4/query/bill/call_dan-iframe.html&menuid=000100030001"
    # data = {
    #     "menuId": "000100030001"
    # }
    # resp = requests.post(url, headers=login_headers, data=data, cookies=cookies, verify=False)
    # cookies.update(resp.cookies.get_dict())
    # print("第六步结束，cookies为：" + str(cookies))
    #
    # # 7
    # url = "https://iservice.10010.com/e3/static/query/verificationSubmit_num?_=1569386947924&accessURL=https://iservice.10010.com/e4/query/bill/call_dan-iframe.html&menuid=000100030001"
    # data = {
    #     "inputcode": inputcode,
    #     "menuId": "000100030001"
    # }
    # resp = requests.post(url, headers=login_headers, data=data, cookies=cookies, verify=False)
    # cookies.update(resp.cookies.get_dict())
    # print("第七步结束，cookies为：" + str(cookies))
    #
    # # 8
    # url = "https://iservice.10010.com/e3/static/query/callDetail?_=1569386948777&accessURL=https://iservice.10010.com/e4/query/bill/call_dan-iframe.html&menuid=000100030001"
    # data = {
    #     "pageNo": 1,
    #     "pageSize": 20,
    #     "beginDate": "20191001",
    #     "endDate": "20191008"
    # }
    # resp = requests.post(url, headers=login_headers, data=data, cookies=cookies, verify=False)
    # print(resp.text)
    # print("第八步结束，cookies为：" + str(cookies))


if __name__ == '__main__':
    login()
