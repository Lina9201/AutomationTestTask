# -*- coding: utf-8 -*-
# @Time    : 2019/11/3 20:25
# @Author  : zhuxuefei

import pymysql

class MysqlUtil:
    def __init__(self, host, username, password, database, charset="utf8", port=3306):

            # 连接数据库信息
            self.conn = pymysql.connect(
                host = host,
                username = username,
                password = password,
                database = database,
                charset = charset,
                port = port
            )
            # 创建光标对象
            self.cursor = self.conn.cursor()

    # 创建查询、执行方法
    def fetchone(self, sql):
        """
        单个查询
        :param sql:
        :return:
        """
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    def fetchall(self,sql):
        """
        多个查询
        :param sql:
        :return:
        """
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def exec(self, sql):
        """
        执行
        :param sql:
        :return:
        """
        try:
            if self.conn and self.cursor:
                self.cursor.execute(sql)
                self.conn.commit()
        except Exception as ex:
            self.conn.rollback()
            return False
        return True


    #关闭对象
    def __del__(self):
        # 关闭光标对象
        if self.cursor is not None:
            self.cursor.close()
        # 关闭连接对象
        if self.conn is not None:
            self.conn.close()


