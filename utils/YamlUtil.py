# -*- coding: utf-8 -*-
# @Time    : 2019/10/24 22:50
# @Author  : zhuxuefei
import os
import yaml

class YamlReader:
    # 初始化，文件是否存在
    def __init__(self, yamlf):
        if os.path.exists(yamlf):
            self.yamlf = yamlf
        else:
            raise FileNotFoundError("文件不存在")
        self._data = None
        self._data_all = None


    # Yaml单个文档读取
    def yamldata(self):
        if not self._data:
            with open(self.yamlf, "rb") as f:
                self._data = yaml.safe_load(f)
        return self._data

    # Yaml多个文档读取
    def yamldata_all(self):
        if not self._data:
            with open(self.yamlf, "rb") as f:
                self._data = yaml.safe_load_all(f)
        return self._data


