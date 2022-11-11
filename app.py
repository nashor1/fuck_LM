import json
import math
import random
import requests
from flask import Flask, request, redirect, url_for
import BaseConfig as CONSTANT

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
def getaccesstoken():
    url = 'https://api.weixin.qq.com/cgi-bin/token'
    params = {
        'grant_type': 'client_credential',
        'appid': 'wx20976a32c7a2fd75',
        'secret': '1f93042373d4622442e884bbc5dec74e'
    }
    accesstoken = requests.get(url=url, params=params)
    accesstoken = accesstoken.text
    accesstoken = json.loads(accesstoken)
    accesstoken = accesstoken['access_token']
    return accesstoken

def geticket(getaccesstoken):
    url = 'https://api.weixin.qq.com/cgi-bin/ticket/getticket'
    params = {
        'access_token': getaccesstoken,
        'type': 2
    }
    ticket = requests.get(url=url, params=params)
    ticket = ticket.text
    ticket = json.loads(ticket)
    ticket = ticket['ticket']
    return ticket

def getqrcode(geticket):
    import uuid
    import time
    import hashlib
    appid = 'wx20976a32c7a2fd75'
    noncestr = uuid.uuid4()
    timestamp = int(time.time())
    sdk_ticket = geticket
    pre_signature = 'appid={}&noncestr={}&sdk_ticket={}&timestamp={}'.format(appid, noncestr, sdk_ticket, timestamp)
    pre_signature_2 = hashlib.sha1(pre_signature.encode('utf-8'))
    signature = pre_signature_2.hexdigest()
    url = 'https://open.weixin.qq.com/connect/sdk/qrconnect'#https://open.weixin.qq.com/connect/sdk/qrconnect&appid=wx20976a32c7a2fd75&noncestr=79dd4a3e-cb9b-43ea-b1ec-800d6450dd8f&timestamp=1667124209&scope=snsapi_userinfo&signature=841576b1e6fe8c5dd446b20e53da46de7c3b54a4
    params = {
        'appid': appid,
        'noncestr': noncestr,
        'timestamp': timestamp,
        'scope': 'snsapi_userinfo',
        'signature': signature
    }
    qrcode = requests.get(url=url, params=params)
    tmp_qrcode = json.loads(qrcode.text)
    qrcode_base64 = tmp_qrcode['qrcode']['qrcodebase64']
    uid = tmp_qrcode['uuid']
    return [qrcode_base64, uid]

def check_():
    pass

def kepp_qrimg(str,uid):
    from flask import render_template
    img_stream = str
    uuid = uid
    return render_template('index.html',img_stream=img_stream,uuid=uuid)

def kepp_qrimg_morning(str,uid):
    from flask import render_template
    img_stream = str
    uuid = uid
    return render_template('fuck_morning.html',img_stream=img_stream,uuid=uuid)

def index_page():
    from flask import render_template
    return render_template('index1.html')

def _rsa_encrypt(pub_key_str, msg):
    """
    静态方法,根据公钥加密字符串
    :param pub_key_str: 公钥完整
    :param msg: 待加密json文本
    :return:
    """
    import base64
    from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
    from Crypto.PublicKey import RSA
    msg = msg.encode('utf-8')
    length = len(msg)
    default_length = 117
    # default_length = 100
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

def get_user_info_data(code,token):
    import re
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
    data_getinfo_row = data_getinfo_row.replace("'",'"')
    data_getinfo = _rsa_encrypt(pub_key_str,data_getinfo_row)
    data_getinfo = str(data_getinfo)
    reg = re.compile(r"'(.*?)'")
    data_getinfo = re.findall(reg,data_getinfo)
    data_getinfo = data_getinfo[0]
    data_getinfo = str(data_getinfo)
    stunum = requests.post(url=url,headers=header,data=data_getinfo).text
    stunum = json.loads(stunum)
    stuNum = stunum['stuNumber']
    stuName = stunum['stuName']
    return stuNum,stuName

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
        if CONSTANT.RANDOMLOCATION_STRENGETH == False:
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

def get_run_post_data(stuNum, token):
    import datetime
    import random
    import re
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
    start_time = (datetime.datetime.now() + datetime.timedelta(minutes=-random.uniform(18, 22),seconds=-random.uniform(30, 60)))
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
        "avgSpeed": speed,  #################################################################
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
    res = requests.post(url=url, headers=header, data=data).text
    polist = polist_1
    return res

def morning_data(stunum,token):
    global pub_key_str
    import re
    import random
    lougitude = random.uniform(120.474700,120.474800)
    lougitude = str(lougitude)
    latitude = random.uniform(31.583100,31.583300)
    latitude = str(latitude)
    data = {
            "mac":"",
            "pointId":"09",
            "qrCode":"mornsignPlace-2022101800000109",
            "longitude":lougitude,#标准点经度点：120.47472216814754
            "latitude":latitude,#标准纬度点：31.58319574260332
            "baseStation":"",
            "token":token,
            "taskId":"mornsignTaskPaper-20211107000001",
            "faceData":"",
            "stuNumber":stunum,
            "appVersion":"",
            "phoneInfo":"",
            "phoneNumber":""
             }
    data = str(data)
    data = _rsa_encrypt(pub_key_str,data)
    data = str(data)
    reg = re.compile(r"'(.*?)'")
    data = re.findall(reg, data)
    return data

# @app.route('/')
# def index():
#     index_page()
#     return index_page()

# @app.route('/check',methods = ['GET','POST'])
# def check_sword():
#     list = []
#     if request.method == 'POST':
#         Token = request.form.get('sword')
#         Token = str(Token)
#         if len(Token) != 15:
#             return "令牌错误"
#         else:
#             with open("token.txt")as r:
#                 for line in r:
#                     list.append(line.strip())
#         if Token in list:
#             list = []
#             with open("token.txt") as f:
#                 for line in f:
#                     list.append(line.strip())
#             a = list.index(Token)
#             list.pop(a)
#             # print(list)
#             with open('token.txt', 'w') as fp:
#                 [fp.write(str(item) + '\n') for item in list]
#                 fp.close()
#             return """<center>令牌正确<br><form action="/sub" method="POST"><br><p><input type="submit"></p><br><h2>点提交开始fuck龙猫</h2>"""

# @app.route('/sub_morning')
# def sub_morning():
#     a = getaccesstoken()
#     b = geticket(a)
#     c = getqrcode(b)
#     global uid_gobal
#     uid_gobal = c[1]
#     # get_code(c[1])
#     return kepp_qrimg_morning(c[0], c[1])

@app.route('/fuck_morning')
def fuck_morning():
    import re
    url_morning = "https://app.xtotoro.com/app/platform/recrecord/morningExercises"
    global uid_gobal
    uid = uid_gobal
    url = 'https://long.open.weixin.qq.com/connect/l/qrconnect'
    params = {
        'f': 'json',
        'uuid': uid
    }
    callback = requests.get(url=url, params=params)
    tmp_callback = json.loads(callback.text)
    code_ = tmp_callback['wx_code']
    code_ = str(code_)
    code = {"code": code_}
    code = f'"code":"{code.get("code")}"'
    code_data = "{" + code + "}"
    """
    以上构造code的数据包
    """
    data = _rsa_encrypt(pub_key_str, code_data)
    data = str(data)
    reg = re.compile(r"'(.*?)'")
    code_data = re.findall(reg, data)
    code_data = str(code_data)
    url_getoken = "https://app.xtotoro.com/app/platform/serverlist/getLesseeServer"
    token = requests.post(url=url_getoken, headers=header, data=code_data).text
    token = json.loads(token)
    token = token['token']
    token = str(token)
    """
    以上获取token
    """
    stuNum = get_user_info_data(code_, token)
    stuNum = str(stuNum)
    data = str(morning_data(stuNum,token))
    res_morning = requests.post(url=url_morning,headers=header,data=data)
    return res_morning.text

@app.route('/',methods = ['GET','POST'])
def action():  # put application's code here
    # if request.method == 'GET':
    #     return redirect(url_for('index'))
    # if request.method == 'POST':
    #     data = request.form.get('data')
    a = getaccesstoken()
    b = geticket(a)
    c = getqrcode(b)
    global uid_gobal
    uid_gobal = c[1]
    # get_code(c[1])
    return kepp_qrimg(c[0],c[1])

@app.route('/fuck',methods = ['GET'])
def action_getcode():
    from flask import request
    import re
    import datetime
    if request.method == 'GET':
        global uid_gobal
        uid = uid_gobal
        url = 'https://long.open.weixin.qq.com/connect/l/qrconnect'
        params = {
            'f': 'json',
            'uuid': uid
        }
        callback = requests.get(url=url, params=params)
        tmp_callback = json.loads(callback.text)
        code_ = tmp_callback['wx_code']
        code_ = str(code_)
        code = {"code": code_}
        code = f'"code":"{code.get("code")}"'
        code_data = "{" + code + "}"
        """
        以上构造code的数据包
        """
        data = _rsa_encrypt(pub_key_str,code_data)
        data = str(data)
        reg = re.compile(r"'(.*?)'")
        code_data = re.findall(reg,data)
        code_data = str(code_data)
        url_getoken = "https://app.xtotoro.com/app/platform/serverlist/getLesseeServer"
        token = requests.post(url=url_getoken,headers=header,data=code_data).text
        token = json.loads(token)
        token = token['token']
        token = str(token)
        """
        以上获取token
        """
        stu_info_list = get_user_info_data(code_,token)
        stuNum = str(stu_info_list[0])
        stuName = str(stu_info_list[1])

        f = open("token.txt", 'r')
        info_list = f.read().splitlines()
        if stuNum in info_list:
            res = get_run_post_data(stuNum,token)
            return res
        else:
            time = datetime.datetime.now()
            time = time.strftime('%Y-%m-%d %H:%M:%S')
            g = open('hack.txt','a',encoding='utf-8')
            g.write(f"{stuName} {stuNum} {time}\n")
            return "<h1>fuck_you_还tm想代跑呢<h1>"

if __name__ == '__main__':
    app.run()
