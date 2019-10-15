import requests
# from TCRCauto.conftest import readexcel

#URL地址
##登录的URL
login_url_path = '/v1/tokens'


# 定义变量
ip = '172.50.10.42'
port = '8000'
login_json = {'authType': "password",'params': {'username': "duxiangyu", 'password': "eSXUb22UfzfFT+1L8/LinQ=="}}
headers = { 'Accept': 'application/json, text/plain, */*', 'Content-Type': 'application/json;charset=UTF-8',}
ip_address = 'http://%s:%s' % (ip, port)
login_request = requests.post(url=ip_address + login_url_path, json=login_json, headers=headers)
login_reponse = login_request.json()
token = login_reponse['data']['key']
headers = {"User-Agent": "automation",'Content-Type': 'application/json;charset=UTF-8','T-AUTH-TOKEN': token}

# aaa = {"data":[{"id":"119"}]}
# print(aaa)
# print(type(aaa))
# bbb = aaa["data"][0]["id"]
# print(bbb)
# print(type(bbb))
# ccc = "hahh" + str(bbb)
# print(ccc)
# print(type(ccc))



