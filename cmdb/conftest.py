import pytest


@pytest.fixture(scope="module")
def auth_token():
    return ''


def pytest_addoption(parser):
    parser.addoption("--ip", action="store", default="172.21.1.132", help="please input target VM ip.")
    parser.addoption("--port", action="store", default="8888", help="please input target service port.")


@pytest.fixture
def ip(request):
    return request.config.getoption("--ip")


@pytest.fixture
def port(request):
    return request.config.getoption("--port")
