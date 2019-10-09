# -*- coding: utf-8 -*-
# @Time    : 2019/10/8 14:49
# @Author  : zhuxuefei

import pytest
import requests
import json
from Common.get_excel_data import OperationExcleData

# 创建数据中心请求url
createDataCenter_url = "/admin/v1/regions"

# 获取创建数据中心请求参数数据
excelFile = "E:\\AutomationTestTask\\Test_data\\计算资源\\资源池.xlsx"
sheetName = "添加数据中心"
datacenter_data = OperationExcleData(excelFile, sheetName).getCaseList(excelFile, sheetName)

@pytest.mark.parametrize("datacenter_data", datacenter_data)
def test_datacenter(ip, port, headers, datacenter_data):
    """
    创建数据中心接口
    :param ip:
    :param port:
    :param headers:
    :param datacenter_data:测试用例
    :return:
    """
    ip_address = "http://%s:%s" % (ip, port)
    createDataCenter_response = requests.post(url=ip_address + createDataCenter_url,
                                         data=json.dumps(datacenter_data),
                                         headers=headers)
    code = createDataCenter_response.status_code
    assert code == 200
    print(createDataCenter_response.text)


def test_getDataCenterId(ip, port, headers):
    """
    获取创建的数据中心所属ID
    :param ip:
    :param port:
    :param headers:
    :return:
    """
    ip_address = "http://%s:%s" % (ip, port)
    getDataCenter_response = requests.get(url=ip_address + createDataCenter_url,
                                   headers=headers).json()
    for dc in getDataCenter_response["data"]:
        if dc["name"] == datacenter_data[0]["name"]:
            return dc["id"]




