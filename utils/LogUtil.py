# -*- coding: utf-8 -*-
# @Time    : 2019/10/14 11:20
# @Author  : zhuxuefei
from config import Conf
from config.Conf import ConfigYaml
import datetime
import os
import logging
log_l = {
    "info": logging.INFO,
    "debug": logging.DEBUG,
    "warning": logging.WARNING,
    "error": logging.ERROR
}

class LogUtil:
    def __init__(self, log_file, log_name, log_level):
        self.log_file = log_file
        self.log_name = log_name
        self.log_level = log_level

        # 设置logger名称
        self.logger = logging.getLogger(self.log_name)
        # 设置logger级别
        self.logger.setLevel(log_l[self.log_level])
        # 判断handlers是否存在
        if not self.logger.handlers:
            # 输出到控制台
            fh_stream = logging.StreamHandler()
            fh_stream.setLevel(log_l[self.log_level])
            formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
            fh_stream.setFormatter(formatter)
            # 写入文件
            fh_file = logging.FileHandler(self.log_file)
            fh_file.setLevel(log_l[self.log_level])
            fh_file.setFormatter(formatter)

            # 添加handler
            self.logger.addHandler(fh_stream)
            self.logger.addHandler(fh_file)

#log目录
log_path = Conf.get_log_path()
#当前时间
current_time = datetime.datetime.now().strftime("%Y-%m-%d")
#扩展名
log_extension = ConfigYaml().get_log_extension()
logfile = os.path.join(log_path,current_time+log_extension)
log_level = ConfigYaml().get_log_config()

# 初始化log工具类，提供给其他类用
def my_log(log_name = __file__):
    return LogUtil(log_file=logfile,log_name=log_name,log_level=log_level).logger

if __name__ == "__main__":
    print(__file__)
    print(log_level)
    my_log().debug("this is debug")


