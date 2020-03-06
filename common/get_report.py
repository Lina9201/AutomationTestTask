# -*- coding: utf-8 -*-
# @Time    : 2020/3/6 9:11
# @Author  : zhuxuefei
import subprocess
from utils.LogUtil import my_log

log = my_log()
def allure_report(report_path, report_html):
    """
    生成测试报告
    :param report_path: 原始测试报告结果路径
    :param report_html: 生产allure html报告结果路径
    :return:
    """
    #执行命令 allure generate
    allure_comand = "allure generate %s -o %s --clean"%(report_path, report_html)
    log.info("生成测试报告")
    try:
        subprocess.call(allure_comand, shell=True)
    except:
        log.error("用例执行失败，请检查测试环境相关配置")


