import base64
import datetime
import hashlib
import json
import math
import os
import random
import re
import time
import uuid

import requests
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.PublicKey import RSA
from flask import Flask, jsonify

import BaseConfig as CONSTANT

"""
pycryptodome
"""
app = Flask(__name__)
uid_gobal = ""
pub_key_str = "-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDU/j+c5FdkEwhSIF9jmw+050iN0/yfjhk/669RyFiG5wu0Adpk3NR2Ikbo2lA+rTBJBx1bpGVGCvMKKQ/pljNUSmJtJaM5ieONFrZD6RhSUbjrNENH89Ks9GGWi+1dkOfdSHNujQilF5oLOIHez1HYmwmlADA29Ux4yb8e4+PtLQIDAQAB\n-----END PUBLIC KEY-----"
header = {
    'Content-Type': 'application/json; charset=utf-8',
    'Accept-Encoding': 'gzip, deflate',
    'User-Agent': 'okhttp/4.9.0'
}
polist = [{
    "longitude": "120.468194",
    "latitude": "31.580517"
}, {
    "longitude": "120.468287",
    "latitude": "31.580629"
}, {
    "longitude": "120.468387",
    "latitude": "31.58065"
}, {
    "longitude": "120.468703",
    "latitude": "31.580654"
}, {
    "longitude": "120.46887",
    "latitude": "31.580656"
}, {
    "longitude": "120.468973",
    "latitude": "31.580478"
}, {
    "longitude": "120.468967",
    "latitude": "31.580153"
}, {
    "longitude": "120.468967",
    "latitude": "31.579732"
}, {
    "longitude": "120.468951",
    "latitude": "31.579673"
}, {
    "longitude": "120.468829",
    "latitude": "31.579618"
}, {
    "longitude": "120.468645",
    "latitude": "31.579563"
}, {
    "longitude": "120.46849",
    "latitude": "31.579545"
}, {
    "longitude": "120.468313",
    "latitude": "31.579563"
}, {
    "longitude": "120.468211",
    "latitude": "31.5796"
}, {
    "longitude": "120.468152",
    "latitude": "31.579829"
}, {
    "longitude": "120.468184",
    "latitude": "31.580526"
}]
polist_1 = [{
    "longitude": "120.468194",
    "latitude": "31.580517"
}, {
    "longitude": "120.468287",
    "latitude": "31.580629"
}, {
    "longitude": "120.468387",
    "latitude": "31.58065"
}, {
    "longitude": "120.468703",
    "latitude": "31.580654"
}, {
    "longitude": "120.46887",
    "latitude": "31.580656"
}, {
    "longitude": "120.468973",
    "latitude": "31.580478"
}, {
    "longitude": "120.468967",
    "latitude": "31.580153"
}, {
    "longitude": "120.468967",
    "latitude": "31.579732"
}, {
    "longitude": "120.468951",
    "latitude": "31.579673"
}, {
    "longitude": "120.468829",
    "latitude": "31.579618"
}, {
    "longitude": "120.468645",
    "latitude": "31.579563"
}, {
    "longitude": "120.46849",
    "latitude": "31.579545"
}, {
    "longitude": "120.468313",
    "latitude": "31.579563"
}, {
    "longitude": "120.468211",
    "latitude": "31.5796"
}, {
    "longitude": "120.468152",
    "latitude": "31.579829"
}, {
    "longitude": "120.468184",
    "latitude": "31.580526"
}]
token_list = []


def get_access_token(session):
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


def get_ticket(session):
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
            return ticket
        elif errcode == 40001 or errcode == 42001:
            access_token = get_access_token(session)
            with open('accesstoken.txt', 'w') as f:
                f.write(access_token)


def getqrcode(geticket, session):
    """
    获取登录二维码
    :param geticket: geticket()函数返回的ticket
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
    t9 = time.time()

    # 解析响应，获取二维码的base64编码和uuid
    data = response.json()
    qrcode_base64 = data["qrcode"]["qrcodebase64"]
    uid = data["uuid"]

    return [qrcode_base64, uid]


def kepp_qrimg(str, uid):
    """
    将二维码和uuid封装到HTML模板中，并返回HTML页面的功能
    :param str: getqrcode()函数返回的二维码base64编码
    :param uid: getqrcode()函数返回的uuid
    :return: 将二维码和uuid封装到HTML模板中，并返回HTML页面的功能
    """
    from flask import render_template
    img_stream = str
    uuid = uid
    return render_template('index.html', img_stream=img_stream, uuid=uuid)


def _rsa_encrypt(pub_key_str, msg):
    """
    静态方法,根据公钥加密字符串
    :param pub_key_str: 公钥完整
    :param msg: 待加密json文本
    :return:
    """

    msg = msg.encode('utf-8')
    length = len(msg)
    default_length = 117
    # 公钥加密
    pubobj = Cipher_pkcs1_v1_5.new(RSA.importKey(pub_key_str))
    # 长度不用分段
    if length < default_length:
        return base64.b64encode(pubobj.encrypt(msg))
    # 需要分段
    offset = 0
    res = []
    while length - offset > 0:
        if length - offset > default_length:
            res.append(pubobj.encrypt(msg[offset:offset + default_length]))
        else:
            res.append(pubobj.encrypt(msg[offset:]))
        offset += default_length
    byte_data = b''.join(res)

    return base64.b64encode(byte_data)


def get_user_info_data(session, code, token):
    """
    获取用户信息
    :param code: getinfo()函数返回的code
    :param token: 从getinfo()函数返回的token
    :return: 用户信息(学号、姓名、手机号）
    """
    url = "https://app.xtotoro.com/app/platform/login/login"
    data_getinfo_row = {
        "code": code,
        "latitude": "39.91639769716885",
        "loginWay": "2",
        "longitude": "116.4102511891155",
        "password": "",
        "phoneNumber": "",
        "token": token
    }
    data_getinfo_row = str(data_getinfo_row)
    data_getinfo_row = data_getinfo_row.replace("'", '"')
    data_getinfo = _rsa_encrypt(pub_key_str, data_getinfo_row)
    data_getinfo = str(data_getinfo)
    reg = re.compile(r"'(.*?)'")
    data_getinfo = re.findall(reg, data_getinfo)
    data_getinfo = data_getinfo[0]
    data_getinfo = str(data_getinfo)
    stunum = session.post(url=url, headers=header, data=data_getinfo).text
    stunum = json.loads(stunum)
    stuNum = stunum['stuNumber']
    stuName = stunum['stuName']
    phoneNumber = stunum['phoneNumber']
    return stuNum, stuName, phoneNumber


class Location:
    def __init__(self, locationArray):
        self.locationArray = locationArray

    def locatRandom(self, node):
        newNode = {}
        longitude = float(node['longitude'])
        latitude = float(node['latitude'])
        longitude = longitude + random.uniform(CONSTANT.RANDOM_LOCATION_LONGITUDE_FLOAT_BEGIN,
                                               CONSTANT.RANDOM_LOCATION_LONGITUDE_FLOAT_END)
        latitude = latitude + random.uniform(CONSTANT.RANDOM_LOCATION_LATITUDE_FLOAT_BEGIN,
                                             CONSTANT.RANDOM_LOCATION_LATITUDE_FLOAT_END)
        newNode['longitude'] = '{:.15f}'.format(longitude)
        newNode['latitude'] = '{:.15f}'.format(latitude)
        return newNode

    def creatNewNode(self, node1, node2):
        '''
        创建新节点
        :param node1:
        :param node2:
        :return:
        '''
        node3 = {}
        node3['longitude'] = (float(node1['longitude']) + float(node2['longitude'])) / 2
        node3['latitude'] = (float(node1['latitude']) + float(node2['latitude'])) / 2
        return node3

    def CalculateDistance(self, node1, node2):
        '''
        用于计算两点间距离，在相距较长的坐标点之间添加坐标点
        :param node1:
        :param node2:
        :return:
        '''
        EARTH_RADIUS = 6378137.0

        def getRad(d):
            return d * math.pi / 180.0

        f = getRad((float(node1['latitude']) + float(node2['latitude'])) / 2)
        g = getRad((float(node1['latitude']) - float(node2['latitude'])) / 2)
        i = getRad((float(node1['longitude']) - float(node2['longitude'])) / 2)

        sg = math.sin(g)
        si = math.sin(i)
        sf = math.sin(f)

        a = EARTH_RADIUS
        fi = 1 / 298.257
        sg = sg * sg
        si = si * si
        sf = sf * sf

        s = sg * (1 - si) + (1 - sf) * si
        c = (1 - sg) * (1 - si) + sf * si

        w = math.atan(math.sqrt(s / c))
        r = math.sqrt(s * c) / w
        d = 2 * w * a
        h1 = (3 * r - 1) / 2 / c
        h2 = (3 * r + 1) / 2 / s
        return d * (1 + fi * (h1 * sf * (1 - sg) - h2 * (1 - sf) * sg))

    def checkDistance(self, node1, node2):
        diastance = self.CalculateDistance(node1, node2)
        if diastance >= CONSTANT.MAX_DISTANCE:
            return True
        else:
            return False

    def increaseNode(self, ):
        '''
        增加节点数,取相邻两节点平均值
        :return:
        '''

        arrBack = self.locationArray[:]
        for i in range(0, len(arrBack)):
            if i == len(arrBack) - 1:
                break
            newnode = self.creatNewNode(arrBack[i], arrBack[i + 1])
            self.locationArray.insert(2 * i + 1, newnode)

    def checkRandomStrength(self):
        if not CONSTANT.RANDOMLOCATION_STRENGETH:
            origin_len = len(self.locationArray)
            if origin_len <= 7:
                return 2
            else:
                return 1
        else:
            return int(CONSTANT.RANDOMLOCATION_STRENGETH)

    def increaseNode_longdistance(self):
        flag = 1
        arrBack = self.locationArray[:]
        for k in range(len(arrBack) - 1):
            node1 = self.locationArray[k]
            node2 = self.locationArray[k + 1]
            res = self.checkDistance(node1, node2)
            if res:
                node3 = self.creatNewNode(node1, node2)
                self.locationArray.insert(self.locationArray.index(node1) + 1, node3)
                flag = 0
        return flag

    def increaseOneCircle(self):
        arr_back = self.locationArray[:]
        for i in arr_back:
            self.locationArray.append(i)

    def getRandomLocation(self):
        newLocationArray = []
        increaseNum = self.checkRandomStrength()
        while increaseNum != 0:
            self.increaseNode()  # 增加节点操作
            increaseNum = increaseNum - 1
        # Logger.INFO("节点增加完成")
        # 检测距离，坐标点距离大于设定值自动添加坐标点

        flag = 0
        times = 0
        # Logger.INFO("当前设置的远距离判定值为"+str(CONSTANT.MAX_DISTANCE)+"最大修饰循环次数为"+str(CONSTANT.DISTANCE_MAX_SEARCH_TIME))
        while flag == 0:
            flag = self.increaseNode_longdistance()
            times = times + 1
            if times == CONSTANT.DISTANCE_MAX_SEARCH_TIME or flag == 1:
                break
        # Logger.INFO("远距离节点修饰完成")
        self.increaseOneCircle()
        # Logger.INFO("圈数增加完成")
        for node in self.locationArray:
            newLocationArray.append(self.locatRandom(node))

        # print(newLocationArray)
        return newLocationArray


def get_run_post_data(session, stuNum, token):
    global polist
    global polist_1
    polist = Location.getRandomLocation(Location(polist))
    stunum = stuNum
    data_time = datetime.date.today()
    data_time_str = str(data_time)
    """
    以上是获取时间
    """
    km_1 = random.uniform(2.1, 2.5)
    km_random = round(km_1, 2)
    km_random_str = str(km_random)
    """
    以上是获取跑步随机数
    """
    step = random.uniform(4000, 4300)
    steps = round(step, )
    """

    """
    time_now = datetime.datetime.now()
    start_time = (datetime.datetime.now() + datetime.timedelta(minutes=-random.uniform(18, 22),
                                                               seconds=-random.uniform(30, 60)))
    usr_time = (time_now - start_time)
    usr_time = str(usr_time)
    usetime = usr_time[0:-7]
    end_time = time_now.strftime("%H:%M:%S")
    start_time = start_time.strftime("%H:%M:%S")
    usetime = "0" + usetime
    usesecond = ((int(usetime[3:5]) * 60 + int(usetime[6:8])) / 3600) / float(km_random_str)
    speed = 1 / usesecond
    speed = str(speed)[0:4]
    """
    跑步速度
    """
    data_raw = {
        "LocalSubmitReason": "",
        "avgSpeed": speed,
        "baseStation": "mcc:460 mnc:0 lac:20706 ci:24832 strength:0",
        "consume": "0",
        "endTime": end_time,
        "evaluateDate": "",
        "fitDegree": "",
        "flag": "1",
        "headImage": "",
        "ifLocalSubmit": "0",
        "km": km_random_str,
        "mac": "44:D3:8F:B9:05:E9",
        "phoneInfo": "CN001/865331303926318/OPPO/PEDM00/10",
        "pointList": polist,
        "routeId": "",
        "runType": "0",
        "schoolId": "13982",
        "sensorString": "",
        "startTime": start_time,
        "steps": steps,
        "stuNumber": stunum,
        "submitDate": data_time_str,
        "taskId": "sunrunTaskPaper-20211107000001",
        "token": token,
        "usedTime": usetime,
        "uuid": "d8b91179-b819-47fc-8045-e934422bb8fa",
        "version": "2.0.4",
        "warnFlag": "0",
        "warnType": ""
    }
    data_raw = str(data_raw)
    data = _rsa_encrypt(pub_key_str, data_raw)
    data = str(data)
    reg = re.compile(r"'(.*?)'")
    data = re.findall(reg, data)
    data = str(data)
    url = "https://app.xtotoro.com/app/platform/recrecord/sunRunExercises"
    res = session.post(url=url, headers=header, data=data).text  #
    polist = polist_1
    return res


def morning_data(stunum, token):
    global pub_key_str
    import re
    import random
    lougitude = random.uniform(120.474700, 120.474800)
    lougitude = str(lougitude)
    latitude = random.uniform(31.583100, 31.583300)
    latitude = str(latitude)
    data = {
        "mac": "",
        "pointId": "09",
        "qrCode": "mornsignPlace-2022101800000109",
        "longitude": lougitude,  # 标准点经度点：120.47472216814754
        "latitude": latitude,  # 标准纬度点：31.58319574260332
        "baseStation": "",
        "token": token,
        "taskId": "mornsignTaskPaper-20211107000001",
        "faceData": "",
        "stuNumber": stunum,
        "appVersion": "",
        "phoneInfo": "",
        "phoneNumber": ""
    }
    data = str(data)
    data = _rsa_encrypt(pub_key_str, data)
    data = str(data)
    reg = re.compile(r"'(.*?)'")
    data = re.findall(reg, data)
    return data


def get_code(session):
    """
    用户扫码登录后，获取用户登录信息
    :return:
    """
    global uid_gobal
    uid = uid_gobal
    url = 'https://long.open.weixin.qq.com/connect/l/qrconnect'
    params = {
        'f': 'json',
        'uuid': uid
    }
    try:
        callback = session.get(url=url, params=params, timeout=3)
        print(callback.text)
    except requests.exceptions.Timeout:

        print('获取用户登录信息失败')
        return None
    tmp_callback = json.loads(callback.text)
    code_ = tmp_callback['wx_code']
    code_data = {
        "code": code_
    }
    code_data_str = json.dumps(code_data)
    encrypted_data = _rsa_encrypt(pub_key_str, code_data_str)
    reg = re.compile(r"'(.*?)'")
    encrypted_data_str = re.findall(reg, str(encrypted_data))[0]
    return encrypted_data_str, code_


@app.route('/fuck_morning')
def fuck_morning():
    with requests.session() as session:
        url_morning = "https://app.xtotoro.com/app/platform/recrecord/morningExercises"
        list1 = get_code(session)
        code_data = list1[0]
        code_ = list1[1]
        url_getoken = "https://app.xtotoro.com/app/platform/serverlist/getLesseeServer"
        token = session.post(url=url_getoken, headers=header, data=code_data).text
        token = json.loads(token)
        token = token['token']
        token = str(token)
        """
        以上获取token
        """
        stu_info_list = get_user_info_data(session, code_, token)
        stuNum = str(stu_info_list[0])
        data = str(morning_data(stuNum, token))
        res_morning = session.post(url=url_morning, headers=header, data=data)
    session.close()
    return jsonify(res_morning)


@app.route('/', methods=['GET', 'POST'])
def action():
    """
    获取二维码的控制函数
    :return:
    """
    t1 = time.time()
    global uid_gobal
    with requests.Session() as session:
        b = get_ticket(session)
        c = getqrcode(b, session)
        uid_gobal = c[1]
    t2 = time.time()
    return kepp_qrimg(c[0], c[1])


@app.route('/fuck', methods=['GET'])
def run_main():
    from flask import request
    if request.method == 'GET':
        with requests.Session() as session:
            t1 = time.time()
            list1 = get_code(session)
            t2 = time.time()
            code_data = list1[0]
            code_ = list1[1]
            session.headers.update(header)
            t3 = time.time()
            token = get_token(session, code_data)
            t4 = time.time()
            t5 = time.time()
            stu_info_list = get_user_info_data(session, code_, token)
            t6 = time.time()
            """
            以上获取token
        
            """
            stuNum = str(stu_info_list[0])
            stuName = str(stu_info_list[1])  # 用于记录用过这个项目跑步人员名字，需要使用的时候再修改
            phoneNumber = str(stu_info_list[2])
            t7 = time.time()
            res = get_run_post_data(session, stuNum, token)  # 传入学号和龙猫token，发送跑步请求包
            t8 = time.time()
            res_json = json.loads(res)  # 解析跑步请求的结果

            # 写入跑步日志
            if res_json['status'] == "00":
                today_str = datetime.date.today().isoformat()  # 获取今天的日期字符串
                with open(os.path.join(os.getcwd(), 'stu.log'), 'a', encoding='utf-8') as f:
                    f.write(f' {stuName} {stuNum} {phoneNumber}\n')
        session.close()
        return jsonify(res)


def get_token(session, code_data):
    url_getoken = "https://app.xtotoro.com/app/platform/serverlist/getLesseeServer"
    token = session.post(url=url_getoken, headers=header, data=code_data).text
    token = json.loads(token)
    return str(token['token'])


@app.route('/refresh_qrcode')
def refresh_qrcode():
    # 重新获取二维码
    global uid_gobal
    with requests.session() as session:
        b = get_ticket(session)
        c = getqrcode(b, session)
        uid_gobal = c[1]
    return c[0]


if __name__ == '__main__':
    app.run(threaded=10, processes=2)
