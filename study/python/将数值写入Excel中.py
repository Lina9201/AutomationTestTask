import xlwt

def writeexcel():
    stus = [['年', '月'], ['2018', '10'], ['2017', '9'], ['2016', '8']]
    Excel = xlwt.Workbook()
    # 新建excel
    sheet = Excel.add_sheet('B')
    #新建页签B
    row = 0
    for stu in stus:
        col = 0
        for s in stu:
            sheet.write(row, col, s)
            #开始写入
            col = col + 1
        row = row + 1
    Excel.save(r'D:\测试数据1.xlsx') #保存
writeexcel()