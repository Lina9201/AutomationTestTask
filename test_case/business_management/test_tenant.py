import pytest
import requests
import json
import os
from config import Conf
from common.get_excel_data import OperationExcleData
from common.get_excel import read_excel_tuple

get_user_url = "/admin/v1/users"
create_tenant_url="/admin/v1/vdcs/"
update_tenant_url="/admin/v1/vdcs/"
delete_tenant_url="/admin/v1/vdcs/"
manage_tenant_url="/admin/v1/vdcs/"
create_project_url="/admin/v1/projects"
update_project_url="/admin/v1/projects/"
delete_project_url="/admin/v1/projects/"

testdata_path = Conf.get_testdata_path()
excelFile = testdata_path + os.sep + "业务管理.xlsx"

create_tenant_data=OperationExcleData(excelFile,"创建租户").getCaseList()
update_tenant_data=OperationExcleData(excelFile,"编辑租户").getcase_tuple()
manage_user_data=OperationExcleData(excelFile,"成员管理").getcase_tuple()
create_project_data = read_excel_tuple(excelFile, '创建项目')
update_project_data=OperationExcleData(excelFile, '编辑项目').getcase_tuple()
delete_project_data=OperationExcleData(excelFile, '删除项目').getcase_tuple()
delete_tenant_data=OperationExcleData(excelFile, '删除租户').getcase_tuple()

# 创建租户
@pytest.mark.smoke
@pytest.mark.run(order=9)
@pytest.mark.parametrize("create_tenant_data",create_tenant_data)
def test_create_tenant(uri, headers, create_tenant_data):
    createTenant_response = requests.post(url=uri + create_tenant_url,
                                         data=json.dumps(create_tenant_data),
                                         headers=headers)
    code = createTenant_response.status_code
    assert code == 200

#查询租户id
def get_tenant_id(uri, headers, tenantname):
    """
    根据传入的租户名称获取租户id
    :param uri:
    :param headers:
    :param tenantname:租户名称
    :return:
    """
    get_tenant_response = requests.get(url = uri + create_tenant_url,
                                       headers = headers
                                       ).json()
    for tenant in get_tenant_response ['data']:
        if tenant['name'] == tenantname:
            return tenant['id']


#编辑租户
@pytest.mark.smoke_update
@pytest.mark.run(order=9)
@pytest.mark.parametrize("ID, testcases,tenant,name,description,enableQuotas",update_tenant_data)
def test_update_tenant(uri,headers,ID,testcases,tenant,name,description,enableQuotas):
    tenant_id = get_tenant_id(uri, headers, tenant)
    update_tenant_data_param={
            "name":name,
            "description":description,
            "vdc":tenant_id
        }
    updateTenant_response=requests.post(url=uri+update_tenant_url+str(tenant_id),
                                        data=json.dumps(update_tenant_data_param),
                                        headers=headers).json()
    code = updateTenant_response['status']
    assert code == 200

#根据账号名称获取userID
def get_user_id(uri, headers, account):
    get_user_response=requests.get(url=uri + get_user_url,
                                   headers=headers
                                   ).json()
    for user in get_user_response['data']['list']:
        if user['account'] == account:
            return user['id']

#租户成员管理
@pytest.mark.smoke
@pytest.mark.run(order=10)
@pytest.mark.parametrize("ID,testcases,tenant,account,role",manage_user_data)
def test_manage_user(uri,headers,ID,testcases,tenant,account,role):
    tenant_id = get_tenant_id(uri, headers, tenant)
    user_id=get_user_id(uri, headers, account)
    # user_data=[]
    # user_data.append(manage_user_data)#列表嵌套字典
    manage__user_param=[{
            "userId": user_id,
            "role": role
        }]
    manage_user_response=requests.post(url=uri+manage_tenant_url+str(tenant_id)+"/users",
                                        data=json.dumps(manage__user_param),
                                        headers=headers).json()
    code = manage_user_response['status']
    assert code == 200

# 创建项目
@pytest.mark.smoke
@pytest.mark.run(order=11)
@pytest.mark.parametrize("tenantname, projectname, description", create_project_data)
def test_create_project(uri, headers, tenantname, projectname, description):
    tenant_id = get_tenant_id(uri, headers, tenantname)
    create_project_data_param={
            "name":projectname,
            "description":description,
            "vdc":tenant_id
        }

    createProject_response = requests.post(url=uri + create_project_url,
                                         data=json.dumps(create_project_data_param),
                                         headers=headers).json()
    code = createProject_response['status']
    assert code == 200


def get_project_id(uri, headers, projectname):
    """
    根据传入的项目名称获取项目id
    :param uri:
    :param headers:
    :param projectname:项目名称
    :return:
    """
    get_project_response = requests.get(url = uri + create_project_url,
                                        headers = headers).json()
    for project in get_project_response['data']['list']:
        if project['name'] == projectname:
            return project['id']


#编辑项目
@pytest.mark.smoke_update
@pytest.mark.run(order=10)
@pytest.mark.parametrize("ID, testcases,project,name,description",update_project_data)
def test_update_project(uri,headers,ID,testcases,project,name,description):
    project_id = get_project_id(uri,headers,project)
    update_project_data_param={
            "name":name,
            "description":description,
        }
    updateProject_response = requests.post(url=uri + update_project_url+str(project_id),
                                         data=json.dumps(update_project_data_param),
                                         headers=headers).json()
    code = updateProject_response['status']
    assert code == 200

#删除项目
@pytest.mark.smoke_delete
@pytest.mark.run(order=7)
@pytest.mark.parametrize("ID,testcases,projectname",delete_project_data)
def test_delete_project(uri, headers,ID,testcases,projectname):
    project_id = get_project_id(uri,headers,projectname)
    delete_project_response = requests.delete(
        url=uri + delete_project_url + str(project_id),
        headers=headers
    ).json()
    assert delete_project_response == 200


#删除租户
@pytest.mark.smoke_delete
@pytest.mark.run(order=11)
@pytest.mark.parametrize("ID,testcases,tenantname",delete_tenant_data)
def test_delete_tenant(uri, headers,ID,testcases,tenantname):
    tenant_id=get_tenant_id(uri,headers,tenantname)
    delete_tenant_response = requests.delete(
        url=uri + delete_tenant_url + str(tenant_id),
        headers=headers
    ).json()
    code = delete_tenant_response["status"]
    assert code == 200



