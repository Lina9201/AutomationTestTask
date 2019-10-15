import pytest

def f(a,b):
    sum = a + b
    raise SystemExit(sum == 3)

def test_mytest():
    assert f(1,2) ==4
    with pytest.raises(SystemExit):
        f(2,2)