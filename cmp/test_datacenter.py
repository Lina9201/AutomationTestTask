# -*- coding: utf-8 -*-
# @Time    : 2019/10/8 14:49
# @Author  : zhuxuefei

import pytest
import requests
import json
from Common.get_excel_data import OperationExcleData

# 创建数据中心请求urk
createDataCenter_url = "/admin/v1/regions"

# 获取创建数据中心请求参数数据
excelFile = "E:\\AutomationTestTask\\Test_data\\计算资源\\资源池.xlsx"
datacenter_data = OperationExcleData(excelFile).getCaseList(excelFile)

@pytest.mark.parametrize("datacenter_data", datacenter_data)
def test_datacenter(ip, port, headers, datacenter_data):
    ip_address = "http://%s:%s" % (ip, port)
    createDataCenter_response = requests.post(url=ip_address + createDataCenter_url,
                                         data=json.dumps(datacenter_data),
                                         headers=headers)
    code = createDataCenter_response.status_code
    assert code == 200
    print(createDataCenter_response.text)