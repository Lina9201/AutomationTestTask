from excelHandle.excelHandle import excelHandle
import pytest

param=excelHandle("excels/test.xlsx","Sheet2")
@pytest.mark.parametrize("id,name",param)
def test_excel(id,name):
    assert id==1
    assert name=="a"

if __name__ == '__main__':
    pytest.main(['--junit-xml=test.xml', 'test_excel.py'])