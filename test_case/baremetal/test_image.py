import pytest
import requests

from baremetal.conftest import the_ip, the_port
from baremetal.excelHandle import excelHandle

ip = the_ip
port = the_port
excel_dir = "test_image.xlsx"


# 根据镜像名查镜像id
def get_image_id(resource_pool_id, token, name):
    url = "http://%s:%s/admin/v1/hypersivor/baremetal/images?resource_pool_id=%s&pageNum=1&pageSize=10" % (
        ip, port, resource_pool_id)
    headers = {"T-AUTH-TOKEN": token}
    r = requests.get(url=url, headers=headers).json()
    list = r["data"]["list"]
    for i in list:
        if i["name"] == name:
            return i["id"]
    return ""


# 镜像文件
@pytest.mark.parametrize("resource_pool_id,file_name,file_path", excelHandle(excel_dir, "test_image_file"))
def test_image_file(token, file_name, file_path, resource_pool_id):
    url = "http://%s:%s/admin/v1/hypersivor/baremetal/images/file?resource_pool_id=%s" % (ip, port, resource_pool_id)
    headers = {"T-AUTH-TOKEN": token}
    r = requests.get(url=url, headers=headers).json()
    assert r["status"] == 200
    data = r["data"]
    l = {"file_name": file_name, "file_path": file_path}
    assert l in data


# 创建镜像
@pytest.mark.parametrize("resource_pool_id,name,os_type,os_version,image_path,image_desc",
                         excelHandle(excel_dir, "test_add_image"))
def test_add_image(token, resource_pool_id, name, os_type, os_version, image_desc, image_path):
    url = "http://%s:%s/admin/v1/hypersivor/baremetal/images?resource_pool_id=%s" % (ip, port, resource_pool_id)
    headers = {"Content-Type": "application/json",
               "T-AUTH-TOKEN": token}
    json = {"name": name, "os_type": os_type, "os_version": os_version, "image_path": image_path, "image_desc": image_desc}
    r = requests.post(url=url, headers=headers, json=json).json()
    assert r["status"] == 200


# 镜像列表
@pytest.mark.parametrize("resource_pool_id,name", excelHandle(excel_dir, "test_imagelist"))
def test_imagelist(token, resource_pool_id, name):
    url = "http://%s:%s/admin/v1/hypersivor/baremetal/images?resource_pool_id=%s&pageNum=1&pageSize=10" % (
    ip, port, resource_pool_id)
    headers = {"T-AUTH-TOKEN": token}
    r = requests.get(url=url, headers=headers).json()
    assert name in str(r)


# 查询镜像
@pytest.mark.parametrize("resource_pool_id,name", excelHandle(excel_dir, "test_get_image"))
def test_get_image(resource_pool_id, name, token):
    url = "http://%s:%s/admin/v1/hypersivor/baremetal/images/%s?resource_pool_id=%s" % \
          (ip, port, get_image_id(resource_pool_id, token, name), resource_pool_id)
    headers = {"Content-Type": "application/json",
               "T-AUTH-TOKEN": token}
    r = requests.get(url, headers=headers).json()
    assert r["status"] == 200
    assert r["data"]["name"] == name


# 编辑镜像
@pytest.mark.parametrize("resource_pool_id,name,new_name,newos_type,newos_version,new_desc",
                         excelHandle(excel_dir, "test_edit_image"))
def test_edit_image(token, resource_pool_id, name, new_name, newos_type, new_desc, newos_version):
    id = get_image_id(resource_pool_id, token, name)
    url = "http://%s:%s/admin/v1/hypersivor/baremetal/images?id=%s&resource_pool_id=%s" \
          % (ip, port, id, resource_pool_id)
    headers = {"Content-Type": "application/json",
               "T-AUTH-TOKEN": token}
    json = {"id": id, "name": new_name, "os_type": newos_type, "os_version": newos_version, \
            "image_desc": new_desc}
    r = requests.put(url, headers=headers, json=json).json()
    assert r["status"] == 200


# 删除镜像
@pytest.mark.parametrize("resource_pool_id,name", excelHandle(excel_dir, "test_delete_image"))
def test_delete_image(token, resource_pool_id, name):
    url = "http://%s:%s/admin/v1/hypersivor/baremetal/images/%s?resource_pool_id=%s" % (
    ip, port, get_image_id(resource_pool_id, \
                         token, name), resource_pool_id)
    headers = {"T-AUTH-TOKEN": token}
    r = requests.delete(url, headers=headers).json()
    assert r["status"] == 200
    assert get_image_id(resource_pool_id, token, name) == ""


# 批量删除镜像
@pytest.mark.parametrize("resource_pool_id,name1,name2", excelHandle(excel_dir, "test_multi_delete_image"))
def test_multi_delete_image(token, resource_pool_id, name1, name2):
    url = "http://%s:%s/admin/v1/hypersivor/baremetal/images?resource_pool_id=%s" % (ip, port, resource_pool_id)
    headers = {"Content-Type": "application/json",
               "T-AUTH-TOKEN": token}
    json = [get_image_id(resource_pool_id, token, name1), get_image_id(resource_pool_id, token, name2)]
    r = requests.delete(url, headers=headers, json=json).json()
    print(r)
    assert r["status"] == 200
    assert get_image_id(resource_pool_id, token, name1) == ""
    assert get_image_id(resource_pool_id, token, name2) == ""
