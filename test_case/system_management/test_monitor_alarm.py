import requests
import pytest
from config import Conf
import os
from common.get_excel_data import OperationExcleData
import time

# 创建监控组url
create_monitorgroup_url = "/admin/v1/groups"
# 编辑/删除监控组url
update_monitorgroup_url = "/admin/v1/groups/"
# 获取资源url
get_resource_url = "/admin/v1/config_items/ip_props/page?pageSize=1000000000"

testdata_path = Conf.get_testdata_path()
excelFile = testdata_path + os.sep + "监控告警.xlsx"
# 创建监控组
create_monitorgroup_param = OperationExcleData(excelFile, "创建监控组").getcase_tuple()
# 编辑监控组
update_monitorgroup_param = OperationExcleData(excelFile, '编辑监控组').getcase_tuple()
# 删除监控组
delete_monitorgroup_param = OperationExcleData(excelFile, '删除监控组').getcase_tuple()


# 获取监控组列表
def get_monitorgroup_list(uri, headers):
    monitorgroup_list_response = requests.get(
        url=uri + create_monitorgroup_url,
        headers=headers
    ).json()
    monitorgroup_list = monitorgroup_list_response['data']["list"]
    return monitorgroup_list


# 获取组织名称列表
def get_monitorgroup_name_list(uri, headers):
    monitorgroup_name_list = []
    for i in get_monitorgroup_list(uri, headers):
        monitorgroup_name_list.append(i['name'])
    return monitorgroup_name_list


# 获取组织id
def get_monitorgroup_id(uri, headers, init_name):
    for monitorgroup in get_monitorgroup_list(uri, headers):
        if monitorgroup['name'] == init_name:
            return monitorgroup['id']


# 获取待取资源列表
def get_vm_resource_list(uri, headers):
    vm_resource_list_response = requests.get(
        url=uri + get_resource_url,
        headers=headers
    ).json()
    vm_resource_list = vm_resource_list_response['data']["list"]
    return vm_resource_list


# 获取虚拟机key
def get_vm_id(uri, headers, vm_name):
    for vm in get_vm_resource_list(uri, headers):
        if vm['name'] == vm_name:
            return vm['_key']


# 根据监控组名称获取虚拟机列表
def get_fixed_vm_list(uri, headers, name):
    monitorgroup_Id = str(get_monitorgroup_id(uri, headers, name))
    fixed_vm_list_response = requests.get(
        url=uri + update_monitorgroup_url + monitorgroup_Id,
        headers=headers
    ).json()
    assert fixed_vm_list_response["status"] == 200
    fixed_vm_list = fixed_vm_list_response['data']["hosts"]
    return fixed_vm_list


# 获取虚拟机列表
def get_fixed_vm_name_list(uri, headers, name):
    fixed_vm_name_list = []
    for i in get_fixed_vm_list(uri, headers, name):
        fixed_vm_name_list.append(i['name'])
    return fixed_vm_name_list


# 创建监控组
@pytest.mark.smoke
@pytest.mark.run(order=38)
@pytest.mark.parametrize('ID,name,description,userNames,vm_name', create_monitorgroup_param)
def test_create_monitorgroup(uri, headers, ID, name, description, userNames, vm_name):
    time.sleep(120)
    hostkey = str(get_vm_id(uri, headers, vm_name))
    create_monitorgroup_param = {
        "description": description,
        "hostKeys": [hostkey],
        "name": name,
        "userNames": [userNames]
    }
    create_monitorgroup_response = requests.post(
        url=uri + create_monitorgroup_url,
        headers=headers,
        json=create_monitorgroup_param
    ).json()
    assert create_monitorgroup_response['status'] == 200
    # 断言名称在组织列表
    assert name in get_monitorgroup_name_list(uri, headers)


# 编辑监控组
@pytest.mark.smoke_update
@pytest.mark.run(order=12)
@pytest.mark.parametrize('ID,name,description,userNames,vm_name', update_monitorgroup_param)
def test_update_monitorgroup(uri, headers, ID, name, description, userNames, vm_name):
    monitorgroup_Id = str(get_monitorgroup_id(uri, headers, name))
    hostkey = str(get_vm_id(uri, headers, vm_name))
    userName = userNames.split(",")
    update_monitorgroup_param = {
        "description": description,
        "hostKeys": [hostkey],
        "name": name,
        "userNames": userName
    }
    update_monitorgroup_response = requests.put(
        url=uri + update_monitorgroup_url + monitorgroup_Id,
        headers=headers,
        json=update_monitorgroup_param
    ).json()
    assert update_monitorgroup_response['status'] == 200
    # 断言组织在列表里
    assert vm_name in get_fixed_vm_name_list(uri, headers, name)


# 删除监控组
@pytest.mark.smoke_delete
@pytest.mark.run(order=8)
@pytest.mark.parametrize('ID,name', delete_monitorgroup_param)
def test_delete_monitorgroup(uri, headers, ID, name):
    monitorgroup_Id = str(get_monitorgroup_id(uri, headers, name))
    delete_monitorgroup_response = requests.delete(
        url=uri + update_monitorgroup_url + monitorgroup_Id,
        headers=headers).json()
    assert delete_monitorgroup_response["status"] == 200
    # 断言组织已删除
    assert name not in get_monitorgroup_name_list(uri, headers)
