# -*- coding: utf-8 -*-
# @Time    : 2019/10/8 14:33
# @Author  : zhuxuefei

import xlrd
import openpyxl

class OperationExcleData():
    """对excel进行操作，包括读取请求参数，和填写操作结果"""
    def __init__(self, excelFile, sheetName):
        self.sheetName = sheetName
        self.excelFile = excelFile
        self.caseList = []

    def getCaseList(self, excelFile, sheetName):
        """
        获取excel中维护的测试用例，每个{}包含字段和对应值的键对值
        :param excelFile: 传入excel文件的名字
        :param sheetName: 传入接口所在sheet页的名字
        :return: 最终返回所有的测试用例
        """
        readExcel = xlrd.open_workbook(excelFile)
        sheet = readExcel.sheet_by_name(sheetName)
        # 获取excel的行数和列数
        trows = sheet.nrows
        tcols = sheet.ncols
        for i in range(2, trows):
            tmpdict = {}
            for j in range(2, tcols):
                case_key = sheet.cell_value(0, j)
                case_value = sheet.cell_value(i, j)
                # if sheet.cell_value(0, j) != "" and sheet.cell_value(0, j + 1) == "":
                #     childdict = {}
                if sheet.cell_value(1, j) != "":
                    childdict = {}
                    childcase_key = sheet.cell_value(1, j)
                    childdict[childcase_key] = sheet.cell_value(i, j)
                    case_value = childdict
                if case_key != "":
                    tmpdict[case_key] = case_value
            self.caseList.append(tmpdict)
        return self.caseList


    def writeExcel(self, excelFile, sheetName, writeData):
        writeExcel = openpyxl.load_workbook(excelFile)
        try:
            writeSheet = writeExcel[sheetName]
            writeSheet["C2"]=writeData
            writeExcel.save(excelFile)
        except Exception as e:
            raise
        finally:
            pass

if __name__=="__main__":
    excelFile = "E:\\AutomationTestTask\\test_data\\cmp\\资源池.xlsx"
    sheetName = "添加资源池"
    ed = OperationExcleData(excelFile, sheetName)
    resourcepool_data = ed.getCaseList(excelFile, sheetName)
    print(resourcepool_data)








