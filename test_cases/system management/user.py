import pytest
import requests

user_url = "/admin/v1/users"
role_url = "/admin/v1/roles"
org_url = "/admin/v1/organizations"

# 创建的测试数据
def test_org(ip, port, headers):
# 获取第一个组织id
    ip_address = "http://%s:%s" % (ip, port)
    org_response = requests.get(url=ip_address + org_url,
                                   headers=headers)
    res_org = org_response.json()
    org_id = res_org["data"][0]["id"]
    return org_id

# 获取第一个角色id
def test_role(ip, port, headers):
    ip_address = "http://%s:%s" % (ip, port)
    role_response = requests.get(url=ip_address + role_url,
                                headers=headers)
    res_role = role_response.json()
    role_id = res_role["data"][0]["id"]
    return role_id

# 构造添加数据
def create_param(ip, port, headers):
    org_id = test_org(ip, port, headers)
    role_id = test_role(ip, port, headers)
    param = {"account": "test", "password": "123456", "name": "test1", "description": "", "type": "", "source": "",
     "status": "active", "mobilePhone": "13222222222", "email": "", "rank": "",
     "extra": {"birstday": None, "sex": "male", "code": "", "isManager": "staff"},
        "organization": [org_id], "roles": [role_id]}
    return param

# 构造编辑数据
def update_param(ip, port, headers):
    org_id = test_org(ip, port, headers)
    role_id = test_role(ip, port, headers)
    param = {"account": "test1", "password": "123456", "name": "test1", "description": "", "type": "", "source": "",
     "status": "active", "mobilePhone": "13222222222", "email": "", "rank": "",
     "extra": {"birstday": None, "sex": "male", "code": "", "isManager": "staff"},
    "organization": [org_id], "roles": [role_id]}
    return param

# 修改密码
passwd = {"password": "123456"}

def test_create_user(ip, port, headers):
    ip_address = "http://%s:%s" % (ip, port)
    param = create_param(ip, port, headers)
    create_response = requests.post(url=ip_address + user_url,
                                    json = param,
                                    headers=headers)
    create_response_2 = create_response.json()
    # print(param)
    code = create_response_2["status"]
    assert code == 200# 创建用户时，未将用户放到组织下

# 查询用户列表，获得组织的第一条数据的姓名和id
def test_check_user(ip, port, headers):
    ip_address = "http://%s:%s" % (ip, port)
    org_id = test_org(ip, port, headers)
    check_url = "/admin/v1/organizations/%s/users" % org_id
    # print(check_url)
    check_response = requests.get(url=ip_address + check_url,
                                headers=headers)
    res_check = check_response.json()
    print(res_check)
# 获取名称、code
    user =  res_check["data"][0]
    user_name = user["name"]
    user_id = user["id"]
    code = res_check["status"]
    # print(user_account)
    assert code == 200
    # 返回名称,id
    return user_name, user_id

# 编辑
def test_update_user(ip, port, headers):
    ip_address = "http://%s:%s" % (ip, port)
# 构造url
    id = test_check_user(ip, port, headers)[1]
    update_url = "/admin/v1/users/%s" % id
# 构造参数，编辑名称
    param = update_param(ip, port, headers)
    update_response = requests.post(url=ip_address + update_url,
                                    json=param,
                                    headers=headers)
    update_response_2 = update_response.json()
    # print(update_response_2)
    code = update_response_2["status"]
    assert code == 200
# 获取编辑输入的名称
    update_name = param["name"]
    #print(update_name)
# 获取编辑后列表中展示的名称
    after_name = test_check_user(ip, port, headers)[0]
# 判断名称是否一致
    assert update_name == after_name

# 修改密码
def test_update_password_user(ip, port, headers):
    ip_address = "http://%s:%s" % (ip, port)
# 构造url
    id = test_check_user(ip, port, headers)[1]
    # print(id)
    password_url = "/admin/v1/users/%s/password" % id
    # print(password_url)
    password_response = requests.post(url=ip_address + password_url,
                                      json=passwd,
                                     headers=headers)
    password_response_2 = password_response.json()
    print(password_response_2)
    code = password_response_2["status"]
    assert code == 200

#查看用户详情
def test_detail_user(ip, port, headers):
    ip_address = "http://%s:%s" % (ip, port)
#构造url
    user_id = test_check_user(ip, port, headers)[1]
    # print(user_id)
    move_url = "/admin/v1/users/%s" % user_id
    # print(move_url)
    move_response = requests.get(url=ip_address + move_url,
                                     headers=headers)
    move_response_2 = move_response.json()
    print(move_response_2)
    code = move_response_2["status"]
    assert code == 200
    # 查看详情
    id_2 = test_check_user(ip, port, headers)[1]
    # print(id_2)
    assert id_2 == user_id

#移除用户
def test_move_user(ip, port, headers):
    ip_address = "http://%s:%s" % (ip, port)
#构造url
    user_id = test_check_user(ip, port, headers)[1]
    # print(user_id)
    org_id = test_org(ip, port, headers)
    move_url = "/admin/v1/organizations/%s/users/%s" % (org_id,user_id)
    # print(move_url)
    move_response = requests.delete(url=ip_address + move_url,
                                     headers=headers)
    move_response_2 = move_response.json()
    # print(move_response_2)
    code = move_response_2["status"]
    assert code == 200
    # 查看列表中是否还有删除的用户
    id_2 = test_check_user(ip, port, headers)[1]
    # print(id_2)
    assert id_2 != user_id

# 删除用户
def test_delete_user(ip, port, headers):
    ip_address = "http://%s:%s" % (ip, port)
# 构造url
    id = test_check_user(ip, port, headers)[1]
    # print(id)
    delete_url = "/admin/v1/users/%s" % id
    delete_response = requests.delete(url=ip_address + delete_url,
                                      headers=headers)
    delete_response_2 = delete_response.json()
    print(delete_response_2)
    code = delete_response_2["status"]
    assert code == 200
    # 查看列表中是否还有删除的用户
    id_2 = test_check_user(ip, port, headers)[1]
    assert id_2 != id


if __name__ == '__main__':
    pytest.main(['-q', 'user.py'])
