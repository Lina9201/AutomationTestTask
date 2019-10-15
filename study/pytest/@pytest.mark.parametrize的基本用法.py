import pytest

# 基本用法，给变量赋值多个参数
@pytest.mark.parametrize("test_input,expected", [
    ("3+5", 8),
    ("2+4", 6),
    ("6*9", 42),
])
# 函数调用变量，将变量的所有参数，从头开始依次调用
def test_eval(test_input, expected):
    assert eval(test_input) == expected

# 延伸用法，将参数赋值给一个变量，再将变量赋值给将要调用的变量
# 创建列表
ceshi = ['a', 'ab']

##@pytest.mark.parametrize(参数名，[参数值1，参数值2])
@pytest.mark.parametrize("x", ceshi)
def test_five(x):
    assert 'a' in x

# 仅调用一个参数时可不用中括号
# @pytest.mark.parametrize("a",[1,2,3])
@pytest.mark.parametrize("a",[(1),(2),(3)])
def test_aa(a):
    assert a <= 2