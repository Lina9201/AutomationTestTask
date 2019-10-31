# -*- coding: utf-8 -*-
# @Time    : 2019/10/14 13:38
# @Author  : zhuxuefei

import pytest

if __name__=='__main__':
    report_path="report/baremetal"
    pytest.main(["-s", "test_case/baremetal/test_resourcepool.py", "--alluredir", report_path + "/resourcepool"])
    pytest.main(["-s","test_case/baremetal/test_image.py","--alluredir", report_path+"/image"])
    pytest.main(["-s","test_case/baremetal/test_power.py","--alluredir", report_path+"/power"])
    pytest.main(["-s", "test_case/baremetal/test_status.py", "--alluredir", report_path + "/status"])
    pytest.main(["-s", "test_case/baremetal/test_instance.py", "--alluredir", report_path + "/instance"])
    pytest.main(["-s", "test_case/baremetal/test_host.py", "--alluredir", report_path + "/host"])
