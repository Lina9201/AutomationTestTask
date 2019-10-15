import pytest

def func(x):
    return x+1

def test_answer():
    assert  func(3)==5      #添加断言判断func(3)==5是否正确


