from tools.mysql_base import MysqlBase
from logger_base import logger


class QaDataTools(MysqlBase):
    def __init__(self):
        super().__init__()

    def update_record(self, q_id, q, o, a, type):
        if len(self.query_qa(q_id, q, type)) == 0:
            logger.info("执行添加记录")
            sql_str = "INSERT INTO qa(q_id,q,o,a,type) VALUES (%s,%s,%s,%s,%s)"
            values = (q_id, q, o, a, type)
            res = self.insert(sql_str, values)
            return res
        logger.info("将要添加的记录已存在")
        return 1

    def query_qa(self, q_id, q, type):
        sql0_str = 'SELECT * FROM qa WHERE q_id = {0}'.format(q_id)
        res = self.select(sql0_str)
        # if len(res) != 0:
        #     return res
        # sql_str = 'SELECT * FROM qa WHERE q = "{0}" and type = {1}'.format(q, type)
        # res = self.select(sql_str)
        return res



