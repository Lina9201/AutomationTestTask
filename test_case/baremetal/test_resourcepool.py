import pytest
import requests

from baremetal.conftest import the_port, the_ip
from excelHandle import excelHandle

ip = the_ip
port = the_port
excel_dir = "../../test_data/test_resourcepool.xlsx"


# 根据资源池名查id
def getresource_pool_id(region, name, token):
    url = "http://%s:%s/admin/v1/resourcepools?region=%s&name=%s&type=baremetal" % (ip, port, region, name)
    headers = {"T-AUTH-TOKEN": token}
    r = requests.get(url, headers=headers).json()
    l = r["data"]
    for i in l:
        if i["name"] == name:
            return i["id"]
    return 0


# 创建资源池
@pytest.mark.parametrize("region,name,type,theip,theport,username,password,protocol", \
                         excelHandle(excel_dir, "test_add_resource_pool"))
def test_add_resource_pool(token, region, name, type, theip, theport, username, password, protocol):
    url = "http://%s:%s/admin/v1/resourcepools" % (ip, port)
    headers = {"Content-Type": "application/json",
               "T-AUTH-TOKEN": token}
    json = {
        "region": int(region),
        "name": name,
        "type": type,
        "ip": theip,
        "port": int(theport),
        "username": username,
        "password": password,
        "extra": {
            "protocol": protocol
        }
    }
    print(json)
    r = requests.post(url, headers=headers, json=json).json()
    print(r)
    assert r["status"] == 200
    assert r["data"]["name"] == name


# 编辑资源池
@pytest.mark.parametrize("region,name,new_name,newtype,new_desc,newip,newport,newproxyip,newproxyport,username", \
                         excelHandle(excel_dir, "test_edit_resource_pool"))
def test_edit_resource_pool(token, region, name, new_name, newtype, new_desc, newip, newport, newproxyip, newproxyport,
                            username):
    url = "http://%s:%s/admin/v1/resourcepools/%s" % (ip, port, str(getresource_pool_id(int(region), name, token)))
    headers = {"Content-Type": "application/json",
               "T-AUTH-TOKEN": token}
    json = {
        "region": int(region),
        "name": new_name,
        "type": newtype,
        "description": new_desc,
        "ip": newip,
        "port": int(newport),
        "proxyIp": newproxyip,
        "proxyPort": int(newproxyport),
        "username": username
    }
    r = requests.put(url, headers=headers, json=json).json()
    assert r["status"] == 200
    assert getresource_pool_id(int(region), new_name, token) != 0


# 修改资源池密码
@pytest.mark.parametrize("region,name,password,oldpassword", excelHandle(excel_dir, "test_change_password"))
def test_change_password(region, token, name, password, oldpassword):
    url = "http://%s:%s/admin/v1/resourcepools/%s/password" % (ip, port, getresource_pool_id(int(region), name, token))
    headers = {"Content-Type": "application/json",
               "T-AUTH-TOKEN": token}
    json = {
        "password": password,
        "oldPassword": oldpassword
    }
    r = requests.put(url, headers=headers, json=json).json()
    assert r["status"] == 200
