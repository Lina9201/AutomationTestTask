import pytest
import requests
from network_resource.conftest import read_excel_dic


# 路径
## 创建网络
create_network_url_path = "/admin/v1/networks"


# 构造测试数据
## 创建网络
param_network = read_excel_dic("测试数据.xlsx","创建网络")
print(param_network)



# ## 获取网络列表
# get_network_url_path = "/admin/v1/networks/page"
# # create_subnet_url_path = "/admin/v1/subnets?networkId="
# # get_subnet_url_path = "/admin/v1/subnets/page?networkId="
# # update_subnet_url_path = "/admin/v1/subnets/"
# # ## 删除子网
# # delete_subnet_url_path = "/admin/v1/subnets/"
# # ## 创建网络对象
# # create_network_objects_url_path = "/admin/v1/network_objects/create?networkId="
# # ## 获取网络所对应的资源池信息
# # get_network_resourcepools_url_path = "/admin/v1/networks/resource_pools/"
# # ## 获取网络所对应的VMware资源池中的分布式交换机
# # get_network_dvswitches_url_path = "/admin/v1/hypersivor/vmware/dvswitches?resourcePoolId="
# # ## 获取网络已添加对象
# # get_network_objects_list = "/admin/v1/network_objects/page?networkId="
# # ## 删除网络对象
# # delete_network_objects_url_path = "/admin/v1/network_objects/"
# # ## 修改子网ip的ip信息状态的路径
# # # update_subnet_ip_status_path = "http://172.50.10.42:8000/admin/v1/subnet_ips/not_used"



# ## 编辑网络
# param_update_network = read_excel_dic("测试数据.xlsx","编辑网络")
#
# # param_subnet = {
# # 	"name": "自动化创建子网",
# # 	"ipProtocol": "IPV4",
# # 	"cidr": "192.168.1.1/24",
# # 	"isGatewayDisabled": "false",
# # 	"gatewayIp": "192.168.1.1",
# # 	"ipPools": "192.168.1.2,192.168.1.200",
# # 	"preferredDns": "114.114.114.114",
# # 	"alternateDns": "115.115.115.115"
# # }
# # update_subnet_name = "自动化创建子网修改"
# # object_name = "自动创建对象8"
# #
# # 定义函数
# ## 获取网络列表
# def get_network_list(ip,port,headers):
#     ip_address = "http://%s:%s" % (ip,port)
#     network_list_response = requests.get(
#         url = ip_address + get_network_url_path,
#         headers=headers
#     ).json()
#     network_list = network_list_response["data"]["list"]
#     return network_list
#
# ## 获取网络名称
# def get_network_name_list(ip,port,headers):
#     network_name_list = []
#     for i in get_network_list(ip,port,headers):
#         network_name_list.append(i["name"])
#     return network_name_list
#
# ## 获取网络ID
# def get_network_id (ip,port,headers,network_name):
#     network_id = []
#     for i in get_network_list(ip,port,headers):
#         if network_name == i["name"]:
#             network_id.append(i["id"])
#     return network_id
#
# # ## 获取子网列表
# # def get_subnet_list(ip,port,headers):
# #     ip_address = "http://%s:%s" % (ip,port)
# #     network_id = get_network_id(ip,port,headers,update_network_name)[0]
# #     subnet_list_response = requests.get(
# #         url = ip_address + get_subnet_url_path + str(network_id),
# #         headers = headers
# #     ).json()
# #     subnet_list = subnet_list_response["data"]["list"]
# #     return subnet_list
# #
# # ## 获取子网名称
# # def get_subnet_name_list(ip,port,hearders):
# #     subnet_name_list = []
# #     for i in get_subnet_list(ip,port,hearders):
# #         subnet_name_list.append(i["name"])
# #     return subnet_name_list
# #
# # ## 获取子网ID
# # def get_subnet_id(ip,port,headers,name):
# #     subnet_id =[]
# #     for i in get_subnet_list(ip,port,headers):
# #         if name == i["name"]:
# #             subnet_id.append(i["id"])
# #     return subnet_id
# #
# # ## 获取已添加对象列表
# # def get_objects_list(ip,port,headers,name):
# #     ip_address = "http://%s:%s" % (ip,port)
# #     network_id = get_network_id(ip,port,headers,name)[0]
# #     object_list_respoons = requests.get(
# #         url = ip_address + get_network_objects_list + str(network_id),
# #         headers = headers
# #     ).json()
# #     object_list = object_list_respoons["data"]["list"]
# #     return object_list
# #
# # ## 获取已添加对象名称列表
# # def get_objects_name_list(ip,port,headers,name):
# #     objects_name_list = []
# #     for i in get_objects_list(ip,port,headers,name):
# #         objects_name_list.append(i["objectName"])
# #     return objects_name_list
# #
# # # 获取已添加网络对象id
# # def get_objects_id(ip,port,headers):
# #     objects_id = []
# #     for i in get_objects_list(ip,port,headers,update_network_name):
# #         if object_name == object_name:
# #             objects_id.append(i["id"])
# #     return objects_id
# #
# # ## 修改子网ip的ip信息状态
# # # def update_subnet_ip_status(ip,port,headers):
# #
# #
# # 测试用例
# ## 创建网络
# ### 通过选择VLAN池创建网络
# @pytest.mark.parametrize("param__network",param_network)
# def test_create_network(ip,port,headers,param__network):
#     ip_address = "http://%s:%s" % (ip,port)
#     create_network_response = requests.post(url = ip_address + create_network_url_path,
#                                             headers = headers,
#                                             json = param__network
#                                             ).json()
#     code = create_network_response["status"]
#     assert code == 200
#     # assert param_network["name"] in get_network_name_list(ip,port,headers)
#
# # 编辑网络
# @pytest.mark.parametrize("param__network",param_network)
# @pytest.mark.parametrize("param__updatenetwork",param_update_network)
# def test_update_network(ip,port,headers,param__network,param__updatenetwork):
#     ip_address = "http://%s:%s" % (ip,port)
#     network_id = str(get_network_id(ip,port,headers,param__network["name"])[0])
#     write_excel("测试数据.xlsx","编辑网络",2,1,network_id)
#     # param_update_network = {
#     #     "category": "BUSINESS",
#     #     "description": "修改后的描述",
#     #     "id": network_id,
#     #     "name": update_network_name,
#     #     "resourcePoolIds": [114],
#     #     "tagType": "OUTER_NET",
#     #     "type": "VLAN",
#     #     "vlanPoolId": 141,
#     #     "vlanTag": 26
#     # }
#     update_network_response = requests.put(url = ip_address + create_network_url_path + "/" + network_id,
#                                             headers = headers,
#                                             json = param__updatenetwork
#                                           ).json()
#     print(update_network_response)
#     code = update_network_response["status"]
#     assert code == 200
#     assert param_update_network["name"] in get_network_name_list(ip,port,headers)
#
# # # 创建子网
# # def test_create_subnet(ip,port,headers):
# #     ip_address = "http://%s:%s" % (ip,port)
# #     network_id = get_network_id(ip,port,headers,update_network_name)[0]
# #     create_subnet_response = requests.post(
# #         url = ip_address + create_subnet_url_path + str(network_id),
# #         headers = headers,
# #         json = param_subnet
# #     ).json()
# #     code = create_subnet_response["status"]
# #     assert code == 200
# #     assert param_subnet["name"] in get_subnet_name_list(ip,port,headers)
# #
# # # 编辑子网
# # def test_update_subnet(ip,port,headers):
# #     ip_address = "http://%s:%s" % (ip,port)
# #     subnet_id = get_subnet_id(ip,port,headers,param_subnet["name"])[0]
# #     param_update_subnet = {
# #             "name": update_subnet_name,
# #             "isGatewayDisabled": "false",
# #             "gatewayIp": "192.168.1.1",
# #             "ipPools": "192.168.1.2,192.168.1.200",
# #             "preferredDns": "114.114.114.114",
# #             "alternateDns": "115.115.115.115"
# #         }
# #     update_subnet_response = requests.put(
# #         url = ip_address + update_subnet_url_path +str(subnet_id),
# #         headers = headers,
# #         json = param_update_subnet
# #     ).json()
# #     code = update_subnet_response["status"]
# #     sunnet_name = get_subnet_name_list(ip,port,headers)
# #     assert code == 200
# #     assert param_update_subnet["name"] in sunnet_name
# #
# # # 删除子网
# # def test_delete_subnet(ip,port,headers):
# #     ip_address = "http://%s:%s" % (ip,port)
# #     subnet_id = get_subnet_id(ip,port,headers,update_subnet_name)[0]
# #     delete_subnet_response = requests.delete(
# #         url = ip_address + delete_subnet_url_path + str(subnet_id),
# #         headers = headers
# #     ).json()
# #     code = delete_subnet_response["status"]
# #     assert code == 200
# #     assert update_subnet_name not in get_subnet_name_list(ip,port,headers)
# #
# # # 创建网络对象
# # def test_create_network_objects(ip,port,headers):
# #     ip_address = "http://%s:%s" % (ip,port)
# #     network_id = get_network_id(ip,port,headers,update_network_name)[0]
# #     network_resourcepools_response = requests.get(
# #         url = ip_address + get_network_resourcepools_url_path + str(network_id),
# #         headers = headers
# #     ).json()
# #     network_resourcepools_name = network_resourcepools_response["data"][0]["name"]
# #     network_resourcepools_id = network_resourcepools_response["data"][0]["id"]
# #     network_dvswitches_response = requests.get(
# #         url = ip_address + get_network_dvswitches_url_path + str(network_resourcepools_id),
# #         headers = headers
# #     ).json()
# #     network_dvswitches_name = network_dvswitches_response["data"][0]["name"]
# #     create_network_objects_response = requests.post(
# #         url = ip_address + create_network_objects_url_path + str(network_id),
# #         headers = headers,
# #         json = {
# #             "resourcePoolId": network_resourcepools_id,
# #             "resourcePoolType": "vmware",
# #             "dvsName": network_dvswitches_name,
# #             "name": object_name,
# #         }
# #     ).json()
# #     code = create_network_objects_response["status"]
# #     assert code == 200
# #     assert object_name in get_objects_name_list(ip,port,headers,update_network_name)
# #
# # # 删除网络对象
# # def test_delete_network_objects(ip,port,headers):
# #     ip_address = "http://%s:%s" % (ip,port)
# #     object_id = get_objects_id(ip,port,headers)[0]
# #     delete_network_objects_response = requests.delete(
# #         url = ip_address + delete_network_objects_url_path + str(object_id),
# #         headers = headers
# #     ).json()
# #     code = delete_network_objects_response["status"]
# #     assert code == 200
# #     assert object_name not in get_objects_name_list(ip,port,headers,update_network_name)
# #
# # #删除网络
# # # def test_delete_network(ip,port,headers):
# # #     ip_address = "http://%s:%s" % (ip,port)
# # #     network_id = get_network_id(ip,port,headers,update_network_name)
# # #     delete_network_response = requests.delete(url =  ip_address + create_network_url_path + "/" + str(network_id[0]),
# # #                                               headers = headers
# # #                                               ).json()
# # #     code =delete_network_response["status"]
# # #     assert code == 200
# # #     assert update_network_name not in get_network_name_list(ip,port,headers)
