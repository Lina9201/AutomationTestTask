import requests
import pytest
import json
from config import Conf
import os
from common.get_excel_data import OperationExcleData

# 创建组织url
create_orgnization_url = "/admin/v1/organizations"
# 编辑组织/删除组织url
update_orgnization_url = "/admin/v1/organizations/"
# 创建用户url
create_user_url = "/admin/v1/users"
# 编辑/删除用户url
update_user_url = "/admin/v1/users/"

# 创建组织
testdata_path = Conf.get_testdata_path()
excelFile = testdata_path + os.sep + "组织用户.xlsx"
create_orgnization_param = OperationExcleData(excelFile, "创建组织").getcase_tuple()
# 编辑组织
update_orgnization_param = OperationExcleData(excelFile, '编辑组织').getcase_tuple()
# 删除组织
delete_orgnization_param = OperationExcleData(excelFile, '删除组织').getcase_tuple()
# 创建用户
create_user_param = OperationExcleData(excelFile, "创建用户").getcase_tuple()
# 编辑用户
update_user_param = OperationExcleData(excelFile, "编辑用户").getcase_tuple()
# 添加已有用户
create_exsiting_user_param = OperationExcleData(excelFile, "添加已有用户").getcase_tuple()
# 移除用户
remove_exsiting_user_param = OperationExcleData(excelFile, "移除用户").getcase_tuple()
# 修改密码
update_user_password_param = OperationExcleData(excelFile, "修改密码").getcase_tuple()
# 删除用户
delete_user_param = OperationExcleData(excelFile, "删除用户").getcase_tuple()


# 获取组织列表
def get_orgnization_list(uri, headers):
    orgnization_list_response = requests.get(
        url=uri + create_orgnization_url,
        headers=headers
    ).json()
    orgnization_list = orgnization_list_response['data']
    return orgnization_list


# 获取组织名称列表
def get_orgnization_name_list(uri, headers):
    orgnization_name_list = []
    for i in get_orgnization_list(uri, headers):
        orgnization_name_list.append(i['alias'])
    return orgnization_name_list


# 获取组织id
def get_orgnization_id(uri, headers, init_name):
    for orgnization in get_orgnization_list(uri, headers):
        if orgnization['alias'] == init_name:
            return orgnization['id']


# 根据组织名称获取用户列表
def get_fixed_user_list(uri, headers, init_name):
    user_url = "/users"
    orgnization_Id = str(get_orgnization_id(uri, headers, init_name))
    fixed_orgnization_list_response = requests.get(
        url=uri + update_orgnization_url + orgnization_Id + user_url,
        headers=headers
    ).json()
    assert fixed_orgnization_list_response["status"] == 200
    fixed_orgnization_list = fixed_orgnization_list_response['data']
    return fixed_orgnization_list


# 获取用户姓名列表
def get_user_name_list(uri, headers, init_name):
    user_name_list = []
    for i in get_fixed_user_list(uri, headers, init_name):
        user_name_list.append(i['name'])
    return user_name_list


# 获取用户名列表
def get_user_account_list(uri, headers, init_name):
    user_account_list = []
    for i in get_fixed_user_list(uri, headers, init_name):
        user_account_list.append(i['account'])
    return user_account_list


# 根据用户名称获取用户id
def get_user_account_id(uri, headers, account, init_name):
    for i in get_fixed_user_list(uri, headers, init_name):
        if i['account'] == account:
            return i['id']


# 创建组织
@pytest.mark.smoke
@pytest.mark.run(order=30)
@pytest.mark.parametrize('ID,alias,parentId,name', create_orgnization_param)
def test_create_orgnization(uri, headers, ID, alias, parentId, name):
    create_orgnization_param = {
        "alias": alias,
        "name": name,
    }
    create_orgnization_response = requests.post(
        url=uri + create_orgnization_url,
        headers=headers,
        json=create_orgnization_param
    ).json()
    assert create_orgnization_response['status'] == 200
    # 断言名称在组织列表
    assert name in get_orgnization_name_list(uri, headers)


# 在组织下创建用户
@pytest.mark.smoke
@pytest.mark.run(order=31)
@pytest.mark.parametrize('ID,org_name,account,password,name,status,mobilePhone,birstday,sex,isManager,roles',
                         create_user_param)
def test_create_user(uri, headers, ID, org_name, account, password, name, status, mobilePhone, birstday, sex, isManager,
                     roles):
    orgnization_id = get_orgnization_id(uri, headers, org_name)
    roled = json.loads(roles)
    create_param = {
        "account": account,
        "password": password,
        "name": name,
        "mobilePhone": mobilePhone,
        "extra": {
            "birstday": birstday,
            "sex": sex,
            "isManager": isManager
        },
        "organizations": [orgnization_id],
        "roles": roled,
        "status": status,
    }
    create_user_response = requests.post(
        url=uri + create_user_url,
        headers=headers,
        json=create_param
    ).json()
    assert create_user_response['status'] == 200
    # 断言用户名在列表里
    assert account in get_user_account_list(uri, headers, org_name)
    # 断言姓名在列表里
    assert name in get_user_name_list(uri, headers, org_name)


# 修改密码
@pytest.mark.smoke
@pytest.mark.run(order=32)
@pytest.mark.parametrize('ID,password,org_name,account', update_user_password_param)
def test_update_password(uri, headers, ID, password, org_name, account):
    user_id = str(get_user_account_id(uri, headers, account, org_name))
    password_url = "/password"
    update_password_param = {"password": password
                             }
    update_user_password_response = requests.post(
        url=uri + update_user_url + user_id + password_url,
        headers=headers,
        json=update_password_param
    ).json()
    assert update_user_password_response['status'] == 200


# 编辑组织下的用户
@pytest.mark.smoke
@pytest.mark.run(order=33)
@pytest.mark.parametrize('ID,org_name,account,name,status,mobilePhone,birstday,sex,isManager,roles', update_user_param)
def test_udpate_user(uri, headers, ID, org_name, account, name, status, mobilePhone, birstday, sex, isManager, roles):
    user_id = str(get_user_account_id(uri, headers, account, org_name))
    roled = json.loads(roles)
    update_user_param = {
        "account": account,
        "name": name,
        "mobilePhone": mobilePhone,
        "extra": {
            "birstday": birstday,
            "sex": sex,
            "isManager": isManager
        },
        "roles": roled,
        "status": status,
    }
    udpate_user_response = requests.post(
        url=uri + update_user_url + user_id,
        headers=headers,
        json=update_user_param
    ).json()
    assert udpate_user_response['status'] == 200
    # 断言用户名在列表里
    assert account in get_user_account_list(uri, headers, org_name)
    # 断言姓名在列表里
    assert name in get_user_name_list(uri, headers, org_name)


# 在组织下添加已有用户
@pytest.mark.smoke
@pytest.mark.run(order=34)
@pytest.mark.smoke
@pytest.mark.parametrize('ID,org_name,exsiting_org_name,exsiting_account', create_exsiting_user_param)
def test_create_existing_user(uri, headers, ID, org_name, exsiting_org_name, exsiting_account):
    user_id = str(get_user_account_id(uri, headers, exsiting_account, exsiting_org_name))
    exsiting_orgnization_id = str(get_orgnization_id(uri, headers, exsiting_org_name))
    orgnization_id = str(get_orgnization_id(uri, headers, org_name))
    org_url = "/organizations"
    # 参数为组织的id第一个id为添加已有用户的所属组织id
    create_existing_user_param = [
        exsiting_orgnization_id,
        orgnization_id
    ]
    create_existing_response = requests.post(
        url=uri + update_user_url + user_id + org_url,
        headers=headers,
        json=create_existing_user_param
    ).json()
    assert create_existing_response['status'] == 200
    # 断言用户名在列表里
    assert exsiting_account in get_user_account_list(uri, headers, org_name)


# 在组织下移除用户
@pytest.mark.smoke
@pytest.mark.run(order=35)
@pytest.mark.smoke
@pytest.mark.parametrize('ID,org_name,exsiting_org_name,exsiting_account', remove_exsiting_user_param)
def test_remove_existing_user(uri, headers, ID, org_name, exsiting_org_name, exsiting_account):
    orgnization_id = str(get_orgnization_id(uri, headers, org_name))
    user_id = str(get_user_account_id(uri, headers, exsiting_account, exsiting_org_name))
    users_url = "/users/"
    remove_existing_user_response = requests.delete(
        url=uri + update_orgnization_url + orgnization_id + users_url + user_id,
        headers=headers
    ).json()
    assert remove_existing_user_response['status'] == 200
    # 断言用户名不在列表里
    assert exsiting_account not in get_user_account_list(uri, headers, org_name)


# 删除用户
@pytest.mark.smoke_delete
@pytest.mark.run(order=9)
@pytest.mark.parametrize('ID,org_name,account', delete_user_param)
def test_delete_user(uri, headers, ID, org_name, account):
    # 删除编辑后的用户胡
    user_id = str(get_user_account_id(uri, headers, account, org_name))
    delete_user_response = requests.delete(
        url=uri + update_user_url + user_id,
        headers=headers
    ).json()
    assert delete_user_response["status"] == 200
    # 断言用户名不在列表里
    assert account not in get_user_account_list(uri, headers, org_name)


# 编辑组织
@pytest.mark.smoke_update
@pytest.mark.run(order=10)
@pytest.mark.parametrize('ID,init_name,alias,name,parentId', update_orgnization_param)
def test_update_orgnization(uri, headers, ID, init_name, alias, name, parentId):
    orgnization_Id = str(get_orgnization_id(uri, headers, init_name))
    update_orgnization_param = {
        "alias": alias,
        "name": name,
        "parentId": parentId
    }
    update_orgnization_response = requests.post(
        url=uri + update_orgnization_url + orgnization_Id,
        headers=headers,
        json=update_orgnization_param
    ).json()
    assert update_orgnization_response['status'] == 200
    # 断言组织在列表里
    assert name in get_orgnization_name_list(uri, headers)


# 删除组织
@pytest.mark.smoke_delete
@pytest.mark.run(order=10)
@pytest.mark.parametrize('ID,name', delete_orgnization_param)
def test_delete_orgnization(uri, headers, ID, name):
    orgnization_Id = str(get_orgnization_id(uri, headers, name))
    delete_orgnization_response = requests.delete(
        url=uri + update_orgnization_url + orgnization_Id,
        headers=headers).json()
    assert delete_orgnization_response["status"] == 200
    # 断言组织已删除
    assert name not in get_orgnization_name_list(uri, headers)
