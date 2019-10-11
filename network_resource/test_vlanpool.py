import pytest
import requests
from network_resource.conftest import read_excel, read_excel_tuple, read_excel_dic, write_excel

# 路径
## 创建VLAN池
create_vlanpool_url_path = '/admin/v1/vlan_pools/'
## 获取VLAN池
get_vlanpool_url_path = '/admin/v1/vlan_pools/page?tag=TRADITIONAL_VLAN'
## 编辑VLAN池
update_vlanpool_url_path = '/admin/v1/vlan_pools/'
## 删除VLAN池
delete_vlanpool_url_path = '/admin/v1/vlan_pools/'

# 构造测试数据
## 创建VLAN池
param_create_vlanpool = read_excel_tuple('测试数据.xlsx', '创建VLAN池')
## 编辑VLAN池
param_update_vlanpool = read_excel_tuple('测试数据.xlsx', '编辑VLAN池')
## 删除VLAN池
param_delete_vlanpool = read_excel('测试数据.xlsx', '删除VLAN池', 'name')


# 定义函数
## 获取VLAN池列表
def get_vlanpool_list(ip, port, headers):
    ip_address = 'http://%s:%s' % (ip, port)
    vlanpool_list_response = requests.get(
        url=ip_address + get_vlanpool_url_path,
        headers=headers
    ).json()
    vlanpool_list = vlanpool_list_response['data']['list']
    return vlanpool_list


## 获取VLAN池名称
def get_vlanpool_name_list(ip, port, headers):
    vlanpool_name_list = []
    for i in get_vlanpool_list(ip, port, headers):
        vlanpool_name_list.append(i['name'])
    return vlanpool_name_list


## 获取VLAN池ID
def get_vlanpool_id(ip, port, headers, name):
    vlanpool_id = []
    for i in get_vlanpool_list(ip, port, headers):
        if name == i['name']:
            vlanpool_id.append(i['id'])
    return vlanpool_id


# 测试用例
## 创建VLAN池
@pytest.mark.parametrize('name,tag,vlanPoolResourcePoolList,vlanTagStart,vlanTagEnd', param_create_vlanpool)
def test_create_vlanpool(ip, port, headers, name, tag, vlanPoolResourcePoolList, vlanTagStart, vlanTagEnd):
    ip_address = "http://%s:%s" % (ip, port)
    param = {
        'name': name,  # VLAN池名称
        'tag': tag,
        'vlanPoolResourcePoolList': [{'resourcePoolId': 114}],  # 作用域调用资源池ID
        'vlanTagEnd': vlanTagStart,  # 结束VLAN ID
        'vlanTagStart': vlanTagEnd  # 起始VLAN ID
    }
    create_vlanpool_response = requests.post(
        url=ip_address + create_vlanpool_url_path,
        headers=headers,
        json=param
    ).json()
    print(create_vlanpool_response)
    code = create_vlanpool_response['status']
    assert code == 200
    assert name in get_vlanpool_name_list(ip, port, headers)


## 编辑VLAN池
@pytest.mark.parametrize('name,update_name,tag,vlanPoolResourcePoolList,vlanTagStart,vlanTagEnd', param_update_vlanpool)
def test_update_vlanpool(ip, port, headers, name, update_name, tag, vlanPoolResourcePoolList, vlanTagStart, vlanTagEnd):
    ip_address = 'http://%s:%s' % (ip, port)
    vlanpool_id = get_vlanpool_id(ip, port, headers, name)[0]
    param = {
        'id': vlanpool_id,
        'name': update_name,
        'tag': tag,
        'vlanPoolResourcePoolList': [{'resourcePoolId': 114, 'vlanPoolId': vlanpool_id}],
        'vlanTagStart': vlanTagStart,
        'vlanTagEnd': vlanTagEnd
    }
    update_vlanpool_response = requests.put(
        url=ip_address + update_vlanpool_url_path + str(vlanpool_id),
        headers=headers,
        json=param
    ).json()
    code = update_vlanpool_response['status']
    assert code == 200
    assert name not in get_vlanpool_name_list(ip, port, headers)
    assert update_name in get_vlanpool_name_list(ip, port, headers)


## 删除VLAN池
@pytest.mark.parametrize('name', param_delete_vlanpool)
def test_delete_vlanpool(ip, port, headers, name):
    ip_address = 'http://%s:%s' % (ip, port)
    print(name)
    vlanpool_id = get_vlanpool_id(ip, port, headers, name)[0]
    print(get_vlanpool_id(ip, port, headers, name))
    delete_vlanpool_response = requests.delete(
        url=ip_address + delete_vlanpool_url_path + str(vlanpool_id),
        headers=headers
    ).json()
    code = delete_vlanpool_response['status']
    assert code == 200
    assert name not in get_vlanpool_name_list(ip, port, headers)


if __name__ == '__main__':
    pytest.main()
