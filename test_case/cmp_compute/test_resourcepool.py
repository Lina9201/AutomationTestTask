import pytest
import requests
import json
import os
from config import Conf
from common.get_excel_data import OperationExcleData
from test_case.cmp_compute.test_datacenter import get_datacenterid, get_datacenter

# 添加资源池请求url
createResourcePool_url = "/admin/v1/resourcepools"

testdata_path = Conf.get_testdata_path()
excelFile = testdata_path + os.sep + "物理资源.xlsx"
sheetName = "添加资源池"
resourcepool_data = OperationExcleData(excelFile, sheetName).getcase_tuple()


@pytest.mark.run(order=2)
@pytest.mark.parametrize("ID,testcases,regionname,name,type,descrption,rpip,rpport,proxyIp,proxyPort,username,password,datacenter,domain,projectId,protocol,region,version", resourcepool_data)
def test_createResourcePool(uri, headers,ID,testcases, regionname,name,type,descrption,rpip,rpport,proxyIp,proxyPort,username,password,datacenter,domain,projectId,protocol,region,version):
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
        code = createvcResourcePool_response['status']
        assert code == 200
    elif type == "openstack":
        createvcResourcePool_response = requests.post(url=uri + createResourcePool_url,
                                                      data=json.dumps(create_opresourcepool_data),
                                                      headers=headers).json()
        code = createvcResourcePool_response['status']
        assert code == 200
    elif type == "baremetal":
        createbmsResourcePool_response = requests.post(url=uri + createResourcePool_url,
                                                       data=json.dumps(create_bmsresourcepool_data),
                                                       headers=headers).json()
        code = createbmsResourcePool_response['status']
        assert code == 200


@pytest.mark.parametrize("ID,testcases,regionname,name,type,description,rpip,rpport,proxyIp,proxyPort,username,password,datacenter,domain,projectId,protocol,region,version", resourcepool_data)
def test_update_resourcePool(uri, headers,ID,testcases, regionname,name,type,description,rpip,rpport,proxyIp,proxyPort,username,password,datacenter,domain,projectId,protocol,region,version):
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
        code = updatevcResourcePool_response['status']
        assert code == 200
    elif type == "openstack":
        resourcepoolId = str(get_resourcepoolid(uri, headers, name))
        updatevcResourcePool_response = requests.put(url=uri + createResourcePool_url + '/' + resourcepoolId,
                                                      data=json.dumps(update_opresourcepool_data),
                                                      headers=headers).json()
        code = updatevcResourcePool_response['status']
        assert code == 200
    elif type == "baremetal":
        resourcepoolId = str(get_resourcepoolid(uri, headers, name))
        updatebmsResourcePool_response = requests.put(url=uri + createResourcePool_url + '/' + resourcepoolId,
                                                       data=json.dumps(update_bmsresourcepool_data),
                                                       headers=headers).json()
        code = updatebmsResourcePool_response['status']
        assert code == 200


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





