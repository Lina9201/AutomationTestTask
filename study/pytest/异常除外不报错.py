
"""有关于python里raise显示引发异常的方法:
当程序出错时,python会自动触发异常,也可以通过raise显示引发异常
一旦执行了raise语句,raise之后的语句不在执行
如果加入了try,except,那么except里的语句会被执行
"""

try:
    s = "1"
    if s is None:# 如果s是空，那么打印's是空对象'，并且raise后面的打印s长度的语句不执行
        print('s是空对象')
        raise NameError
    print(len(s))

except Exception:# 出现了异常，执行打印'空对象没有长度'
    print('空对象没有长度')
