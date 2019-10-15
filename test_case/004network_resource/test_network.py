import pytest
import requests
from network_resource.conftest import read_excel, read_excel_tuple, read_excel_dic, write_excel

# 路径
## 创建网络
create_network_url_path = '/admin/v1/networks/'
## 获取网络列表
get_network_url_path = '/admin/v1/networks/page/'
## 编辑网络
update_network_url_path = '/admin/v1/networks/'
## 创建子网
create_subnet_url_path = '/admin/v1/subnets?networkId='
## 获取子网列表
get_subnet_url_path = '/admin/v1/subnets/page?networkId='
## 编辑子网
update_subnet_url_path = '/admin/v1/subnets/'
## 删除子网
delete_subnet_url_path = '/admin/v1/subnets/'
## 创建网络对象
create_network_object_url_path = '/admin/v1/network_objects/create?networkId='
## 添加已有网络对象
add_network_object_url_path = '/admin/v1/network_objects/add?networkId='
## 获取网络所对应的资源池信息
get_network_resourcepool_url_path = '/admin/v1/networks/resource_pools/'
## 获取网络所对应的VMware资源池中的分布式交换机
get_network_dvswitch_url_path = '/admin/v1/hypersivor/vmware/dvswitches?resourcePoolId='
## 获取网络已添加对象
get_network_object_url_path = '/admin/v1/network_objects/page?networkId='
## 获取网路所对应的VMware资源池中的端口组
get_network_dvportgroup = '/admin/v1/hypersivor/vmware/dvportgroups?resourcePoolId='
## 删除网络对象
delete_network_object_url_path = '/admin/v1/network_objects/'
## 删除网络
delete_network_url_path = '/admin/v1/networks/'

# 构造测试数据
## 创建网络
param_create_network = read_excel_tuple('网络资源.xlsx', '创建网络')
## 编辑网络
param_update_network = read_excel_tuple('网络资源.xlsx', '编辑网络')
## 创建子网
param_create_subnet = read_excel_tuple('网络资源.xlsx', '创建子网')
## 编辑子网
param_update_subnet = read_excel_tuple('网络资源.xlsx', '编辑子网')
## 删除子网
param_delete_subnet = read_excel_tuple('网络资源.xlsx', '删除子网')
## 创建新对象
param_create_network_object = read_excel_tuple('网络资源.xlsx', '创建新对象')
## 添加已有对象
param_add_network_object = read_excel_tuple('网络资源.xlsx', '添加已有对象')
## 删除对象
param_delete_network_object = read_excel_tuple('网络资源.xlsx', '删除对象')
## 删除网络
param_delete_network = read_excel('网络资源.xlsx', '删除网络', 'network_name')


# 定义函数
## 获取网络列表
def get_network_list(ip, port, headers):
    ip_address = 'http://%s:%s' % (ip, port)
    network_list_response = requests.get(
        url=ip_address + get_network_url_path,
        headers=headers
    ).json()
    network_list = network_list_response['data']['list']
    return network_list


## 获取网络名称
def get_network_name_list(ip, port, headers):
    network_name_list = []
    for i in get_network_list(ip, port, headers):
        network_name_list.append(i['name'])
    return network_name_list


## 获取网络ID
def get_network_id(ip, port, headers, network_name):
    network_id = []
    for i in get_network_list(ip, port, headers):
        if network_name == i['name']:
            network_id.append(i['id'])
    return network_id


## 获取子网列表
def get_subnet_list(ip, port, headers, network_name):
    ip_address = 'http://%s:%s' % (ip, port)
    network_id = get_network_id(ip, port, headers, network_name)[0]
    subnet_list_response = requests.get(
        url=ip_address + get_subnet_url_path + str(network_id),
        headers=headers
    ).json()
    subnet_list = subnet_list_response['data']['list']
    return subnet_list


## 获取子网名称
def get_subnet_name_list(ip, port, hearders, network_name):
    subnet_name_list = []
    for i in get_subnet_list(ip, port, hearders, network_name):
        subnet_name_list.append(i['name'])
    return subnet_name_list


## 获取子网ID
def get_subnet_id(ip, port, headers, network_name, subnet_name):
    subnet_id = []
    for i in get_subnet_list(ip, port, headers, network_name):
        if subnet_name == i['name']:
            subnet_id.append(i['id'])
    return subnet_id


## 获取网络所对应的资源池列表
def get_network_resourcepool_list(ip, port, headers, network_name):
    ip_address = 'http://%s:%s' % (ip, port)
    network_id = get_network_id(ip, port, headers, network_name)[0]
    network_resourcepool_response = requests.get(
        url=ip_address + get_network_resourcepool_url_path + str(network_id),
        headers=headers
    ).json()
    network_resourcepool_list = network_resourcepool_response['data']
    return network_resourcepool_list


## 获取网络所对应的资源池名称列表
def get_network_resourcepool_name_list(ip, port, headers, network_name):
    network_resourcepool_name_list = []
    for i in get_network_resourcepool_list(ip, port, headers, network_name):
        network_resourcepool_name_list.append(i['name'])
    return network_resourcepool_name_list


## 获取网络所对应的资源池ID
def get_network_resourcepool_id(ip, port, headers, network_name, network_resourcepool_name):
    network_resourcepool_id = []
    for i in get_network_resourcepool_list(ip, port, headers, network_name):
        if network_resourcepool_name == i['name']:
            network_resourcepool_id.append(i['id'])
    return network_resourcepool_id


## 获取资源池中分布式交换机列表
def get_dvswitch_list(ip, port, headers, network_name, network_resourcepool_name):
    ip_address = 'http://%s:%s' % (ip, port)
    network_resourcepool_id = get_network_resourcepool_id(ip, port, headers, network_name, network_resourcepool_name)[0]
    network_dvswitch_response = requests.get(
        url=ip_address + get_network_dvswitch_url_path + str(network_resourcepool_id),
        headers=headers
    ).json()
    network_dvswitch_list = network_dvswitch_response['data']
    return network_dvswitch_list


## 获取资源池中分布式交换机名称列表
def get_dvswitch_name_list(ip, port, headers, network_name, network_resourcepool_name):
    network_dvswitch_name_list = []
    for i in get_dvswitch_list(ip, port, headers, network_name, network_resourcepool_name):
        network_dvswitch_name_list.append(i['name'])
    return network_dvswitch_name_list


## 获取资源池中分布式交换机名称列表
def get_dvswitch_id(ip, port, headers, network_name, network_resourcepool_name, dvswitch_name):
    network_dvswitch_id = []
    for i in get_dvswitch_list(ip, port, headers, network_name, network_resourcepool_name):
        if dvswitch_name == i['name']:
            network_dvswitch_id = (i['id'])
    return network_dvswitch_id


## 获取已添加对象列表
def get_object_list(ip, port, headers, network_name):
    ip_address = 'http://%s:%s' % (ip, port)
    network_id = get_network_id(ip, port, headers, network_name)[0]
    object_list_respoons = requests.get(
        url=ip_address + get_network_object_url_path + str(network_id),
        headers=headers
    ).json()
    object_list = object_list_respoons['data']['list']
    return object_list


## 获取已添加对象名称列表
def get_object_name_list(ip, port, headers, network_name):
    object_name_list = []
    for i in get_object_list(ip, port, headers, network_name):
        object_name_list.append(i['objectName'])
    return object_name_list


# 获取已添加网络对象id
def get_object_id(ip, port, headers, network_name, object_name):
    object_id = []
    for i in get_object_list(ip, port, headers, network_name):
        if object_name == i['objectName']:
            object_id.append(i['id'])
    return object_id


## 获取网络所包含资源池中的端口组列表
# def get_network_dvportgroup


# 测试用例
## 创建网络
### 通过选择VLAN池创建网络
@pytest.mark.parametrize('name,type,vlanPoolId,vlanId,category,tagType,description', param_create_network)
def test_create_network(ip, port, headers, name, type, vlanPoolId, vlanId, category, tagType,
                        description):
    ip_address = "http://%s:%s" % (ip, port)
    param = {
        'name': name,
        'type': type,
        'vlanPoolId': vlanPoolId,
        'vlanId': vlanId,
        'category': category,
        'tagType': tagType,
        'description': description
    }
    create_network_response = requests.post(
        url=ip_address + create_network_url_path,
        headers=headers,
        json=param
    ).json()
    code = create_network_response['status']
    assert code == 200
    assert name in get_network_name_list(ip, port, headers)


## 编辑网络
@pytest.mark.parametrize('name,update_name,type,vlanPoolId,vlanTag,category,tagType,description,resourcePoolIds',
                         param_update_network)
def test_update_network(ip, port, headers, name, update_name, type, vlanPoolId, vlanTag, category, tagType, description,
                        resourcePoolIds):
    ip_address = 'http://%s:%s' % (ip, port)
    network_id = get_network_id(ip, port, headers, name)[0]
    param = {
        'id': network_id,
        'name': update_name,
        'type': type,
        "vlanPoolId": vlanPoolId,
        'vlanTag': vlanTag,
        'category': category,
        'tagType': tagType,
        'description': description,
        'resourcePoolIds': [114]
    }
    update_network_response = requests.put(
        url=ip_address + update_network_url_path + str(network_id),
        headers=headers,
        json=param
    ).json()
    code = update_network_response['status']
    assert code == 200
    assert update_name in get_network_name_list(ip, port, headers)


## 创建子网
@pytest.mark.parametrize(
    'network_name,subnet_name,ipProtocol,cidr,isGatewayDisabled,gatewayIp,ipPools,preferredDns,alternateDns',
    param_create_subnet)
def test_create_subnet(ip, port, headers, network_name, subnet_name, ipProtocol, cidr, isGatewayDisabled, gatewayIp,
                       ipPools, preferredDns, alternateDns):
    ip_address = 'http://%s:%s' % (ip, port)
    network_id = get_network_id(ip, port, headers, network_name)[0]
    param = {
        'name': subnet_name,
        'ipProtocol': ipProtocol,
        'cidr': cidr,
        'isGatewayDisabled': isGatewayDisabled,
        'gatewayIp': gatewayIp,
        'ipPools': ipPools,
        'preferredDns': preferredDns,
        'alternateDns': alternateDns
    }
    create_subnet_response = requests.post(
        url=ip_address + create_subnet_url_path + str(network_id),
        headers=headers,
        json=param
    ).json()
    code = create_subnet_response['status']
    assert code == 200
    assert subnet_name in get_subnet_name_list(ip, port, headers, network_name)


## 编辑子网
@pytest.mark.parametrize(
    'network_name,subnet_name,update_subnet_name,isGatewayDisabled,gatewayIp,ipPools,preferredDns,alternateDns',
    param_update_subnet)
def test_update_subnet(ip, port, headers, network_name, subnet_name, update_subnet_name, isGatewayDisabled, gatewayIp,
                       ipPools, preferredDns, alternateDns):
    ip_address = 'http://%s:%s' % (ip, port)
    subnet_id = get_subnet_id(ip, port, headers, network_name, subnet_name)[0]
    param = {
        'name': update_subnet_name,
        'isGatewayDisabled': isGatewayDisabled,
        'gatewayIp': gatewayIp,
        'ipPools': ipPools,
        'preferredDns': preferredDns,
        'alternateDns': alternateDns
    }
    update_subnet_response = requests.put(
        url=ip_address + update_subnet_url_path + str(subnet_id),
        headers=headers,
        json=param
    ).json()
    code = update_subnet_response['status']
    assert code == 200
    assert update_subnet_name in get_subnet_name_list(ip, port, headers, network_name)


## 删除子网
@pytest.mark.parametrize('network_name,subnet_name', param_delete_subnet)
def test_delete_subnet(ip, port, headers, network_name, subnet_name):
    ip_address = 'http://%s:%s' % (ip, port)
    subnet_id = get_subnet_id(ip, port, headers, network_name, subnet_name)[0]
    delete_subnet_response = requests.delete(
        url=ip_address + delete_subnet_url_path + str(subnet_id),
        headers=headers
    ).json()
    code = delete_subnet_response["status"]
    assert code == 200
    assert subnet_name not in get_subnet_name_list(ip, port, headers, network_name)


## 创建网络对象
# @pytest.mark.parametrize('network_name,network_resourcepool_name,resourcePoolType,object_name',
#                          param_create_network_object)
# def test_create_network_object(ip, port, headers, network_name, network_resourcepool_name, resourcePoolType,
#                                object_name):
#     ip_address = 'http://%s:%s' % (ip, port)
#     network_id = get_network_id(ip, port, headers, network_name)[0]
#     network_resourcepool_id = get_network_resourcepool_id(ip, port, headers, network_name, network_resourcepool_name)[0]
#     network_dvswitches_name = get_dvswitch_name_list(ip, port, headers, network_name, network_resourcepool_name)[0]
#     param = {
#         'resourcePoolId': network_resourcepool_id,
#         'resourcePoolType': resourcePoolType,
#         "dvsName": network_dvswitches_name,
#         "name": object_name,
#     }
#     create_network_object_response = requests.post(
#         url=ip_address + create_network_object_url_path + str(network_id),
#         headers=headers,
#         json=param
#     ).json()
#     code = create_network_object_response['status']
#     assert code == 200
#     assert object_name in get_object_name_list(ip, port, headers, network_name)


## 添加已有对象
@pytest.mark.parametrize('network_name,network_resourcepool_name', param_add_network_object)
def test_add_network_object(ip, port, headers,network_name,network_resourcepool_name):
    ip_address = 'http://%s:%s' % (ip, port)
    network_id = get_network_id(ip, port, headers, network_name)[0]
    network_resourcepool_id = get_network_resourcepool_id(ip, port, headers, network_name, network_resourcepool_name)[0]
    objectname = get_object_name_list(ip,port,headers,network_name)[0]
    param = [{
        'objectId': 'dvportgroup-1159',
        'objectName': objectname,
        'resourcePoolId': network_resourcepool_id,
        'resourcePoolType': 'vmware',
        'vlanPoolResourcePoolId': network_resourcepool_id
    }]
    add_network_object_response = requests.post(
        url=ip_address + add_network_object_url_path + str(network_id),
        headers=headers,
        json=param
    ).json()
    code = add_network_object_response['status']
    assert code == 200
    assert objectname in get_object_name_list(ip,port,headers,network_name)


## 删除网络对象
@pytest.mark.parametrize('network_name,object_name', param_delete_network_object)
def test_delete_network_object(ip, port, headers, network_name, object_name):
    ip_address = 'http://%s:%s' % (ip, port)
    object_id = get_object_id(ip, port, headers, network_name, object_name)[0]
    delete_network_object_response = requests.delete(
        url=ip_address + delete_network_object_url_path + str(object_id),
        headers=headers
    ).json()
    code = delete_network_object_response['status']
    assert code == 200
    assert object_name not in get_object_name_list(ip, port, headers, network_name)


## 删除网络
@pytest.mark.parametrize('network_name', param_delete_network)
def test_delete_network(ip, port, headers, network_name):
    ip_address = 'http://%s:%s' % (ip, port)
    print(network_name)
    network_id = get_network_id(ip, port, headers, network_name)[0]

    delete_network_response = requests.delete(
        url=ip_address + delete_network_url_path + str(network_id),
        headers=headers
    ).json()
    code = delete_network_response['status']
    assert code == 200
    assert network_name not in get_network_name_list(ip, port, headers)
