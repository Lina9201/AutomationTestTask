
import pytest
import requests

from baremetal.conftest import the_ip, the_port
from baremetal.excelHandle import excelHandle

ip = the_ip
port = the_port
excel_dir = "test_host.xlsx"


# 根据主机名获取主机id
def get_host_id(name, resource_pool_id, token):
    url = "http://%s:%s/admin/v1/hypersivor/baremetal/hosts?pageNum=1&pageSize=10&resource_pool_id=%s" % (
    ip, port, resource_pool_id)
    headers = {"T-AUTH-TOKEN": token}
    r = requests.get(url, headers=headers).json()
    l = r["data"]["list"]
    for i in l:
        if i["name"] == name:
            return i["id"]
    return ""


# 注册主机连接测试
@pytest.mark.parametrize("resource_pool_id,ipmi_ip,user,passwd", excelHandle(excel_dir, "test_test_connect"))
def test_test_connect(token, resource_pool_id, ipmi_ip, user, passwd):
    url = "http://%s:%s/admin/v1/hypersivor/baremetal/hosts/ipmi?resource_pool_id=%s" % (ip, port, resource_pool_id)
    headers = {"Content-Type": "application/json",
               "T-AUTH-TOKEN": token}
    json = [
        {
            "ip": ipmi_ip,
            "user": user,
            "passwd": passwd
        }
    ]
    r = requests.post(url, headers=headers, json=json).json()
    assert r["status"] == 200
    assert r["data"] == []


# 创建主机
@pytest.mark.parametrize("resource_pool_id,name,ipmi_ip,ipmi_user,ipmi_password,pxe_mac,enable_public,up_port", \
                         excelHandle(excel_dir, "test_add_host"))
def test_add_host(token, resource_pool_id, name, ipmi_ip, ipmi_user, ipmi_password, pxe_mac, enable_public, up_port):
    url = "http://%s:%s/admin/v1/hypersivor/baremetal/hosts?resource_pool_id=%s" % (ip, port, resource_pool_id)
    headers = {"Content-Type": "application/json",
               "T-AUTH-TOKEN": token}
    json = [
        {
            "name": name,
            "resourceId": resource_pool_id,
            "ipmi_ip": ipmi_ip,
            "ipmi_user": ipmi_user,
            "ipmi_password": ipmi_password,
            "pxe_mac": pxe_mac,
            "enable_public": enable_public,
            "up_port": up_port
        }
    ]
    r = requests.post(url=url, headers=headers, json=json).json()
    assert r["status"] == 200


# 查询主机
@pytest.mark.parametrize("name,resource_pool_id", excelHandle(excel_dir, "test_get_host"))
def test_get_host(token, name, resource_pool_id):
    url = "http://%s:%s/admin/v1/hypersivor/baremetal/hosts/%s?resource_pool_id=%s" % \
          (ip, port, get_host_id(name, resource_pool_id, token), resource_pool_id)
    headers = {"T-AUTH-TOKEN": token}
    r = requests.get(url=url, headers=headers).json()
    assert r["status"] == 200
    assert r["data"]["name"] == name


# 查询主机规格
@pytest.mark.parametrize("resource_pool_id,host_status,maintenance,project_id,cpu_mem",
                         excelHandle(excel_dir, "test_host_spec"))
def test_host_spec(token, resource_pool_id, host_status, maintenance, project_id, cpu_mem):
    url = "http://%s:%s/admin/v1/hypersivor/baremetal/hosts/flavors?resource_pool_id=%s&host_status=%s\
    &maintenance=%s&project_id=%s" % (ip, port, resource_pool_id, host_status, maintenance, project_id)
    headers = {"T-AUTH-TOKEN": token}
    r = requests.get(url, headers=headers).json()
    assert r["status"] == 200
    assert r["data"][0] == cpu_mem


# 编辑主机
@pytest.mark.parametrize("name,resource_pool_id,pxe_mac,vdc_id,project_id,enable_public",\
                         excelHandle(excel_dir,"test_edit_host"))
def test_edit_host(token,name,resource_pool_id,pxe_mac,vdc_id,project_id,enable_public):
    host_id=get_host_id(name,resource_pool_id,token)
    url="http://%s:%s/admin/v1/hypersivor/baremetal/hosts?id=%s&resource_pool_id=%s"%(ip,port,\
        host_id,resource_pool_id)
    headers = {"Content-Type": "application/json",
               "T-AUTH-TOKEN": token}
    json={
	"id": host_id,
	"name": name,
	"pxe_mac": pxe_mac,
	"vdc_id": vdc_id,
	"project_id": project_id,
	"enable_public": enable_public
}
    r=requests.put(url,headers=headers,json=json).json()
    assert r["status"]==200


# 主机列表
@pytest.mark.parametrize("resource_pool_id", excelHandle(excel_dir, "test_get_hostlist"))
def test_get_hostlist(token, resource_pool_id):
    url = "http://%s:%s/admin/v1/hypersivor/baremetal/hosts?pageNum=1&pageSize=10&resource_pool_id=%s" % (
    ip, port, resource_pool_id)
    headers = {"T-AUTH-TOKEN": token}
    r = requests.get(url=url, headers=headers).json()
    assert r["status"] == 200


# 删除主机
@pytest.mark.parametrize("name,resource_pool_id", excelHandle(excel_dir, "test_delete_host"))
def test_delete_host(name, resource_pool_id, token):
    url = "http://%s:%s/admin/v1/hypersivor/baremetal/hosts/%s?resource_pool_id=%s" % \
          (ip, port, get_host_id(name, resource_pool_id, token), resource_pool_id)
    headers = {"Content-Type": "application/json",
               "T-AUTH-TOKEN": token}
    r = requests.delete(url, headers=headers).json()
    assert r["status"] == 200


# 部署主机
@pytest.mark.parametrize("name,resource_pool_id", excelHandle(excel_dir, "test_deploy_host"))
def test_deploy_host(name, resource_pool_id, token):
    url = "http://%s:%s/admin/v1/hypersivor/baremetal/hosts/%s/deploy?resource_pool_id=%s" % \
          (ip, port, get_host_id(name, resource_pool_id, token), resource_pool_id)
    headers = {"Content-Type": "application/x-www-form-urlencoded",
               "T-AUTH-TOKEN": token}
    r = requests.put(url, headers).json()
    assert r["status"] == 200
