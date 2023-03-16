import hashlib
import time
import uuid

import requests

session = requests.Session()


def get_access_token():
    """
    获取微信公众号的access_token
    :return: access_token
    """
    url = 'https://api.weixin.qq.com/cgi-bin/token'
    params = {
        'grant_type': 'client_credential',
        'appid': 'wx20976a32c7a2fd75',
        'secret': '1f93042373d4622442e884bbc5dec74e'
    }
    res = session.get(url=url, params=params).json()
    return res['access_token']


def get_ticket():
    """
    获取微信ticket，用于生成二维码
    :return: ticket
    """
    while True:
        with open('accesstoken.txt', 'r') as f:
            access_token = f.read()
        url = 'https://api.weixin.qq.com/cgi-bin/ticket/getticket'
        params = {
            'access_token': access_token,
            'type': 2
        }
        res = session.get(url=url, params=params).json()
        errcode = res['errcode']
        if errcode == 0:
            ticket = res['ticket']
            break
        elif errcode == 40001 or errcode == 42001:
            access_token = get_access_token()
            with open('accesstoken.txt', 'w') as f:
                f.write(access_token)
        else:
            raise Exception(f"获取ticket失败，错误代码：{errcode}")

    return ticket


def getqrcode(geticket):
    """
    获取微信公众号二维码
    :param geticket: 微信公众号ticket
    :return: 包含二维码base64编码和uuid的列表
    """
    appid = 'wx20976a32c7a2fd75'
    noncestr = str(uuid.uuid4())
    timestamp = int(time.time())
    sdk_ticket = geticket

    # 计算签名
    pre_signature = "appid={}&noncestr={}&sdk_ticket={}&timestamp={}".format(
        appid, noncestr, sdk_ticket, timestamp
    )
    signature = hashlib.sha1(pre_signature.encode('utf-8')).hexdigest()

    # 构造URL和参数
    url = "https://open.weixin.qq.com/connect/sdk/qrconnect"
    params = {
        "appid": appid,
        "noncestr": noncestr,
        "timestamp": timestamp,
        "scope": "snsapi_userinfo",
        "signature": signature,
    }

    # 发送请求，获取二维码
    response = session.get(url=url, params=params)
    # 解析响应，获取二维码的base64编码和uuid
    data = response.json()
    qrcode_base64 = data["qrcode"]["qrcodebase64"]
    uid = data["uuid"]

    return [qrcode_base64, uid]

# t1 = time.time()
# qrcode_base64, uid = getqrcode(get_ticket())
# print(qrcode_base64)
# t2 = time.time()
# print(t2 - t1)
