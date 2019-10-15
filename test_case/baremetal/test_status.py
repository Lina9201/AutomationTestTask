import json

import pytest
import requests

from baremetal.conftest import the_port, the_ip
from baremetal.excelHandle import excelHandle

ip=the_ip
port=the_port
excel_dir="test_status.xlsx"

# 根据主机名获取主机id
def get_host_id(name, resource_pool_id, token):
    url = "http://%s:%s/admin/v1/hypersivor/baremetal/hosts?pageNum=1&pageSize=10&resource_pool_id=%s" % (
    ip, port, resource_pool_id)
    headers = {"T-AUTH-TOKEN": token}
    r = requests.get(url, headers=headers).json()
    l = r["data"]["list"]
    for i in l:
        if i["name"] == name:
            return i["id"]
    return ""

# 查询主机,返回查询结果
def get_host(name,resource_pool_id,token):
    id=get_host_id(name,resource_pool_id,token)
    url="http://%s:%s/admin/v1/hypersivor/baremetal/hosts/%s?resource_pool_id=%s"%(ip,port,id,resource_pool_id)
    headers = {"T-AUTH-TOKEN": token}
    return requests.get(url,headers)

#设置主机维护模式
@pytest.mark.parametrize("name,resource_pool_id",excelHandle(excel_dir,"test_maintenance"))
def test_maintenance(token,name,resource_pool_id):
    id=get_host_id(name,resource_pool_id,token)
    url="http://%s:%s/admin/v1/hypersivor/baremetal/hosts/%s/maintenance?resource_pool_id=%s"%(ip,port,id,resource_pool_id)
    headers = {"Content-Type":"application/x-www-form-urlencoded",
               "T-AUTH-TOKEN": token}
    r=requests.put(url,headers=headers).json()
    print (r)
    assert r["status"]==200
    assert get_host(name,resource_pool_id,token)["data"]["maintenance"]==True

#取消主机维护模式
@pytest.mark.parametrize("name,resource_pool_id",excelHandle(excel_dir,"test_unmaintenance"))
def test_unmaintenance(token,name,resource_pool_id):
    id=get_host_id(name,resource_pool_id,token)
    url="http://%s:%s/admin/v1/hypersivor/baremetal/hosts/%s/unmaintenance?resource_pool_id=%s"%(ip,port,id,resource_pool_id)
    headers = {"Content-Type":"application/x-www-form-urlencoded",
               "T-AUTH-TOKEN": token}
    r=requests.put(url,headers=headers).json()
    assert r["status"]==200
    assert get_host(name,resource_pool_id,token)["data"]["maintenance"]==False

#查询cmdb物理机
@pytest.mark.parametrize("pagenum,pagesize,names",excelHandle(excel_dir,"test_cmdb"))
def test_cmdb(token,pagenum,pagesize,names):
    url="http://%s:%s/admin/v1/hypersivor/baremetal/hosts/cmdb/items?pageNum=%s&pageSize=%s"%(ip,port,pagenum,pagesize)
    headers = {"T-AUTH-TOKEN": token}
    r=requests.get(url,headers=headers).json()
    assert r["status"]==200
    s=json.dumps(r,ensure_ascii=False)
    l=list(eval(names))
    for i in l:
        assert i in s
