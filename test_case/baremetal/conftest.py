import os
from time import sleep

import pytest
import requests

the_ip="172.50.10.42"
the_port="8000"

the_ip="172.50.10.42"
the_port="8000"

login_api="/v1/tokens"
logout_api="/v1/tokens/logout"
user="jfquanneng"
password="0V7PrMAZUVgx92QWSIvfmw=="

if "baremetal" in os.getcwd():
    dir="../../"
else:
    dir=""

@pytest.fixture()
def token(ip,port):
    token = ""
    url="http://%s:%s/%s" % (ip,port,login_api)
    headers = {"User-Agent": "automation",
               "content-type": "application/json;charset=UTF-8"
               }
    json={
    "authType": "password",
    "params": {
        "username": user,
        "password": password
    }
    }
    result = requests.post(url, headers=headers, json=json).json()
    try:
        authtoken = result["data"]["key"]
    except:
        sleep(0.00001)

    return authtoken


