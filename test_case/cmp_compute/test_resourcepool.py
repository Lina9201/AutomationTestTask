import pytest
import requests
import json
import os
from config import Conf
from common.get_excel_data import OperationExcleData
from common.get_db_data import assert_mysqldb
from test_case.cmp_compute.test_datacenter import get_datacenterid, get_datacenter
import allure
from utils.LogUtil import my_log
from utils.AssertUtil import AssertUtil

# 添加资源池请求url
createResourcePool_url = "/admin/v1/resourcepools"

testdata_path = Conf.get_testdata_path()
excelFile = testdata_path + os.sep + "物理资源.xlsx"
sheetName = "添加资源池"
resourcepool_data = OperationExcleData(excelFile, sheetName).getcase_tuple()

@pytest.mark.smoke
@pytest.mark.run(order=2)
@pytest.mark.parametrize("ID,testcases,regionname,name,type,descrption,rpip,rpport,proxyIp,proxyPort,username,password,datacenter,domain,projectId,protocol,region,version,status_code,expected_result,db_verify", resourcepool_data)
@allure.feature("计算资源")
@allure.story("添加资源池")
def test_createResourcePool(uri, headers,ID,testcases, regionname,name,type,descrption,rpip,rpport,proxyIp,proxyPort,username,password,datacenter,domain,projectId,protocol,region,version,status_code,expected_result,db_verify):
    """
    添加资源池接口
    :param ip:
    :param port:
    :param headers:
    :param resourcepool_data:
    :return:
    """
    create_vcresourcepool_data = {
        "region": get_datacenterid(uri, headers, regionname),
        "name": name,
        "type": type,
        "extra":{
            "datacenter": datacenter
        },
        "ip": rpip,
        "port": rpport,
        "proxyIp": proxyIp,
        "proxyPort": proxyPort,
        "username": username,
        "password": password
    }

    create_opresourcepool_data = {
         "region": get_datacenterid(uri, headers, regionname),
         "name": name,
         "type": type,
         "extra": {
             "version": version,
             "region": region,
             "domain": domain,
             "projectId": projectId,
             "protocol": protocol
         },
         "ip": rpip,
         "port": rpport,
         "proxyIp": proxyIp,
         "proxyPort": proxyPort,
         "username": username,
         "password": password
    }

    create_bmsresourcepool_data = {
        "region": get_datacenterid(uri, headers, regionname),
        "name": name,
        "type": type,
        "extra": {
            "protocol": protocol
        },
        "ip": rpip,
        "port": rpport,
        "proxyIp": proxyIp,
        "proxyPort": proxyPort,
        "username": username,
        "password": password

    }

    if type == "vmware":
        createvcResourcePool_response = requests.post(url=uri + createResourcePool_url,
                                              data=json.dumps(create_vcresourcepool_data),
                                              headers=headers).json()
        allure.attach("请求响应code", str(createvcResourcePool_response['status']))
        allure.attach("请求响应结果", str(createvcResourcePool_response))
        my_log().info(createvcResourcePool_response)
        AssertUtil().assert_code(createvcResourcePool_response['status'], status_code)
        AssertUtil().assert_in_body(createvcResourcePool_response['data'], expected_result)
        assert_mysqldb("tcrc_db", createvcResourcePool_response['data'], db_verify)
    elif type == "openstack":
        createopResourcePool_response = requests.post(url=uri + createResourcePool_url,
                                                      data=json.dumps(create_opresourcepool_data),
                                                      headers=headers).json()
        allure.attach("请求响应code", str(createopResourcePool_response['status']))
        allure.attach("请求响应结果", str(createopResourcePool_response))
        my_log().info(createopResourcePool_response)
        AssertUtil().assert_code(createopResourcePool_response['status'], status_code)
        AssertUtil().assert_in_body(createopResourcePool_response['data'], expected_result)
        assert_mysqldb("tcrc_db", createopResourcePool_response['data'], db_verify)
    elif type == "baremetal":
        createbmsResourcePool_response = requests.post(url=uri + createResourcePool_url,
                                                       data=json.dumps(create_bmsresourcepool_data),
                                                       headers=headers).json()
        allure.attach("请求响应code", str(createbmsResourcePool_response['status']))
        allure.attach("请求响应结果", str(createbmsResourcePool_response))
        my_log().info(createbmsResourcePool_response)
        AssertUtil().assert_code(createbmsResourcePool_response['status'], status_code)
        AssertUtil().assert_in_body(createbmsResourcePool_response['data'], expected_result)
        assert_mysqldb("tcrc_db", createbmsResourcePool_response['data'], db_verify)

@pytest.mark.smoke_update
@pytest.mark.run(order=2)
@pytest.mark.parametrize("ID,testcases,regionname,name,type,description,rpip,rpport,proxyIp,proxyPort,username,password,datacenter,domain,projectId,protocol,region,version,status_code,expected_result,db_verify", resourcepool_data)
@allure.feature("计算资源")
@allure.story("编辑资源池")
def test_update_resourcePool(uri, headers,ID,testcases, regionname,name,type,description,rpip,rpport,proxyIp,proxyPort,username,password,datacenter,domain,projectId,protocol,region,version,status_code,expected_result,db_verify):
    """
    编辑资源池接口
    :param uri:
    :param headers:
    :param ID:
    :param testcases:
    :param regionname:
    :param name:
    :param type:
    :param descrption:
    :param rpip:
    :param rpport:
    :param proxyIp:
    :param proxyPort:
    :param username:
    :param password:
    :param datacenter:
    :param domain:
    :param projectId:
    :param protocol:
    :param region:
    :param version:
    :return:
    """
    update_vcresourcepool_data = {
        "region": get_datacenterid(uri, headers, regionname),
        "name": name,
        "type": type,
        "description": description,
        "extra":{
            "datacenter": datacenter
        },
        "ip": rpip,
        "port": rpport,
        "proxyIp": proxyIp,
        "proxyPort": proxyPort,
        "username": username,
        "password": password
    }
    update_opresourcepool_data = {
        "region": get_datacenterid(uri, headers, regionname),
        "name": name,
        "type": type,
        "description": description,
        "extra": {
            "version": version,
            "region": region,
            "domain": domain,
            "projectId": projectId,
            "protocol": protocol
        },
        "ip": rpip,
        "port": rpport,
        "proxyIp": proxyIp,
        "proxyPort": proxyPort,
        "username": username,
        "password": password
    }
    update_bmsresourcepool_data = {
        "region": get_datacenterid(uri, headers, regionname),
        "name": name,
        "type": type,
        "description": description,
        "extra": {
            "protocol": protocol
        },
        "ip": rpip,
        "port": rpport,
        "proxyIp": proxyIp,
        "proxyPort": proxyPort,
        "username": username,
        "password": password

    }

    if type == "vmware":
        resourcepoolId = str(get_resourcepoolid(uri, headers, name))
        updatevcResourcePool_response = requests.put(url=uri + createResourcePool_url + '/' + resourcepoolId,
                                                      data=json.dumps(update_vcresourcepool_data),
                                                      headers=headers).json()
        allure.attach("请求响应code", str(updatevcResourcePool_response['status']))
        allure.attach("请求响应结果", str(updatevcResourcePool_response))
        my_log().info(updatevcResourcePool_response)
        AssertUtil().assert_code(updatevcResourcePool_response['status'], status_code)
        AssertUtil().assert_in_body(updatevcResourcePool_response['data'], expected_result)
        assert_mysqldb("tcrc_db", updatevcResourcePool_response['data'], db_verify)
    elif type == "openstack":
        resourcepoolId = str(get_resourcepoolid(uri, headers, name))
        updateopResourcePool_response = requests.put(url=uri + createResourcePool_url + '/' + resourcepoolId,
                                                      data=json.dumps(update_opresourcepool_data),
                                                      headers=headers).json()
        allure.attach("请求响应code", str(updateopResourcePool_response['status']))
        allure.attach("请求响应结果", str(updateopResourcePool_response))
        my_log().info(updateopResourcePool_response)
        AssertUtil().assert_code(updateopResourcePool_response['status'], status_code)
        AssertUtil().assert_in_body(updateopResourcePool_response['data'], expected_result)
        assert_mysqldb("tcrc_db", updateopResourcePool_response['data'], db_verify)

    elif type == "baremetal":
        resourcepoolId = str(get_resourcepoolid(uri, headers, name))
        updatebmsResourcePool_response = requests.put(url=uri + createResourcePool_url + '/' + resourcepoolId,
                                                       data=json.dumps(update_bmsresourcepool_data),
                                                       headers=headers).json()
        allure.attach("请求响应code", str(updatebmsResourcePool_response['status']))
        allure.attach("请求响应结果", str(updatebmsResourcePool_response))
        my_log().info(updatebmsResourcePool_response)
        AssertUtil().assert_code(updatebmsResourcePool_response['status'], status_code)
        AssertUtil().assert_in_body(updatebmsResourcePool_response['data'], expected_result)
        assert_mysqldb("tcrc_db", updatebmsResourcePool_response['data'], db_verify)


def get_resourcepoolid(uri, headers, resourcepoolname):
    """
    根据传入的资源池名称获取资源池id
    :param uri:
    :param headers:
    :param resourcepoolname:资源池名称
    :return:
    """
    getResourcePoolId_response = requests.get(url=uri + createResourcePool_url,
                                            headers=headers).json()
    for rp in getResourcePoolId_response["data"]:
        if rp["name"] == resourcepoolname:
            return rp["id"]





