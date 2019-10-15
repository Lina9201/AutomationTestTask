import pytest
import requests

other_url = '/admin/v1/regions'

def test_createdb(ip,port,token,headers):
    # ip_address=ip+port
    ip_address = "http://%s:%s"%(ip,port)

    # url=ip_address
    url = ip_address + other_url

    # 参数/消息体
    param = {'name': "dxy",'description': "dxy"}

    #消息体
    createdb_request=requests.post(url=url,json=param ,headers=headers)

    #将request请求.json转化成json格式，其实就是response响应值
    createdb_response = createdb_request.json()

    #提取响应值中status值code代码为200
    code = createdb_response['status']

    name = createdb_response['data']['name']

    #进行断言assert
    assert code==200

    #调用创建用户中心发送参数来判断param['name']
    assert name==param['name']

