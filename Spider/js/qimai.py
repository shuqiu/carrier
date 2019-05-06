import requests, os, execjs, json

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
}

cookies = dict()


def getanaly(synct, params):
    js_path = "%s/qimai.js" % "/".join(os.path.abspath(__file__).split("/")[:-1])
    with open(js_path, 'r') as f:
        js_content = f.read()
        ctx = execjs.compile(js_content)
        new_pwd = ctx.call("get0analysis", synct, params)
        return new_pwd


def qimai():
    resp = requests.get('https://www.qimai.cn/rank', headers=headers, verify=False)
    cookies.update(resp.cookies.get_dict())
    synct = cookies.get('synct')

    for i in range(3):
        params = {
            'brand': 'all',
            'country': 'cn',
            'device': 'iphone',
            'genre': '5000',
            'date': '2019-04-17',
            'page': 2 # 这里写1也是可以的
        }
        url = "https://api.qimai.cn/rank/indexPlus/brand_id/" + str(i)
        analy_list = getanaly(synct, params)
        params['analysis'] = analy_list[i]
        resp = requests.get(url=url, params=params, headers=headers, verify=False, cookies=cookies)
        resjson = json.loads(resp.text)
        contents = resjson['list']
        for content in contents:
            appInfo = content['appInfo']
            print(appInfo)


if __name__ == '__main__':
    qimai()
