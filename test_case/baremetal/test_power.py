import pytest
import requests

from baremetal.conftest import the_ip, the_port
from baremetal.excelHandle import excelHandle

ip=the_ip
port=the_port
excel_dir="test_power.xlsx"

#根据主机名获取主机id
def get_host_id(name,resource_pool_id,token):
    url="http://%s:%s/admin/v1/hypersivor/baremetal/hosts?pageNum=1&pageSize=10&resource_pool_id=%s"%(ip,port,resource_pool_id)
    headers={"T-AUTH-TOKEN":token}
    r=requests.get(url,headers=headers).json()
    l=r["data"]["list"]
    for i in l:
        if i["name"]==name:
            return i["id"]
    return ""

#查询主机状态
def get_host_status(name,resource_pool_id,token):
    url = "http://%s:%s/admin/v1/hypersivor/baremetal/hosts/%s?resource_pool_id=%s" % \
          (ip, port, get_host_id(name, resource_pool_id, token), resource_pool_id)
    headers = {"T-AUTH-TOKEN": token}
    return requests.get(url=url, headers=headers).json()

#开启电源
@pytest.mark.parametrize("name,resource_pool_id",excelHandle(excel_dir,"test_power_on"))
def test_power_on(name,resource_pool_id,token):
    id=get_host_id(name,resource_pool_id,token)
    url="http://%s:%s/admin/v1/hypersivor/baremetal/hosts/%s/poweron?resource_pool_id=%s"%\
        (ip,port,id,resource_pool_id)
    headers = {"Content-Type": "application/x-www-form-urlencoded",
               "T-AUTH-TOKEN": token}
    r=requests.put(url,headers=headers).json()
    assert r["status"]==200
    status=get_host_status(name,resource_pool_id,token)
    assert status["data"]["powerStatus"]=="power on"

#关闭电源
@pytest.mark.parametrize("name,resource_pool_id",excelHandle(excel_dir,"test_power_off"))
def test_power_off(name,resource_pool_id,token):
    id = get_host_id(name, resource_pool_id, token)
    url="http://%s:%s/admin/v1/hypersivor/baremetal/hosts/%s/poweroff?resource_pool_id=%s"%\
        (ip,port,id,resource_pool_id)
    headers = {"Content-Type": "application/x-www-form-urlencoded",
               "T-AUTH-TOKEN": token}
    r=requests.put(url,headers=headers).json()
    assert r["status"]==200
    status = get_host_status(name, resource_pool_id, token)
    assert status["data"]["powerStatus"] == "power off"

#重启电源
@pytest.mark.parametrize("name,resource_pool_id",excelHandle(excel_dir,"test_reboot"))
def test_reboot(name,resource_pool_id,token):
    id=get_host_id(name,resource_pool_id,token)
    url="http://%s:%s/admin/v1/hypersivor/baremetal/hosts/%s/reboot?resource_pool_id=%s"%\
        (ip,port,id,resource_pool_id)
    headers = {"Content-Type": "application/x-www-form-urlencoded",
               "T-AUTH-TOKEN": token}
    r=requests.put(url,headers=headers).json()
    assert r["status"]==200
    status = get_host_status(name, resource_pool_id, token)
    assert status["data"]["powerStatus"] == "power off"

