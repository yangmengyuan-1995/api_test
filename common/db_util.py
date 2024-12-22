"""
@Date  :  2024/12/18 6:11
@File  :  db_util.py
@Author:  杨梦远
"""
import pymysql

from setting import DB_CONF


class DBUtil:
    """
    数据库工具类
    """
    @staticmethod
    def conn_database():
        return pymysql.connect(**DB_CONF)

    def get_one(self, sql):
        conn = self.conn_database()
        cs = conn.cursor()
        cs.execute(sql)
        value = cs.fetchone()
        cs.close()
        conn.close()
        try:
            return value[0]
        except (IndexError, TypeError):
            return None

    # def get_all(self, sql):
    #     conn = self.conn_database()
    #     cs = conn.cursor()
    #     cs.execute(sql)
    #     data_list = cs.fetchall()
    #     cs.close()
    #     conn.close()
    #     return data_list
