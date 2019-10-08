# -*- coding: utf-8 -*-
# @Time    : 2019/10/8 14:33
# @Author  : zhuxuefei

import xlrd

class OperationExcleData():
    """对excel进行操作，包括读取请求参数，和填写操作结果"""
    def __init__(self, excelFile):
        self.excelFile = excelFile
        self.caseList = []

    """传入excel用例名称，其中元素是{}，每个{}包含字段和对应值的键对值"""
    def getCaseList(self, excelFile):
        readExcel = xlrd.open_workbook(excelFile)
        # 获取excel的第一个sheet
        sheet = readExcel.sheet_by_index(0)
        print(sheet.name)
        # 获取excel的行数
        trows = sheet.nrows
        for n in range(1, trows):
            tmpdict = {}
            tmpdict["name"] = sheet.cell_value(n, 2)
            tmpdict["description"] = sheet.cell_value(n, 3)
            self.caseList.append(tmpdict)
        return self.caseList



