import xlrd

def readexcel():
    #打开excel
    openworkbook = xlrd.open_workbook(r'D:\测试数据.xlsx')

    #打印页签名
    print(openworkbook.sheet_names())

    #打开页签
    table = openworkbook.sheet_by_name("Sheet1")

    #获取行数
    nrows = table.nrows

    #获取列数
    ncols = table.ncols

    #打印行数和列数
    print(nrows,ncols)

    #取出第2行第2列的值
    cell_A = table.cell(1,0).value
    print(cell_A)

# if __name__ == '__name__':
readexcel()

