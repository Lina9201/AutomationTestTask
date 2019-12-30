# -*- encoding: utf-8 -*-
#@Time    :2019/12/25 17:13
#@Author  :shenfeifei

from config import Conf
import os
import pytest
import json
import requests
import time
from common.get_excel_data import OperationExcleData
from test_case.cmp_compute.test_vm import get_instance_id

#从Excel获取虚拟机信息
testdata_path = Conf.get_testdata_path()
excelFile =testdata_path + os.sep + "物理资源.xlsx"
sheetName = "操作虚拟机"
instance_data = OperationExcleData(excelFile, sheetName).getcase_tuple()

# 创建虚拟机请求url
create_instance_url = "/admin/v1/instances"


#虚拟机关机
@pytest.mark.parametrize("vmname,resourcepool", instance_data)
def test_instance_powerOff(uri, headers, vmname, resourcepool):
    instance_id = get_instance_id(uri, headers, vmname, resourcepool)
    instance_powerOff_url = create_instance_url + "/" + str(instance_id) + "/powerOff"

    instance_powerOff_data = {
        "instanceId": instance_id
    }

    instance_powerOff_response = requests.post(url=uri + instance_powerOff_url,
                                               headers=headers,
                                               data=json.dumps(instance_powerOff_data)).json()
    assert instance_powerOff_response["status"] == 200

    # 虚拟机关机后等待60s再开机
    time.sleep(60)



#虚拟机开机
@pytest.mark.parametrize("vmname,resourcepool", instance_data)
def test_instance_powerOn(uri, headers, vmname, resourcepool):
    instance_id = get_instance_id(uri, headers, vmname, resourcepool)
    instance_powerOn_url = create_instance_url + "/" + str(instance_id) + "/powerOn"

    instance_powerOn_data = {
        "instanceId": instance_id
    }

    instance_powerOn_response = requests.post(url = uri + instance_powerOn_url,
                                              headers = headers,
                                              data = json.dumps(instance_powerOn_data)).json()
    print(instance_powerOn_response)
    assert  instance_powerOn_response["status"] == 200

    # 虚拟机开机后等待60s再硬重启
    time.sleep(60)

#虚拟机硬重启
@pytest.mark.parametrize("vmname, resourcepool", instance_data)
def test_instance_restart(uri, headers, vmname, resourcepool):
    instance_id = get_instance_id(uri, headers, vmname, resourcepool)
    instance_restart_url = create_instance_url +"/" + str(instance_id) + "/restart"
    instance_restart_data = {
        "instanceId": instance_id
    }
    instance_restart_response = requests.post(url = uri + instance_restart_url,
                                              headers = headers,
                                              data = json.dumps(instance_restart_data)).json()
    assert instance_restart_response["status"] == 200

    #虚拟机硬重启后等待30s
    time.sleep(30)

#虚拟机软重启

@pytest.mark.parametrize("vmname, resourcepool")
def test_instance_rebootOS(uri, headers, vmname, resourcepool):
    instance_id = get_instance_id(uri, headers, vmname, resourcepool)
    instance_rebootOS_url = create_instance_url +"/" + str(instance_id) + "/rebootOS"
    instance_rebootOS_data = {
        "instanceId": instance_id
    }
    instance_restart_response = requests.post(url = uri + instance_rebootOS_url,
                                              headers = headers,
                                              data = json.dumps(instance_rebootOS_data)).json()
    assert instance_restart_response["status"] == 200
