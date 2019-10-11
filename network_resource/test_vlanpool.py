import pytest
import requests
from network_resource.conftest import read_excel_tuple,read_excel_dic, write_excel

# 路径
## 创建VLAN池
create_vlanpool_url_path = '/admin/v1/vlan_pools'
# ## 获取VLAN池
# get_vlanpool_url_path = "/admin/v1/vlan_pools/page?tag=TRADITIONAL_VLAN"
#
# 构造测试数据
param_create_vlanpool = read_excel_tuple('测试数据.xlsx','创建VLAN池')
# # updatename = "自动创建VLAN池修改"
# #
# # 定义函数
# ## 获取VLAN池列表
# def get_vlanpool_list(ip,port,headers):
#     ip_address = "http://%s:%s" % (ip,port)
#     vlanpoollist_response = requests.get(url=ip_address + get_vlanpool_url_path,
#                                          headers=headers).json()
#     vlanpoollist = vlanpoollist_response["data"]["list"]
#     return vlanpoollist
#
# ## 获取VLAN池名称
# def get_vlanpool_name_list(ip,port,headers):
#     vlanpool_name_list = []
#     for i in get_vlanpool_list(ip,port,headers):
#         vlanpool_name_list.append(i["name"])
#     return vlanpool_name_list

# ## 获取VLAN池ID
# def get_vlanpool_id (ip,port,headers,name):
#     vlanpool_id = []
#     for i in get_vlanpool_list(ip,port,headers):
#         if name == i["name"]:
#             vlanpool_id.append(i["id"])
#     return vlanpool_id
#

# 测试用例
## 创建VLAN池
@pytest.mark.parametrize('name,tag,vlanPoolResourcePoolList,vlanTagStart,vlanTagEnd',param_create_vlanpool)
def test_create_vlanpool(ip,port,headers,name,tag,vlanPoolResourcePoolList,vlanTagStart,vlanTagEnd):
    ip_address = "http://%s:%s" % (ip,port)
    param = {
        "name": name,    #VLAN池名称
        "tag": tag,
        "vlanPoolResourcePoolList": [{"resourcePoolId": 114}],      #作用域调用资源池ID
        "vlanTagEnd": vlanTagStart,      #结束VLAN ID
        "vlanTagStart": vlanTagEnd     #起始VLAN ID
    }
    createvlanpool_response = requests.post(url = ip_address + create_vlanpool_url_path,
                                            headers = headers,
                                            json = param
                                            ).json()
    code = createvlanpool_response["status"]
    assert code == 200
    # assert name in get_vlanpool_name_list(ip,port,headers)
#
# # 编辑VLAN池
# def test_update_vlanpool(ip,port,headers):
#     ip_address = "http://%s:%s" % (ip,port)
#     vlanpool_id = get_vlanpool_id(ip,port,headers,param_vlanpool["name"])[0]
#     param_updatevlanpool = {
#         "id": vlanpool_id,
#         "name": updatename,
#         "tag": "TRADITIONAL_VLAN",
#         "vlanPoolResourcePoolList": [{"resourcePoolId": 114, "vlanPoolId":vlanpool_id}],
#         "vlanTagEnd": 101,
#         "vlanTagStart": 101
#     }
#     update_vlanpool_response = requests.put(url=ip_address + create_vlanpool_url_path + "/" + str(vlanpool_id),
#                                             headers=headers,
#                                             json=param_updatevlanpool
#                                           ).json()
#     code = update_vlanpool_response["status"]
#     assert code == 200
#     assert param_updatevlanpool["name"] in get_vlanpool_name_list(ip,port,headers)
#
#
# # 删除VLAN池
# def test_deletevlanpool(ip,port,headers):
#     ip_address = "http://%s:%s" % (ip,port)
#     vlanpool_id = get_vlanpool_id(ip,port,headers,updatename)
#     deletevlanpool_response = requests.delete(url=ip_address + create_vlanpool_url_path + "/" + str(vlanpool_id[0]),
#                                      headers=headers).json()
#     code =deletevlanpool_response["status"]
#     assert code == 200
#     assert updatename not in get_vlanpool_name_list(ip,port,headers)
#
