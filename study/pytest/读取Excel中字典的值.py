import xlrd

excel_path = r'D:\测试数据.xlsx'
data = xlrd.open_workbook(excel_path)
table = data.sheet_by_name("Sheet3")
rows = table.nrows
cols = table.ncols
for i in range(rows):
    list1 = table.row_values(i)
    for i in list1:
        if eval(i).get('username'):
            print(eval(i)['username'])
        elif eval(i).get('password'):
            print(eval(i)['password'])
