# -*- coding: utf-8 -*-
# @Time    : 2019/10/8 14:49
# @Author  : zhuxuefei

import pytest
import requests
import json
from common.get_excel_data import OperationExcleData

# 创建数据中心请求url
createDataCenter_url = "/admin/v1/regions"

# 获取创建数据中心请求参数数据
excelFile = "../../data/cmp/资源池.xlsx"
sheetName = "添加数据中心"
datacenter_data = OperationExcleData(excelFile, sheetName).getCaseList(excelFile, sheetName)

@pytest.mark.parametrize("datacenter_data", datacenter_data)
def test_create_datacenter(ip, port, headers, datacenter_data):
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


def test_get_datacenterid(ip, port, headers, name):
    """
    根据创建数据中心名称获取所属ID
    :param ip:
    :param port:
    :param headers:
    :return:
    """
    ip_address = "http://%s:%s" % (ip, port)
    getDataCenter_response = requests.get(url=ip_address + createDataCenter_url,
                                   headers=headers).json()
    for dc in getDataCenter_response["data"]:
        if dc["name"] == name:
            return dc["id"]


if __name__ == '__main__':
    pytest.main()




