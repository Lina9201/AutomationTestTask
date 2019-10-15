import pytest
import requests
import xlrd
import xlwt

#定义变量，以下函数都能调用
login_url_path = '/v1/tokens'

#使用@pytest.fixture()，然后在同级别的文件中可以调用def函数
@pytest.fixture()
def ip():
    ip = '172.50.10.42'
    return ip

@pytest.fixture()
def port():
    port = '8000'
    return port

@pytest.fixture()
def login_json():
    login_json = {'authType': "password",
                'params': {'username': "duxiangyu", 'password': "eSXUb22UfzfFT+1L8/LinQ=="}
                }
    return login_json

@pytest.fixture()
def token(ip,port,login_json):
    ip_address = 'http://%s:%s'%(ip,port)
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json;charset=UTF-8',
   }

    login_request = requests.post(url=ip_address+login_url_path,json=login_json,headers=headers)
    login_reponse = login_request.json()
    return login_reponse['data']['key']

@pytest.fixture()
def headers(token):
    headers = {
        "User-Agent": "automation",
        'Content-Type': 'application/json;charset=UTF-8',
        'T-AUTH-TOKEN': token
        }
    return headers

# def readexcel(dataname,Sheetname):
#     #打开excel
#     workboll = xlrd.open_workbook(r'%s' % dataname)
#     # workboll = xlrd.open_workbook(r'D:\测试数据.xlsx')
#
#     #打印页签名
#     print(workboll.sheet_names())
#
#     #打开页签
#     # sheetname = workboll.sheet_by_name("Sheet1")
#     sheetname = workboll.sheet_by_name(Sheetname)
#     #获取行数
#     nrows = sheetname.nrows
#
#     #获取列数
#     ncols = sheetname.ncols
#
#     #打印行数和列数
#     print(nrows,ncols)
#
#     sheetvlaues = []
#     sheetvlauesa = []
#
#     for i in range(1,nrows):
#         for j in range(ncols):
#             sheetvlauesa.append(sheetname.cell(i, j).value)
#         sheetvlaues.append(tuple(sheetvlauesa))
#         sheetvlauesa = []
#     return sheetvlaues
    # print(sheetvlaues)
# print(readexcel("D:\测试数据.xlsx","Sheet1"))










