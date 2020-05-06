
import requests
import pytest
from config import Conf
import os
from common.get_excel import read_excel, read_excel_tuple
from common.get_excel_data import OperationExcleData
from test_case.cmp_compute.test_resourcepool import get_resourcepoolid
import allure
from utils.LogUtil import my_log

# 创建镜像
create_images_url = "/admin/v1/images?osType="
# 获取vmware模板
get_vmware_templates_url = "/admin/v1/hypersivor/vmware/templates?resourcePoolId="
# 获取openstack模板
get_openstack_templates_url = "/admin/v1/hypersivor/openstack/images?resourcePoolId="
# 获取镜像
get_images_url = "/admin/v1/images/"

# 构造测试数据
testdata_path = Conf.get_testdata_path()
excelFile = testdata_path + os.sep + "镜像管理.xlsx"
# 创建镜像
param_create_images = read_excel_tuple(excelFile, '创建镜像')
# 编辑镜像
param_update_images = read_excel_tuple(excelFile, '编辑镜像')
# 删除镜像
param_delete_images = OperationExcleData(excelFile, "删除镜像").getcase_tuple()
# 添加资源池模板
param_create_template = read_excel_tuple(excelFile, '添加资源池模板')
# 删除资源池模板
param_delete_template = OperationExcleData(excelFile, "删除资源池模板").getcase_tuple()


# 根据传入的资源池获取镜像模板列表
def get_template_list(uri, headers, resourcepoolType, resourcepool):
    template_list = []
    resourcepool_id = get_resourcepoolid(uri, headers, resourcepool)
    if resourcepoolType == "vmware":
        get_vmware_template_response = requests.get(url=uri + get_vmware_templates_url + str(resourcepool_id),
                                                    headers=headers).json()
        template_list = get_vmware_template_response['data']
    elif resourcepoolType == "openstack":
        get_openstack_template_response = requests.get(url=uri + get_openstack_templates_url + str(resourcepool_id),
                                                       headers=headers).json()
        template_list = get_openstack_template_response['data']
    # print(template_list)
    return template_list


# 根据传入的资源池获取镜像模板列表名称
def get_template_name(uri, headers, resourcepoolType, resourcepool):
    template_name = []
    for template in get_template_list(uri, headers, resourcepoolType, resourcepool):
        template_name.append(template['name'])
    return template_name


# 根据选择的资源池名称获取资源池id
def get_template_id(uri, headers, resourcepoolType, resourcepool, template_name):
    for template in get_template_list(uri, headers, resourcepoolType, resourcepool):
        if template['name'] == template_name:
            if resourcepoolType == "vmware":
                return template['morValue']
            elif resourcepoolType == "openstack":
                return template['id']


# 获取镜像列表
def get_images_list(uri, headers):
    images_list_response = requests.get(
        url=uri + create_images_url,
        headers=headers
    ).json()
    images_list = images_list_response['data']
    return images_list


# 获取镜像名称列表
def get_images_name_list(uri, headers):
    images_name_list = []
    for i in get_images_list(uri, headers):
        images_name_list.append(i['name'])
    return images_name_list


# 根据镜像名称获取镜像id
def get_image_id(uri, headers, imagename):
    for image in get_images_list(uri, headers):
        if image['name'] == imagename:
            return image['id']


# 根据编辑后的镜像名称获取镜像id
def get_imageedited_id(uri, headers, image_name):
    for image in get_images_list(uri, headers):
        if image['name'] == image_name:
            return image['id']


# 创建镜像
@pytest.mark.smoke
@pytest.mark.run(order=3)
@allure.feature("计算资源")
@allure.story("创建镜像")
@pytest.mark.parametrize(
    "name,description,os,osType,password,username,loading,resourcepoolType,resourcepool,template_name",
    param_create_images)
def test_create_images(uri, headers, name, description, os, osType, password, username, loading,
                       resourcepool, resourcepoolType, template_name):
    templateId = get_template_id(uri, headers, resourcepoolType, resourcepool, template_name)
    resourcepoolid = get_resourcepoolid(uri, headers, resourcepool)
    create_images_param = {"description": description,
                           "name": name,
                           "os": os,
                           "osType": osType,
                           "relations": [
                               {
                                   "extra": {
                                       "password": password,
                                       "username": username
                                   },
                                   "loading": loading,
                                   "relavant": {},
                                   "relavantId": templateId,
                                   "relavantName": template_name,
                                   "resourcepoolId": resourcepoolid,
                                   "resourcepoolType": resourcepoolType
                               }
                           ]
                           }
    create_images_response = requests.post(url=uri + create_images_url,
                                           json=create_images_param,
                                           headers=headers).json()
    allure.attach("请求响应code", str(create_images_response['status']))
    allure.attach("请求响应结果", str(create_images_response))
    my_log().info(create_images_response)
    assert create_images_response['status'] == 200
    # 断言创建的镜像名称能在查询到的响应结果中存在
    assert name in get_images_name_list(uri, headers)


# 校验创建镜像的资源池
def get_resourcepool_template_list(uri, headers, imagename):
    images_Id = str(get_image_id(uri, headers, imagename))
    relation = "/relations?"
    get_images_param_response = requests.get(
        url=uri + get_images_url + images_Id + relation,
        headers=headers).json()
    assert get_images_param_response["status"] == 200
    return get_images_param_response["data"]


# 获取relavantName列表
def get_template_name_list(uri, headers, imagename):
    template_name_list = []
    for i in get_resourcepool_template_list(uri, headers, imagename):
        template_name_list.append(i['relavantName'])
    return template_name_list


# 删除关联的vmware/openstack资源池模板
@pytest.mark.parametrize("ID,init_name",
                         param_delete_template)
@allure.feature("计算资源")
@allure.story("删除镜像关联模板")
def test_delete_resourcepool_template(uri, headers, ID, init_name):
    relation_url = "/relations"
    images_Id = str(get_image_id(uri, headers, init_name))
    delete_resourcepool_template_param = []
    delete_resourcepoll_template_response = requests.post(
        url=uri + get_images_url + images_Id + relation_url,
        json=delete_resourcepool_template_param,
        headers=headers).json()
    allure.attach("请求响应code", str(delete_resourcepoll_template_response['status']))
    allure.attach("请求响应结果", str(delete_resourcepoll_template_response))
    my_log().info(delete_resourcepoll_template_response)
    assert delete_resourcepoll_template_response["status"] == 200
    # 断言镜像的资源池模板为空，即无数据
    assert "data" not in delete_resourcepoll_template_response.keys()


# 添加关联的资源池模板
@pytest.mark.smoke_update
@pytest.mark.run(order=3)
@pytest.mark.parametrize("init_name,resourcepool,loading,password,username,template_name,resourcepoolType",
                         param_create_template)
@allure.feature("计算资源")
@allure.story("镜像添加关联模板")
def test_create_resourcepool_template(uri, headers, init_name, resourcepool, loading, password, username,
                                      template_name,
                                      resourcepoolType):
    images_Id = str(get_image_id(uri, headers, init_name))
    resourcePoolId = get_resourcepoolid(uri, headers, resourcepool)
    relavant_id = str(get_template_id(uri, headers, resourcepoolType, resourcepool, template_name))
    relation_url = "/relations"
    create_resourcepool_template_param = [{
        "imageId": images_Id,
        "loading": loading,
        "extra":
            {
                "password": password,
                "username": username
            },
        "relavant": {},
        "relavantId": relavant_id,
        "relavantName": template_name,
        "resourcepoolId": resourcePoolId,
        "resourcepoolType": resourcepoolType
    }]
    create_resourcepool_template_response = requests.post(
        url=uri + get_images_url + images_Id + relation_url,
        json=create_resourcepool_template_param,
        headers=headers).json()
    allure.attach("请求响应code", str(create_resourcepool_template_response['status']))
    allure.attach("请求响应结果", str(create_resourcepool_template_response))
    my_log().info(create_resourcepool_template_response)
    assert create_resourcepool_template_response["status"] == 200
    # 断言创建的模板关联能在查询到的响应结果中存在
    assert template_name in get_template_name_list(uri, headers, init_name)


# 编辑镜像
@pytest.mark.smoke_update
@pytest.mark.run(order=4)
@pytest.mark.parametrize("init_name,name,os,osType,deleted,isPublic", param_update_images)
@allure.feature("计算资源")
@allure.story("编辑镜像")
def test_udpate_images(uri, headers, init_name, name, os,osType, deleted, isPublic):
    # 根据镜像名称获取镜像id
    images_Id = str(get_image_id(uri, headers, init_name))
    update_images_param = {"name": name,
                           "os": os,
                           "osType": osType,
                           "deleted": deleted,
                           "isPublic": isPublic
                           }
    update_images_param_response = requests.post(
        url=uri + get_images_url + images_Id,
        headers=headers,
        json=update_images_param
    ).json()
    allure.attach("请求响应code", str(update_images_param_response['status']))
    allure.attach("请求响应结果", str(update_images_param_response))
    my_log().info(update_images_param_response)
    assert update_images_param_response["status"] == 200
    # 断言镜像名称在列表里
    assert name in get_images_name_list(uri, headers)


# 删除镜像
@pytest.mark.smoke_delete
@pytest.mark.run(order=2)
@pytest.mark.parametrize('ID,image_name', param_delete_images)
@allure.feature("计算资源")
@allure.story("删除镜像")
def test_delete_image(uri, headers, ID, image_name):
    images_Id = str(get_imageedited_id(uri, headers, image_name))
    delete_images_response = requests.delete(
        url=uri + get_images_url + images_Id,
        headers=headers
    ).json()
    allure.attach("请求响应code", str(delete_images_response['status']))
    allure.attach("请求响应结果", str(delete_images_response))
    my_log().info(delete_images_response)
    assert delete_images_response['status'] == 200
    # 断言镜像名称不在列表里
    assert image_name not in get_images_name_list(uri, headers)
