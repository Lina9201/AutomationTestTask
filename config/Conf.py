# -*- coding: utf-8 -*-
# @Time    : 2019/10/26 20:54
# @Author  : zhuxuefei

import os
from utils.YamlUtil import YamlReader

# 获取当前项目的绝对路径
current = os.path.abspath(__file__)
print(current)
BASE_DIR = os.path.dirname(os.path.dirname(current))
print(BASE_DIR)

# 定义config目录的路径
_config_path = BASE_DIR + os.sep + "config"

# 定义report目录的路径
_report_path = BASE_DIR + os.sep + "report"

# 定义test_data目录的路径
_testdata_path = BASE_DIR + os.sep + "test_data"

# 定义db_config.yml文件的路径
_db_config_file = _config_path + os.sep + "db_conf.yml"

# 定义config.yml文件的路径
_config_file = _config_path + os.sep + "conf.yml"


# 定义logs文件的路径
_log_path = BASE_DIR + os.sep + "logs"


def get_config_path():
    return _config_path


def get_db_config_file():
    return _db_config_file

def get_config_file():
    return _config_file

def get_report_path():
    return _report_path


def get_testdata_path():
    return _testdata_path

def get_log_path():
    """
    获取Log文件路径
    :return:
    """
    return _log_path

# 读取配置文件
class ConfigYaml:
    def __init__(self):
        self.db_config = YamlReader((get_db_config_file())).yamldata()
        self.config = YamlReader((get_config_file())).yamldata()

    def get_db_config(self, db_alias):
        return self.db_config[db_alias]

    def get_log_config(self):
        """
        获取日志级别
        :return:
        """
        return self.config["BASE"]["log_level"]

    def get_log_extension(self):
        return self.config["BASE"]["log_extension"]

    


