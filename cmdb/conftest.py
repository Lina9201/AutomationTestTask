import pytest
import requests

authentication_url_path = "/v1/tokens"

json_login = {
    "authType": "password",
    "params": {
        "username": "vic",
        "password": "12345678"
    }
}


def pytest_addoption(parser):
    parser.addoption("--ip", action="store", default="172.21.1.132", help="please input target VM ip.")
    parser.addoption("--port", action="store", default="8000", help="please input target service port.")


@pytest.fixture(scope="session")
def ip(request):
    return request.config.getoption("--ip")


@pytest.fixture(scope="module")
def port(request):
    return request.config.getoption("--port")


@pytest.fixture(scope="module")
def ip_address(ip, port):
    ip_address = "http://%s:%s" % (ip, port)
    return ip_address


@pytest.fixture(scope="module")
def auth_token(ip, port):
    ip_address = "http://%s:%s" % (ip, port)
    headers = {"User-Agent": "automation",
               "content-type": "application/json;charset=UTF-8"
               }

    post_response = requests.post(url=ip_address + authentication_url_path,
                                  json=json_login,
                                  headers=headers)

    assert post_response.status_code == requests.status_codes.codes.OK
    resp_payload = post_response.json()
    assert resp_payload['status'] == 200  # to be defined.
    auth_token = resp_payload['data']['key']

    return auth_token


@pytest.fixture(scope="module")
def headers(ip, port):
    ip_address = "http://%s:%s" % (ip, port)
    headers = {"User-Agent": "automation",
               "content-type": "application/json;charset=UTF-8"
               }

    post_response = requests.post(url=ip_address + authentication_url_path,
                                  json=json_login,
                                  headers=headers)

    assert post_response.status_code == requests.status_codes.codes.OK
    resp_payload = post_response.json()
    assert resp_payload['status'] == 200  # to be defined.
    auth_token = resp_payload['data']['key']

    headers = {"User-Agent": "automation",
               "content-type": "application/json;charset=UTF-8",
               "T-AUTH-TOKEN": auth_token}
    return headers
