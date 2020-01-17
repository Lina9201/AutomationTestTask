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
from test_case.cmp_compute.test_vm import get_instance_id, get_instance_vmName, get_intance_nics, get_instance_disks
from test_case.network_resource.test_network import get_network_id, get_object_id, get_subnet_id, get_subnetip_id
from test_case.cmp_compute.test_images import get_image_id
from test_case.cmp_compute.test_datacenter import get_datacenterid
from test_case.cmp_compute.test_resourcepool import get_resourcepoolid
from test_case.business_management.test_tenant import get_tenant_id, get_project_id

#从Excel获取虚拟机信息
testdata_path = Conf.get_testdata_path()
excelFile =testdata_path + os.sep + "物理资源.xlsx"
sheetName = "操作虚拟机"
disk_sheetName = "编辑虚拟机磁盘"
network_sheetName = "添加虚拟机网卡"
deleteNic_sheetName = "删除虚拟机网卡"
configCpuAndMemory_sheetName = "编辑虚拟机配置"
clone_sheetName = "克隆虚拟机"
rebuildOs_sheetName = "重装虚拟机操作系统"
migrate_sheetName = "迁移虚拟机"
snapshot_sheetName = "创建快照"

instance_data = OperationExcleData(excelFile, sheetName).getcase_tuple()
instance_disk_data = OperationExcleData(excelFile, disk_sheetName).getcase_tuple()
instance_network_data = OperationExcleData(excelFile, network_sheetName).getcase_tuple()
instance_deleteNic_data = OperationExcleData(excelFile,deleteNic_sheetName).getcase_tuple()
instance_configCpuAndMemory_data = OperationExcleData(excelFile, configCpuAndMemory_sheetName).getcase_tuple()
instance_clone_data = OperationExcleData(excelFile, clone_sheetName).getcase_tuple()
instance_rebuildOs_data = OperationExcleData(excelFile, rebuildOs_sheetName).getcase_tuple()
instance_migrate_data = OperationExcleData(excelFile, migrate_sheetName).getcase_tuple()
instance_snapshot_data = OperationExcleData(excelFile, snapshot_sheetName).getcase_tuple()

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
    assert  instance_powerOn_response["status"] == 200

    # 虚拟机开机后等待60s
    time.sleep(60)

#克隆虚拟机
@pytest.mark.parametrize("cloned_vmname, resourcepool, count, region, tenant, project, hypervisorType, name,ostype, cpu, memory, network, subnet, ipaddress",instance_clone_data)
def test_instance_clone(uri, headers, cloned_vmname, resourcepool, count, region, tenant, project, hypervisorType, name, ostype, cpu, memory, network, subnet, ipaddress):
    instance_id = get_instance_id(uri, headers, cloned_vmname, resourcepool)
    instance_clone_url = create_instance_url + "/" + str(instance_id) + "/clone"
    region_id = get_datacenterid(uri, headers, region)
    resourcepool_id = get_resourcepoolid(uri, headers, resourcepool)
    tenant_id = get_tenant_id(uri, headers, tenant)
    project_id = get_project_id(uri, headers, project)
    disk = get_instance_disks(uri, headers, cloned_vmname, resourcepool)
    nic = get_intance_nics(uri, headers, cloned_vmname, resourcepool)
    network_id = get_network_id(uri, headers, network)
    subnet_id = get_subnet_id(uri, headers, network, subnet)
    ip_id = get_subnetip_id(uri, headers, network, subnet, ipaddress)
    object_id = get_object_id(uri,headers, resourcepool,network)
    instance_clone_param =[{
        "count" : count,
        "regionId" : region_id,
        "resourcePoolId" : resourcepool_id,
        "vdcId" : tenant_id,
        "projectId" : project_id,
        "hypervisorType" : hypervisorType,
        "name" : name,
        "description" : "",
        "imageId" : "" ,
        "osType" : ostype,
        "cpu" : cpu,
        "memory" : memory,
        "osDatastore" : "",
        "disks" : [{
            "os" : disk["os"],
            "size" : disk["size"],
            "id" : None,
            "name" : disk["name"],
            "diskId" : None,
            "diskName" : disk["diskName"],
            "instanceId" : None,
            "type" : disk["type"],
            "configs" : {
                "datastore" : ""
            }
        }],
        "nics" : [{
            "id" : "",
            "instanceId" : "",
            "networkId" : network_id,
            "subnetId" : subnet_id,
            "ipId" : ip_id,
            "ip" : ipaddress,
            "targetId": object_id,
            "type" : nic["type"],
        }]
  }]

    instance_clone_response = requests.post(url = uri + instance_clone_url,
                                            headers = headers,
                                            data = json.dumps(instance_clone_param)).json()
    assert instance_clone_response["status"] == 200
    time.sleep(300)

#虚拟机挂起
@pytest.mark.parametrize("vmname,resourcepool", instance_data)
def test_instance_suspend(uri, headers, vmname, resourcepool):
    instance_id = get_instance_id(uri, headers, vmname, resourcepool)
    instance_suspend_url = create_instance_url +"/" + str(instance_id) + "/suspend"
    instance_suspend_response =  requests.post(url = uri + instance_suspend_url,
                                               headers = headers).json()
    assert  instance_suspend_response["status"] == 200
    #虚拟机挂起后等待
    time.sleep(120)

#虚拟机恢复
@pytest.mark.parametrize("vmname,resourcepool", instance_data)
def test_instance_resume(uri, headers, vmname, resourcepool):
    instance_id = get_instance_id(uri, headers, vmname, resourcepool)
    instance_resume_url = create_instance_url +"/" + str(instance_id) + "/resume"
    instance_resume_response =  requests.post(url = uri + instance_resume_url,
                                               headers = headers).json()
    assert  instance_resume_response["status"] == 200
    #虚拟机恢复后等待15s
    time.sleep(120)

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

    #虚拟机硬重启后等待
    time.sleep(60)

#虚拟机软重启

@pytest.mark.parametrize("vmname, resourcepool", instance_data)
def test_instance_rebootOS(uri, headers, vmname, resourcepool):
    instance_id = get_instance_id(uri, headers, vmname, resourcepool)
    instance_rebootOS_url = create_instance_url +"/" + str(instance_id) + "/rebootOS"
    instance_rebootOS_data = {
        "instanceId": instance_id
    }
    instance_rebootOS_response = requests.post(url = uri + instance_rebootOS_url,
                                              headers = headers,
                                              data = json.dumps(instance_rebootOS_data)).json()
    assert instance_rebootOS_response["status"] == 200

    #虚拟机软重启后等待
    time.sleep(60)

#虚拟机关闭操作系统

@pytest.mark.parametrize("vmname, resourcepool", instance_data)
def test_instance_shutdownOS(uri, headers, vmname, resourcepool):
    instance_id = get_instance_id(uri, headers, vmname, resourcepool)
    instance_shutdownOS_url = create_instance_url +"/" + str(instance_id) + "/shutdownOS"
    instance_shutdownOS_data = {
        "instanceId": instance_id
    }
    instance_shutdownOS_response = requests.post(url = uri + instance_shutdownOS_url,
                                              headers = headers,
                                              data = json.dumps(instance_shutdownOS_data)).json()
    assert instance_shutdownOS_response["status"] == 200

    #虚拟机软重启后等待120s
    time.sleep(120)

#编辑配置
@pytest.mark.parametrize("cpu, memory, name, resourcepool", instance_configCpuAndMemory_data)
def test_instance_configCpuAndMemory(uri, headers, cpu, memory, name, resourcepool):
    instance_id = get_instance_id(uri, headers, name, resourcepool )
    vmName =  get_instance_vmName(uri, headers, name, resourcepool)
    configCpuAndMemory_url = create_instance_url + "/" + str(instance_id) +"/configCpuAndMemory"
    configCpuAndMemory_data = {
        "cpu": cpu,
        "memory": memory,
        "vmName": vmName,
        "name": name
    }
    configCpuAndMemory_response = requests.put(url= uri + configCpuAndMemory_url,
                                               headers = headers,
                                               data=json.dumps(configCpuAndMemory_data)).json()
    assert configCpuAndMemory_response["status"] == 200

#编辑磁盘
@pytest.mark.parametrize("vmname, resourcepool, name, os, size, type, datastore", instance_disk_data)
def test_instance_disks(uri, headers, vmname, resourcepool, name, os, size, type, datastore):
    instance_id = get_instance_id(uri, headers, vmname, resourcepool)
    instance_disks_url = create_instance_url + "/" + str(instance_id) + "/disks"
    instance_addDisk_data = {
        "name": name,
        "os": os,
        "size": size,
        "type": type,
        "configs":{
            "datastore": datastore
        }
    }

    instance_addDisk_response = requests.post(url = uri + instance_disks_url,
                                                  headers = headers,
                                                  data = json.dumps(instance_addDisk_data)).json()
    assert instance_addDisk_response["status"] == 200


#添加网卡
@pytest.mark.parametrize("vmname, resourcepool, resourcepoolType, network, subnet, ipaddress, type", instance_network_data)
def test_instance_nic(uri, headers, vmname, resourcepool, resourcepoolType, network, subnet, ipaddress, type):
    instance_id = get_instance_id(uri, headers, vmname, resourcepool)
    networkId = get_network_id(uri, headers, network)
    subnetId = get_subnet_id(uri, headers,network,subnet)
    ipId = get_subnetip_id(uri, headers, network, subnet, ipaddress)
    targetId = get_object_id(uri, headers, resourcepool, network)
    instance_nic_url = create_instance_url + "/" + str(instance_id) + "/nics"
    if resourcepoolType == "vmware":
        instance_addNetwork_data = {
            "networkId": networkId,
            "subnetId": subnetId,
            "ipId": ipId,
            "ip": ipaddress,
            "targetId": targetId,
            "type": type
        }
        instance_addNetwork_response = requests.post(url = uri + instance_nic_url,
                                                     headers = headers,
                                                     data = json.dumps(instance_addNetwork_data)).json()
        assert instance_addNetwork_response["status"] == 200
    elif resourcepoolType == "openstack":
        instance_addNetwork_data = {
            "networkId": networkId,
            "subnetId": subnetId,
            "ipId": ipId,
            "ip": ipaddress
        }
        instance_addNetwork_response = requests.post(url=uri + instance_nic_url,
                                                     headers=headers,
                                                     data=json.dumps(instance_addNetwork_data)).json()
        assert instance_addNetwork_response["status"] == 200

#根据虚拟机id获取虚拟机网卡信息
def get_instance_nicId(uri, headers, instance_name, resourcepool, ipaddress):
    instance_id = get_instance_id(uri, headers, instance_name, resourcepool)
    get_instance_nics_url = create_instance_url + "/" + str(instance_id) + "/nics"
    get_instance_nics_response = requests.get(url=uri + get_instance_nics_url,
                                              headers = headers).json()
    for nic in get_instance_nics_response["data"]:
        if nic["ip"] == ipaddress:
            return nic["id"]

#根据网卡id删除虚拟机网卡
@pytest.mark.parametrize("vmname, resourcepool, ipaddress", instance_deleteNic_data)
def test_instance_delete_nic(uri, headers, vmname, resourcepool, ipaddress):
    instance_id = get_instance_id(uri, headers, vmname, resourcepool)
    nic_id = get_instance_nicId(uri, headers, vmname, resourcepool, ipaddress)
    instance_deleteNic_url = create_instance_url + "/" + str(instance_id) + "/nics/" + str(nic_id)
    instance_deleteNic_response = requests.delete(url=uri + instance_deleteNic_url,
                                                  headers = headers).json()
    assert instance_deleteNic_response["status"] == 200

#同步虚拟机
@pytest.mark.parametrize("vmname, resourcepool", instance_data)
def test_instance_sync(uri, headers, vmname, resourcepool):
    instance_id = get_instance_id(uri, headers, vmname, resourcepool)
    instance_sync_url = create_instance_url + "/sync"
    instance_sync_data = [instance_id]
    instance_sync_response = requests.post(url = uri + instance_sync_url,
                                          headers = headers,
                                          data = json.dumps(instance_sync_data)).json()
    assert instance_sync_response["status"] == 200

#重置操作系统
@pytest.mark.parametrize("vmname, resourcepool", instance_data)
def test_instance_resetOs(uri, headers, vmname, resourcepool):
    instance_id = get_instance_id(uri, headers, vmname, resourcepool)
    instance_resetOs_url = create_instance_url + "/" + str(instance_id) + "/resetOs"
    instance_resetOs_response = requests.put(url = uri + instance_resetOs_url,
                                             headers = headers).json()
    assert instance_resetOs_response["status"] == 200
    #重置虚拟机后等待5min，需要等待虚拟机创建完成
    time.sleep(300)


#重装操作系统
@pytest.mark.parametrize("vmname, resourcepool, image", instance_rebuildOs_data)
def test_instance_rebuildOs(uri, headers, vmname, resourcepool, image):
    instance_id = get_instance_id(uri, headers, vmname, resourcepool)
    image_id = get_image_id(uri, headers, image)
    instance_rebuildOs_url = create_instance_url + "/" + str(instance_id) +"/rebuildOs/" + str(image_id)
    instance_rebuildOs_response = requests.put(url = uri + instance_rebuildOs_url,
                                               headers = headers).json()
    assert instance_rebuildOs_response["status"] == 200
    time.sleep(300)


#虚拟机迁移
@pytest.mark.parametrize("vmname, resourcepool, hostname, storename", instance_migrate_data)
def test_instance_migrate(uri, headers, vmname, resourcepool, hostname, storename):
    instance_id = get_instance_id(uri, headers, vmname, resourcepool)
    instance_migrate_url = create_instance_url + "/" + str(instance_id) + "/migrate"
    instance_migrateHost_data = {
        "instanceId": instance_id,
        "migrateType": "MigrateHost",
        "hostName": hostname
    }
    instance_migrateStore_data = {
         "instanceId": instance_id,
         "migrateType": "MigrateStore",
         "storeName": storename
    }
    instance_migrateHost_response = requests.put(url = uri + instance_migrate_url,
                                                 headers = headers,
                                                 data = json.dumps(instance_migrateHost_data)).json()
    assert instance_migrateHost_response["status"] == 200

    time.sleep(30)

    instance_migrateStore_response = requests.put(url = uri + instance_migrate_url,
                                                  headers = headers,
                                                  data = json.dumps(instance_migrateStore_data)).json()
    assert instance_migrateStore_response["status"] == 200

#创建快照
@pytest.mark.parametrize("vmname, resourcepool, name, desc, memory, quiesce", instance_snapshot_data)
def test_instance_createSnapshot(uri, headers, vmname, resourcepool, name, desc, memory, quiesce):
    instance_id = get_instance_id(uri, headers, vmname, resourcepool)
    instance_createSnapshot_url = create_instance_url + "/" + str(instance_id) + "/snapshots"
    instance_createSnapshot_data = {
        "instanceId": instance_id,
        "name": name,
        "desc": desc,
        "memory": memory,
        "quiesce": quiesce
    }
    instance_createSnapshot_response = requests.post(url = uri + instance_createSnapshot_url,
                                               headers = headers,
                                               data = json.dumps(instance_createSnapshot_data)).json()
    assert instance_createSnapshot_response["status"] == 200
    #创建快照后等待2min
    time.sleep(120)

#获取第一个快照id
def get_snapshot_id(uri, headers, vmname, resourcepool):
    instance_id = get_instance_id(uri, headers, vmname, resourcepool)
    get_snapshot_url = create_instance_url + "/" + str(instance_id) + "/snapshots"
    get_snapshot_response = requests.get(url = uri + get_snapshot_url,
                                         headers = headers).json()
 #   if get_snapshot_response["name"] == snapshotName:
    return get_snapshot_response["data"][0]["id"]

#恢复快照
#@pytest.mark.parametrize("vmname, resourcepool", instance_data)
def test_instance_revertSnapshot(uri, headers):
    vmname = instance_snapshot_data[0][0]
    resourcepool = instance_snapshot_data[0][1]
    instance_id = get_instance_id(uri, headers, vmname, resourcepool)
    snapshot_id = get_snapshot_id(uri, headers, vmname,resourcepool)
    instance_revertSnapshot_url = create_instance_url + "/" + str(instance_id) + "/snapshots/" + str(snapshot_id)
    instance_revertSnapshot_response = requests.put(url = uri + instance_revertSnapshot_url,
                                                    headers = headers).json()
    assert instance_revertSnapshot_response["status"] == 200
    #恢复快照后等待30s
    time.sleep(30)

#删除快照
def test_instance_deleteSnapshot(uri, headers):
    vmname = instance_snapshot_data[0][0]
    resourcepool = instance_snapshot_data[0][1]
    instance_id = get_instance_id(uri, headers, vmname, resourcepool)
    snapshot_id = get_snapshot_id(uri, headers, vmname,resourcepool)
    instance_deleteSnapshot_url = create_instance_url + "/" + str(instance_id) + "/snapshots/" + str(snapshot_id)
    instance_deleteSnapshot_response = requests.delete(url = uri + instance_deleteSnapshot_url,
                                                    headers = headers).json()
    assert instance_deleteSnapshot_response["status"] == 200

#删除虚拟机
@pytest.mark.parametrize("vmname, resourcepool", instance_data)
def test_instance_delete(uri, headers, vmname, resourcepool):
    instance_id = get_instance_id(uri, headers, vmname, resourcepool)
    instance_delete_url = create_instance_url + "/" + str(instance_id)
    instance_delete_response = requests.delete(url= uri + instance_delete_url,
                                               headers = headers).json()
    assert instance_delete_response["status"] == 200
