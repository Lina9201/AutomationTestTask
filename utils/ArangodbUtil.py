# -*- coding: utf-8 -*-
# @Time    : 2020/1/7 9:40
# @Author  : zhuxuefei

from pyArango.connection import *

class ArangodbUtil:
    def __init__(self, arangoURL, username, password):
        # 连接Arangodb数据库信息
        self.conn = Connection(
            arangoURL = arangoURL,
            username = username,
            password = password
        )

    def opendb(self, database):
        """
        打开Arangodb数据库
        :param database:
        :return:
        """
        self.db = self.conn[database]
        return self.db

if __name__=="__main__":
    db1 = ArangodbUtil("http://172.23.1.2:8529", "root", "root1234")
    dbname = db1.opendb("cmdb")
    print(dbname)
    categoryName = "category_auto"
    categorykey = dbname.AQLQuery("FOR c IN category FILTER c.name=='%s' RETURN c._key" % categoryName)
    queryResult = dbname.AQLQuery("FOR c IN category RETURN c")
    for key in queryResult:
        if key.name == categoryName:
            print(key._key)
            print(type(key._key))
    print(categorykey)


