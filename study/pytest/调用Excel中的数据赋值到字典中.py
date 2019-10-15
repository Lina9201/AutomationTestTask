import xlrd

def read_excel_dic(dataname, Sheetname):
    # 打开excel表，填写路径
    workbook = xlrd.open_workbook(r'%s' % dataname)
    # 找到sheet页
    table = workbook.sheet_by_name(Sheetname)
    # 获取总行数总列数
    row_Num = table.nrows
    col_Num = table.ncols

    param = []
    key = table.row_values(0)  # 这是第一行数据，作为字典的key值

    if row_Num <= 1:
        print("没数据")
    else:
        j = 1
        for i in range(1, row_Num):
            paramrow = {}
            paramcol = table.row_values(j)
            for x in range(col_Num):
                # 把key值对应的value赋值给key，每行循环
                paramrow[key[x]] = paramcol[x]
            j += 1
            # 把字典加到列表中
            param.append(paramrow)
    return param

print(read_excel_dic("D:\测试数据.xlsx", "创建VLAN池"))
# param_create_vlanpool = read_excel_dic("D:\测试数据.xlsx", "创建VLAN池")
# param_create_vlanpoola = []
# a = []
# b = []
# for i in range(len(param_create_vlanpool)):
#     a.append(param_create_vlanpool[i])
#     b.append(tuple(a))
#     b = a
#     param_create_vlanpoola.append(b)
# print(param_create_vlanpoola)