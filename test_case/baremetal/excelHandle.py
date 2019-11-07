import os

import xlrd


# 参数为Excel文件路径和sheet名，返回param
def excelHandle(excel_dir, sheetName):
    sheet = xlrd.open_workbook(excel_dir).sheet_by_name(sheetName)  # 根据excel文件路径和sheet名获取sheet
    cols = sheet.ncols  # 获取列数
    rows = sheet.nrows  # 获取行数

    # 将Excel中的单元格数据放到param中，最终param的格式形如[(1.0, 'a'), (2.0, 'b'), (3.0, 'c')]
    param = []
    l = []
    if rows >= 1 and cols > 0:
        for i in range(1, rows):
            for j in range(cols):
                v=sheet.cell(i, j).value
                ctype=sheet.cell(i, j).ctype
                if ctype == 2 and v % 1 == 0.0:  # ctype为2且为浮点
                    cell = int(v)
                else:
                    cell=v
                l.append(cell)
            if len(l) == 1:
                param.append(l[0])
            else:
                param.append(tuple(l))
            l = []

    return param


if __name__ == '__main__':
    print(os.getcwd())
