# -*- coding: utf-8 -*-
# @Time    : 2019/10/14 10:47
# @Author  : zhuxuefei

import json
from utils.LogUtil import my_log
import allure

class AssertUtil:
    def __init__(self):
        self.log = my_log("AssertUtil")

    def assert_code(self, code, expected_code):
        """
        验证返回code一致
        :param code:
        :param expected_code:
        :return:
        """
        try:
            assert int(code) == int(expected_code)
            return True
        except:
            self.log.error("响应code error, 响应code is %s,期望code is %s"%(code, expected_code))
            allure.attach("响应code error, 响应code is %s,期望code is %s" % (code, expected_code))
            raise

    def assert_body(self, body, expected_body):
        """
        验证返回结果内容相等
        :param body:
        :param expected_body:
        :return:
        """
        try:
            assert body == expected_body
            return True
        except:
            self.log.error("响应body error, 响应body is %s,期望body is %s" % (body, expected_body))
            allure.attach("响应body error, 响应body is %s,期望body is %s" % (body, expected_body))
            raise


    def assert_in_body(self, body, excepted_body):
        """
        验证返回结果是否包含预期的结果
        :param body:
        :param excepted_body:
        :return:
        """
        try:
            body = json.dumps(body,ensure_ascii=False)
            assert excepted_body in body
            return True
        except:
            self.log.error("不包含或者body是错误, 响应body is %s,期望body is %s" % (body, excepted_body))
            allure.attach("不包含或者body是错误, 响应body is %s,期望body is %s" % (body, excepted_body))
            raise