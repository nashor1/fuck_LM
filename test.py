import requests
while True:
    with open('accesstoken.txt', 'r') as f:
        getaccesstoken = f.read()
    url = 'https://api.weixin.qq.com/cgi-bin/ticket/getticket'
    params = {
        'access_token': getaccesstoken,
        'type': 2
    }
    res = requests.get(url=url, params=params).json()
    errcode = res['errcode']
    if errcode != 0:
        url = 'https://api.weixin.qq.com/cgi-bin/token'
        params = {
            'grant_type': 'client_credential',
            'appid': 'wx20976a32c7a2fd75',
            'secret': '1f93042373d4622442e884bbc5dec74e'
        }
        accesstoken = requests.get(url=url, params=params).json()
        accesstoken = accesstoken['access_token']

        with open('accesstoken.txt', 'w') as f:
            f.write(accesstoken)
    else:
        print(res)
        break
        # geticket = res['ticket']
        # print(geticket)