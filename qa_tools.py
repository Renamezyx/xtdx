import time

from openAI.ai_tools import AITools
from tools.qa_data_tools import QaDataTools


class QATools(object):
    qa_data_tools = QaDataTools()
    ai_tools = AITools()

    @staticmethod
    def qa_type_1(questions: list, ai_switch=False):
        a_list = []
        for q in questions:
            q_id = q["ID"]
            q_type = q["QuestionType_ID"]
            q_q = q["Title"]
            q_o = q["Body"]
            curr_a = {"ID": q_id, "MyAnswer": "", "Judge": 0, "QuestionType_ID": q_type, "FileJson": ""}
            # 数据库查找
            a = QATools.qa_data_tools.query_qa(q_id, q_q, q_type)
            if a:
                if isinstance(a, list):
                    a = a[0]
                curr_a["MyAnswer"] = a["a"]
            elif ai_switch:
                curr_a["MyAnswer"] = QATools.ai_tools.ai_qa(q_q, q_o)
                time.sleep(60)
            a_list.append(curr_a)
        return a_list

    @staticmethod
    def qa_update(questions: list):
        for q in questions:
            q_id = q["ID"]
            q_type = q["QuestionType_ID"]
            q_q = q["Title"]
            q_o = q["Body"]
            q_a = q["Answer"]
            QATools.qa_data_tools.update_record(q_id, q_q, q_o, q_a, q_type)
