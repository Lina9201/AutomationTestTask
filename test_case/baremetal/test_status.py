#前置条件：有名为115的主机，且未处于维护模式
import time

import pytest
import requests

from baremetal.conftest import the_port, the_ip
from baremetal.excelHandle import excelHandle
from test_power import get_host_status

ip = the_ip
port = the_port
excel_dir = "../../test_data/test_status.xlsx"


# 根据主机名获取主机id
def get_host_id(name, resource_pool_id, token):
    url = "http://%s:%s/admin/v1/hypersivor/baremetal/hosts?pageNum=1&pageSize=10&resourcePoolId=%s" % (
        ip, port, resource_pool_id)
    headers = {"T-AUTH-TOKEN": token}
    r = requests.get(url, headers=headers).json()
    l = r["data"]["list"]
    for i in l:
        if i["name"] == name:
            return i["id"]
    return ""


# 查询主机,返回查询结果
def get_host(name, resource_pool_id, token):
    id = get_host_id(name, resource_pool_id, token)
    url = "http://%s:%s/admin/v1/hypersivor/baremetal/hosts/%s?resourcePoolId=%s" % (ip, port, id, resource_pool_id)
    headers = {"T-AUTH-TOKEN": token}
    r=requests.get(url, headers=headers).json()
    return r


# 设置主机维护模式
@pytest.mark.parametrize("name,resource_pool_id", excelHandle(excel_dir, "test_maintenance"))
def test_maintenance(token, name, resource_pool_id):
    id = get_host_id(name, resource_pool_id, token)
    # 确保主机是开机状态
    status = get_host_status(name, resource_pool_id, token)
    if status["data"]["powerStatus"] != "power on":
        time.sleep(3)
        status = get_host_status(name, resource_pool_id, token)

    url = "http://%s:%s/admin/v1/hypersivor/baremetal/hosts/%s/maintenance?resourcePoolId=%s" % (
    ip, port, id, resource_pool_id)
    headers = {"Content-Type": "application/x-www-form-urlencoded",
               "T-AUTH-TOKEN": token}
    r = requests.put(url, headers=headers).json()
    assert r["status"] == 200
    dic=get_host(name, resource_pool_id, token)
    assert dic["data"]["maintenance"] == True


# 取消主机维护模式
@pytest.mark.parametrize("name,resource_pool_id", excelHandle(excel_dir, "test_unmaintenance"))
def test_unmaintenance(token, name, resource_pool_id):
    id = get_host_id(name, resource_pool_id, token)
    url = "http://%s:%s/admin/v1/hypersivor/baremetal/hosts/%s/unmaintenance?resourcePoolId=%s" % (
    ip, port, id, resource_pool_id)
    headers = {"Content-Type": "application/x-www-form-urlencoded",
               "T-AUTH-TOKEN": token}
    r = requests.put(url, headers=headers).json()
    assert r["status"] == 200
    assert get_host(name, resource_pool_id, token)["data"]["maintenance"] == False


