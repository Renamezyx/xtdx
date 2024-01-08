import pymysql
from logger_base import logger


class MysqlBase(object):
    def __init__(self, host='175.178.73.5',
                 user='root',
                 password='6f4c219eeb4088d8',
                 database='xtdx_qa',
                 charset='utf8mb4',
                 cursorclass=pymysql.cursors.DictCursor):
        # 建立数据库连接
        self.connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            charset=charset,  # 可选项，指定字符集
            cursorclass=cursorclass  # 可选项，返回字典类型的游标对象
        )

    def __del__(self):
        self.connection.close()

    def select(self, sql_str: str) -> dict:
        # 查询
        logger.info("执行sql: " + sql_str)
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql_str)
            res = cursor.fetchall()
        except Exception as e:
            logger.info(f"Error occurred: {str(e)}")
            res = {}
        finally:
            if cursor:
                cursor.close()
            logger.info("执行结果: {0}".format(res))
            return res

    def update(self, sql_str: str) -> int:
        # 修改
        logger.info("执行sql: " + sql_str)
        try:
            cursor = self.connection.cursor()
            res = cursor.execute(sql_str)
        except Exception as e:
            logger.info(f"Error occurred: {str(e)}")
            res = -1
        finally:
            if cursor:
                cursor.close()
            logger.info("执行结果: {0}".format(res))
            return res

    def delete(self, sql_str: str) -> int:
        # 删除
        logger.info("执行sql: " + sql_str)
        try:
            cursor = self.connection.cursor()
            res = cursor.execute(sql_str)
        except Exception as e:
            logger.info(f"Error occurred: {str(e)}")
            res = -1
        finally:
            if cursor:
                cursor.close()
            logger.info("执行结果: {0}".format(res))
            return res

    def insert(self, sql_str: str, values) -> int:
        # 新增
        logger.info("执行sql: {0}, values: {1}".format(sql_str, values))
        try:
            cursor = self.connection.cursor()
            res = cursor.execute(sql_str, values)
            self.connection.commit()
        except Exception as e:
            logger.info(f"Error occurred: {str(e)}")
            res = -1
        finally:
            if cursor:
                cursor.close()
            logger.info("执行结果: {0}".format(res))
            return res


if __name__ == '__main__':
    mysql_tools = MysqlBase()
    query = "SELECT * FROM qa"
    for i in mysql_tools.select(query):
        print(i)
