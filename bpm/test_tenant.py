import pytest
import requests

vdc_url = "/admin/v1/vdcs"

createTenant_param = [{
  "description": "vdc1test-朱雪飞自动化创建租户测试",
  "name": "vdc1test",
  "enableQuotas": "true"
},
{
  "description": "vdc2test-朱雪飞自动化创建租户测试",
  "name": "vdc2test",
  "enableQuotas": "true"
}
]

updateTenant_param = [{
  "description": "vdc1test-update-朱雪飞自动化修改租户测试",
  "name": "vdc1test-update"
}
]

#定义vdc_id列表存创建的租户ID
vdc_id = []
updateElementIndex = 0

# 创建租户
@pytest.mark.parametrize("createTenant_param", createTenant_param)
def test_createTenant(ip, port, headers, createTenant_param):
    ip_address = "http://%s:%s" % (ip, port)
    createTenant_response = requests.post(url=ip_address + vdc_url,
                              json=createTenant_param,
                              headers=headers)

    code = createTenant_response.status_code
    assert code == 200
    # 断言创建的租户名称能在查询到的租户响应结果中存在
    assert createTenant_param["name"] in getTenant(ip, port, headers)


#  查询租户，返回所有租户名称，用于断言校验
def getTenant(ip, port, headers):
    vdc_all = []
    ip_address = "http://%s:%s" % (ip, port)
    getVdc_response = requests.get(url=ip_address + vdc_url,
                                   headers=headers).json()
    for vdcs in getVdc_response["data"]:
        vdc_all.append(vdcs["name"])
    return vdc_all


#  返回创建的租户ID
def test_getTenantId(ip, port, headers):
    ip_address = "http://%s:%s" % (ip, port)
    getVdcId_response = requests.get(url=ip_address + vdc_url,
                                   headers=headers).json()
    for vdc_created in createTenant_param:
        for vdc in getVdcId_response["data"]:
            if vdc_created["name"] == vdc["name"]:
                vdc_id.append(vdc["id"])


#  修改租户
@pytest.mark.parametrize("updateTenant_param", updateTenant_param)
def test_updateTenant(ip, port, headers, updateTenant_param):
    updateElementIndex = 0
    ip_address = "http://%s:%s" % (ip, port)
    # 获取要修改的租户id

    updateTenant_url = "/admin/v1/vdcs/%i"%vdc_id[updateElementIndex]
    update_response = requests.post(url= ip_address + updateTenant_url,
                             json=updateTenant_param,
                             headers=headers)
    code = update_response.status_code
    assert code == 200
    print(updateElementIndex)
    updateElementIndex += 1
    # 断言修改后的租户名称能在查询到的租户响应结果中存在
    assert updateTenant_param["name"] in getTenant(ip, port, headers)


# 删除租户
def test_deleteTenant(ip, port, headers):
    ip_address = "http://%s:%s" % (ip, port)
    # 获取要删除的租户id
    for currentId in vdc_id:
        deleteTenant_url = "/admin/v1/vdcs/%i" % currentId
        delete_response = requests.delete(url=ip_address + deleteTenant_url,
                                          headers=headers)
        code = delete_response.status_code
        assert code == 200
        for vdc_name in updateTenant_param:
            assert vdc_name["name"] not in getTenant(ip, port, headers)














