import requests

headers = {
    "Host": "dy.feigua.cn",
    "Connection": "keep-alive",
    "Accept": "*/*",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
    "Referer": "https://dy.feigua.cn/Member",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
}

cookies = {
    # "Hm_lvt_b9de64757508c82eff06065c30f71250": "1578466213",
    # "chl": "key=feigua2",
    # "Hm_lpvt_b9de64757508c82eff06065c30f71250": "1578466225",
    # "_uab_collina": "157846622517020118898476",
    # "ASP.NET_SessionId": "w5nv1jch0majfdmys2pbkvsd",
    # "FEIGUA": "UserId=d8e9d6b1da00c091ecda4f7bbae2c650&NickName=20f3035a43719b9b&checksum=64d4f0d6d205&FEIGUALIMITID=12dbf5f497c64e3690b934b219f721c0",
    "FEIGUAUNIONID": "094ba700f9fcf3715ee415232243cb0fa2eac274a5a9d7f458431a779188cbcf",
}


def search_blogger():
    """
    播主搜索
    """

    key = "尿尿"
    url = f"https://dy.feigua.cn/Blogger/Search?keyword={key}"
    resp = requests.get(url=url, headers=headers, cookies=cookies, verify=False)
    print(resp.text)


def blogger_rank():
    """
    播主排行榜
    """

    # 行业排行榜
    # url = "https://dy.feigua.cn/Rank/Tag"

    # 涨粉排行榜
    url = "https://dy.feigua.cn/Rank/RiseFans"

    # 成长排行榜
    # url = "https://dy.feigua.cn/Rank/GrowingUp"

    # 地区排行榜
    # url = "https://dy.feigua.cn/Rank/Area"

    # 蓝V排行榜
    # url = "https://dy.feigua.cn/Rank/BlueV"

    params = {
        "period": "day",  # week month
        "tag": "全部",  # 切换行业
        "keyword": "",
        "datecode": "20200107",
        "page": "1"
    }

    resp = requests.get(url=url, params=params, headers=headers, cookies=cookies, verify=False)
    print(resp.text)


if __name__ == '__main__':
    # hot_video()
    blogger_rank()
