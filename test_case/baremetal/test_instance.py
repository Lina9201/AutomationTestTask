#前置条件：有名为115的主机且是可使用状态；有id为9bafce63a2314c97abb03dccaddf1d23的镜像
import json

import pytest
import requests

from baremetal.conftest import the_port, the_ip
from baremetal.excelHandle import excelHandle

ip = the_ip
port = the_port
excel_dir = "../../test_data/test_instance.xlsx"


# 根据实例名，返回实例id
def get_instance_id(name, resource_pool_id, token):
    url = "http://%s:%s/admin/v1/instances?start=0&limit=100&resourcePoolId=%s" % (ip, port, resource_pool_id)
    headers = {"T-AUTH-TOKEN": token}
    r = requests.get(url=url, headers=headers).json()
    l = r["data"]["list"]
    for i in l:
        if i["name"] == name:
            return i["id"]
    return ""


# 根据主机ipmi ip返回主机状态
def get_host_status(ipmi_ip, resource_pool_id, token):
    url = "http://%s:%s/admin/v1/hypersivor/baremetal/hosts?pageNum=1&pageSize=10&resourcePoolId=%s" % (
        ip, port, resource_pool_id)
    headers = {"T-AUTH-TOKEN": token}
    r = requests.get(url=url, headers=headers).json()
    print(r)
    list = r["data"]["list"]
    for host in list:
        if host["ipmiIp"] == ipmi_ip:
            return host["hostStatus"]
    return ""


# 根据实例名，返回实例详情（字符串）
def get_instance(name, resource_pool_id, token):
    url = "http://%s:%s/admin/v1/instances/%s" % (ip, port, get_instance_id(name, resource_pool_id, token))
    headers = {"T-AUTH-TOKEN": token}
    r = requests.get(url, headers=headers).json()
    return json.dumps(r, ensure_ascii=False)


# 根据实例名，返回实例详情（字典）
def get_instance_dic(name, resource_pool_id, token):
    url = "http://%s:%s/admin/v1/instances/%s" % (ip, port, get_instance_id(name, resource_pool_id, token))
    headers = {"T-AUTH-TOKEN": token}
    r = requests.get(url, headers=headers).json()
    return r


# 返回实例列表（字符串）
def get_instance_list(token, resource_pool_id):
    url = "http://%s:%s/admin/v1/instances?start=0&limit=100&resourcePoolId=%s" % (ip, port, resource_pool_id)
    headers = {"T-AUTH-TOKEN": token}
    r = requests.get(url=url, headers=headers).json()
    return json.dumps(r, ensure_ascii=False)


# 实例关机
def poweroff(name, token):
    url = "http://%s:%s/admin/v1/instances/powerOff" % (ip, port)
    headers = {"Content-Type": "application/json;charset=UTF-8",
               "T-AUTH-TOKEN": token}
    list = []
    list.append(name)
    json = list
    r = requests.post(url, headers=headers, json=json).json()


# 创建裸金属实例
# 需要确认有可用主机才执行创建实例
@pytest.mark.parametrize("region_id,resource_pool_id,vdc_id,project_id,hypervisor_type,name,description,image_id,os_type,cpu,\
memory,network_id,subnet_id,ip_id,nic_ip,target_id,if_name,ipmi_ip", excelHandle(excel_dir, "test_create_instance"))
def test_create_instance(token, region_id, resource_pool_id, vdc_id, project_id, hypervisor_type, name, description,
                         image_id, \
                         os_type, cpu, memory, network_id, subnet_id, ip_id, nic_ip, target_id, if_name, ipmi_ip):
    url = "http://%s:%s/admin/v1/instances" % (ip, port)
    headers = {"Content-Type": "application/json",
               "T-AUTH-TOKEN": token}
    json = [
        {
            "count": 1,
            "regionId": region_id,
            "resourcePoolId": resource_pool_id,
            "vdcId": vdc_id,
            "projectId": project_id,
            "hypervisorType": hypervisor_type,
            "name": name,
            "description": description,
            "imageId": image_id,
            "osType": os_type,
            "cpu": cpu,
            "memory": memory,
            "osDatastore": "",
            "disks": [
                {
                    "name": "系统盘",
                    "os": True,
                    "size": 40,
                    "type": "",
                    "configs": {
                        "datastore": ""
                    }
                }
            ],
            "nics": [
                {
                    "name": "网卡1",
                    "networkId": network_id,
                    "subnetId": subnet_id,
                    "ipId": ip_id,
                    "ip": nic_ip,
                    "type": "VMXNET 3",
                    "targetId": target_id,
                    "extra": {
                        "ifName": if_name
                    }
                }
            ],
            "placement": {
                "cluster": None,
                "host": None,
                "ipmiIp": ipmi_ip
            }
        }
    ]
    if get_host_status(ipmi_ip, resource_pool_id, token) == "available":
        r = requests.post(url=url, headers=headers, json=json).json()
        assert r["status"] == 200


# 查询实例列表
@pytest.mark.parametrize("resource_pool_id,name", excelHandle(excel_dir, "test_instance_list"))
def test_instance_list(token, resource_pool_id, name):
    url = "http://%s:%s/admin/v1/instances?start=0&limit=100&resourcePoolId=%s" % (ip, port, resource_pool_id)
    headers = {"T-AUTH-TOKEN": token}
    r = requests.get(url=url, headers=headers).json()
    #从实例创建到实例加入实例列表会花些时间，所以要等
    while True:
        if name in str(r):
            break
        r = requests.get(url=url, headers=headers).json()

    assert name in str(r)


# 查询实例
@pytest.mark.parametrize("resource_pool_id,name", excelHandle(excel_dir, "test_get_instance"))
def test_get_instance(token, name, resource_pool_id):
    url = "http://%s:%s/admin/v1/instances/%s" % (ip, port, get_instance_id(name, resource_pool_id, token))
    headers = {"T-AUTH-TOKEN": token}
    r = requests.get(url=url, headers=headers).json()
    d = r["data"]
    assert d["name"] == name


# 关机
@pytest.mark.parametrize("inslist", excelHandle(excel_dir, "test_instance_poweroff"))
def test_instance_poweroff(token, inslist):
    url = "http://%s:%s/admin/v1/instances/powerOff" % (ip, port)
    headers = {"Content-Type": "application/json;charset=UTF-8",
               "T-AUTH-TOKEN": token}
    json = eval(inslist)
    r = requests.post(url, headers=headers, json=json).json()
    assert r["status"] == 200


# 开机
@pytest.mark.parametrize("inslist", excelHandle(excel_dir, "test_instance_poweron"))
def test_instance_poweron(token, inslist):
    url = "http://%s:%s/admin/v1/instances/powerOn" % (ip, port)
    headers = {"Content-Type": "application/json;charset=UTF-8",
               "T-AUTH-TOKEN": token}
    json = eval(inslist)
    r = requests.post(url, headers=headers, json=json).json()
    assert r["status"] == 200


# 重启
@pytest.mark.parametrize("inslist", excelHandle(excel_dir, "test_instance_restart"))
def test_instance_restart(token, inslist):
    url = "http://%s:%s/admin/v1/instances/restart" % (ip, port)
    headers = {"Content-Type": "application/json;charset=UTF-8",
               "T-AUTH-TOKEN": token}
    json = eval(inslist)
    r = requests.post(url, headers=headers, json=json).json()
    assert r["status"] == 200


# 编辑ip,添加与删除
@pytest.mark.parametrize("resource_pool_id,name,network_id,subnet_id,ip_id,the_ip,type",
                         excelHandle(excel_dir, "test_add_ip"))
def test_add_ip(token, resource_pool_id, name, network_id, subnet_id, ip_id, the_ip, type):
    url = "http://%s:%s/admin/v1/instances/%s/nics" % (ip, port, get_instance_id(name, resource_pool_id, token))
    headers = {"Content-Type": "application/json;charset=UTF-8",
               "T-AUTH-TOKEN": token}
    json = {"networkId": network_id, "subnetId": subnet_id, "ipId": ip_id, "ip": the_ip, "targetId": "", "type": type}
    r = requests.post(url=url, headers=headers, json=json).json()
    assert r["status"] == 200
    status = get_instance(name, resource_pool_id, token)
    assert the_ip in status

    # 获取刚添加的ip的id
    status_dic = get_instance_dic(name, resource_pool_id, token)
    nicinfos = status_dic["data"]["nicInfos"]
    id = 0
    for i in nicinfos:
        if i["ip"] == the_ip:
            id = i["id"]
            break

    url = "http://%s:%s/admin/v1/instances/%s/nics/%s" % (ip, port, get_instance_id(name, resource_pool_id, token), id)
    r = requests.delete(url, headers=headers).json()
    assert r["status"] == 200
    assert the_ip not in get_instance(name, resource_pool_id, token)


# 删除实例
@pytest.mark.parametrize("resource_pool_id,name", excelHandle(excel_dir, "test_delete_instance"))
def test_delete_instance(token, resource_pool_id, name):
    url = "http://%s:%s/admin/v1/instances/%s" % (ip, port, get_instance_id(name, resource_pool_id, token))
    headers = {"T-AUTH-TOKEN": token}

    # 保证实例处于关机状态
    status_dic = get_instance_dic(name, resource_pool_id, token)
    if status_dic["data"]["powerStatus"] == "poweredOn":
        poweroff(name, token)

    r = requests.delete(url, headers=headers).json()
    assert r["status"] == 200
    assert name not in get_instance_list(token, resource_pool_id)
