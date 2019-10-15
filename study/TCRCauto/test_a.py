import pytest
# import requests
# from TCRCauto.conftest import readexcel
#
# # 定义VLAN池路径
# ## 创建VLAN池
#
# create_vlanpool_url_path = "/admin/v1/vlan_pools"
# ## 获取VLAN池
# get_vlanpool_url_path = "/admin/v1/vlan_pools/page?tag=TRADITIONAL_VLAN"
#
# #
# def param_excel(rows,cols):
#     sheetname = readexcel('D:\测试数据.xlsx', '创建VLAN池')
#     A2 = sheetname.cell(rows,cols).value
#     return A2
# print(param_excel(1,0))
#
# # 构造测试数据
# param_vlanpool = {
#     "name": "自动创建VLAN池",    #VLAN池名称
#     "tag": "TRADITIONAL_VLAN",
#     "vlanPoolResourcePoolList": [{"resourcePoolId": 114}],      #作用域调用资源池ID
#     "vlanTagEnd": 100,      #结束VLAN ID
#     "vlanTagStart": 100     #起始VLAN ID
# }
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
#
# # ## 获取VLAN池ID
# # def get_vlanpool_id (ip,port,headers,name):
# #     vlanpool_id = []
# #     for i in get_vlanpool_list(ip,port,headers):
# #         if name == i["name"]:
# #             vlanpool_id.append(i["id"])
# #     return vlanpool_id
# #
# #
# # 测试用例
# ## 创建VLAN池
# # # @pytest.mark.parametrize(param_vlanpool)
# # def test_create_vlanpool(ip,port,headers):
# #     ip_address = "http://%s:%s" % (ip,port)
# #     createvlanpool_response = requests.post(url = ip_address + create_vlanpool_url_path,
# #                                             headers = headers,
# #                                             json = param_vlanpool
# #                                             ).json()
# #     code = createvlanpool_response["status"]
# #     assert code == 200
# #     assert param_vlanpool["name"] in get_vlanpool_name_list(ip,port,headers)
# #
# # # 编辑VLAN池
# # def test_update_vlanpool(ip,port,headers):
# #     ip_address = "http://%s:%s" % (ip,port)
# #     vlanpool_id = get_vlanpool_id(ip,port,headers,param_vlanpool["name"])[0]
# #     param_updatevlanpool = {
# #         "id": vlanpool_id,
# #         "name": updatename,
# #         "tag": "TRADITIONAL_VLAN",
# #         "vlanPoolResourcePoolList": [{"resourcePoolId": 114, "vlanPoolId":vlanpool_id}],
# #         "vlanTagEnd": 101,
# #         "vlanTagStart": 101
# #     }
# #     update_vlanpool_response = requests.put(url=ip_address + create_vlanpool_url_path + "/" + str(vlanpool_id),
# #                                             headers=headers,
# #                                             json=param_updatevlanpool
# #                                           ).json()
# #     code = update_vlanpool_response["status"]
# #     assert code == 200
# #     assert param_updatevlanpool["name"] in get_vlanpool_name_list(ip,port,headers)
# #
# #
# # # 删除VLAN池
# # def test_deletevlanpool(ip,port,headers):
# #     ip_address = "http://%s:%s" % (ip,port)
# #     vlanpool_id = get_vlanpool_id(ip,port,headers,updatename)
# #     deletevlanpool_response = requests.delete(url=ip_address + create_vlanpool_url_path + "/" + str(vlanpool_id[0]),
# #                                      headers=headers).json()
# #     code =deletevlanpool_response["status"]
# #     assert code == 200
# #     assert updatename not in get_vlanpool_name_list(ip,port,headers)
# #

a = [1,2,3]
b = [4,5,6]

@pytest.mark.parametrize("x,y",[(b,a)])
def test_add(x,y):
    c = y - x
    assert c == 3