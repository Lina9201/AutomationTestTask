import pytest
import requests
import tcrc.function.user

url = "/admin/v1/vdcs"
create_param = [{
  "description": "n",
  "name": "wmc",
  "enableQuotas": "true"
}]

update_param = [{
  "description": "tempor",
  "name": "wmc1"
}]



# 创建
@pytest.mark.parametrize("createparam", create_param)
def test_create(ip, port, createparam, headers):
    ip_address = "http://%s:%s" % (ip, port)
    response = requests.post(url=ip_address + url,
                              json=createparam,
                              headers=headers)
    # print(type(response))
    code = response.status_code
    # print(code)
    assert code == 200
    # 获取创建后的第一个租户名称
    name = test_check(ip, port, headers)[1]
    # print(name)
    # 判断获取的名称是否与创建时传入的一致
    assert name == createparam["name"]

# 获取列表，获得第一个租户的id、名称
def test_check(ip, port, headers):
    ip_address = "http://%s:%s" % (ip, port)
    check_response = requests.get(url=ip_address + url,
                                   headers=headers)
    code = check_response.status_code
    assert code == 200
    check_response_2 = check_response.json()
    # print(check_response_2)
    data = check_response_2["data"][0]
    name = data["name"]
    # print(name)
    # 获取id
    id = data["id"]
    # print(id)
    return id, name

# 编辑名称
@pytest.mark.parametrize("updateparam", update_param)
def test_update(ip, port, updateparam, headers):
    ip_address = "http://%s:%s" % (ip, port)
    id = test_check(ip, port, headers)[0]
    # 获取创建的租户id
    update_url = "/admin/v1/vdcs/%i"%id
    # print(update_url)
    update_response = requests.post(url= ip_address + update_url,
                             json=updateparam,
                             headers=headers)
    code = update_response.status_code
    assert code == 200
    # print(code)
    # 获取编辑后的名称
    name = test_check(ip, port, headers)[1]
    # print(name)
    # 判断名称是否与编辑时输入的一致
    assert name == updateparam["name"]

# 查看租户详情
def test_detail(ip, port, headers):
    ip_address = "http://%s:%s" % (ip, port)
    # 获取要查询的租户的id
    id_1 = test_check(ip, port, headers)[0]
    # 组成查看详情url
    detail_url = "/admin/v1/vdcs/%i" % id_1
    detail_response = requests.get(url=ip_address+detail_url, headers=headers)
    code = detail_response.status_code
    assert code == 200
    # 获取详情中的id
    detail_response_2 = detail_response.json()
    # print(detail_response_2)
    id_2 = detail_response_2["data"]["id"]
    # print(id_2)
    # 判断id不致
    assert id_1 == id_2


# 删除
def test_delete(ip, port, headers):
    ip_address = "http://%s:%s" % (ip, port)
    # 获取要删除的租户的id
    id_1 = test_check(ip, port, headers)[0]
    # 组成删除url
    delete_url = "/admin/v1/vdcs/%i" % id_1
    delete_response = requests.delete(url=ip_address+delete_url,
                                      headers=headers)
    code = delete_response.status_code
    assert code == 200
    # 获取删除之后的第一个id
    id_2 = test_check(ip, port, headers)[0]
    # 判断第一个租户被删除，id不一致
    assert id_1 != id_2


if __name__ == '__main__':
    pytest.main(['-q', 'tenant.py'])
