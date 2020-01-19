# -*- coding: utf-8 -*-
# @Time    : 2019/10/8 14:49
# @Author  : zhuxuefei

import pytest
import requests
import json
import allure
import os
from config import Conf
from common.get_excel_data import OperationExcleData
from utils.AssertUtil import AssertUtil

# 创建数据中心请求url
createDataCenter_url = "/admin/v1/regions"

# 获取创建数据中心请求参数数据
testdata_path = Conf.get_testdata_path()
excelFile = testdata_path + os.sep + "物理资源.xlsx"
datacenter_data = OperationExcleData(excelFile, "添加数据中心").getCaseList()
update_datacenter_data = OperationExcleData(excelFile, "编辑数据中心").getcase_tuple()
delete_datacenter_data = OperationExcleData(excelFile, "删除数据中心").getcase_tuple()

@pytest.mark.smoke
@pytest.mark.run(order=1)
@pytest.mark.parametrize("datacenter_data", datacenter_data)
def test_create_datacenter(uri, headers, datacenter_data):
    """
    创建数据中心接口
    :param ip:
    :param port:
    :param headers:
    :param datacenter_data:测试用例
    :return:
    """
    createDataCenter_response = requests.post(url=uri + createDataCenter_url,
                                         data=json.dumps(datacenter_data),
                                         headers=headers)
    code = createDataCenter_response.status_code
    AssertUtil().assert_code(code, 200)
    allure.dynamic.feature(excelFile)


@pytest.mark.parametrize("ID, testcases, regionname, upadte_region, description", update_datacenter_data)
@pytest.mark.smoke_update
@pytest.mark.run(order=1)
def test_update_datacenter(uri, headers, ID, testcases, regionname, upadte_region, description):
    """
    编辑数据中心
    :param uri:
    :param headers:
    :param ID:
    :param testcases:
    :param regionname:需要编辑的数据中心名称
    :param upadte_region: 更改的数据中心名称
    :param description: 更改后的数据中心描述
    :return:
    """
    regionId = str(get_datacenterid(uri, headers, regionname))
    update_datacenter_data = {
        "name": upadte_region,
        "description": description
    }
    update_datacenter_response = requests.post(url=uri + createDataCenter_url + "/" + regionId,
                                         data=json.dumps(update_datacenter_data),
                                         headers=headers)
    code = update_datacenter_response.status_code
    AssertUtil().assert_code(code, 200)


@pytest.mark.parametrize("ID, testcases, regionname", delete_datacenter_data)
def test_delete_datacenter(uri, headers, ID, testcases, regionname):
    regionId = str(get_datacenterid(uri, headers, regionname))
    delete_datacenter_response = requests.delete(url=uri + createDataCenter_url + "/" + regionId,
                                                 headers=headers)
    code = delete_datacenter_response.status_code
    AssertUtil().assert_code(code, 200)


def get_datacenterid(uri, headers, datacentername):
    """
    根据创建数据中心名称获取所属ID
    :param ip:
    :param port:
    :param headers:
    :return:
    """
    getDataCenterId_response = requests.get(url=uri + createDataCenter_url,
                                   headers=headers).json()
    for dc in getDataCenterId_response["data"]:
        if dc["name"] == datacentername:
            return dc["id"]


def get_datacenter(uri, headers):
    getDataCenter_response = requests.get(url=uri + createDataCenter_url,
                                            headers=headers).json()
    return getDataCenter_response["data"]





