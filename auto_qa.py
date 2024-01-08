# 自动答题
import json
import random
import time

from requests import Response

from logger_base import logger
from qa_tools import QATools
from tools.request_base import request
from config import headers

urls = {
    "GetStuSpecialtyCurriculumList": "https://xtdx.web2.superchutou.com/service/eduSuper/Specialty/GetStuSpecialtyCurriculumList",
    "GetExamPaperQuestions": "https://xtdx.web2.superchutou.com/service/eduSuper/Question/GetExamPaperQuestions",
    "GetStuStagePaperList": "https://xtdx.web2.superchutou.com/service/eduSuper/Question/GetStuStagePaperList",
    "SubmitExamPractice": "https://xtdx.web2.superchutou.com/service/eduSuper/Question/SubmitExamPractice",
    "GetExamPaperResult": "https://xtdx.web2.superchutou.com/service/eduSuper/Question/GetExamPaperResult",
    "GetStuCourseByID": "https://xtdx.web2.superchutou.com/service/eduSuper/Question/GetStuCourseByID?StuID=60B01EDBFFDE421FB3DDC379FEF7914F&Vaild=1",
    "CheckVerify": "https://xtdx.web2.superchutou.com/service/eduSuper/Common/CheckVerify?OnlyKey=0&_notMessage=true",
    "SubmitSimplePractice": "https://xtdx.web2.superchutou.com/service/eduSuper/Question/SubmitSimplePractice"
}


def CheckVerify() -> None:
    request(method="get", url=urls["CheckVerify"], headers=headers)


def GetStuSpecialtyCurriculumList(StuDetail_ID: str, StuID: str, IsStudyYear: int = 1) -> Response:
    """
    获取课程列表
    :param StuDetail_ID:
    :param StuID:
    :param IsStudyYear:
    :return:
    """
    params = {
        "StuDetail_ID": StuDetail_ID,
        "StuID": StuID,
        "IsStudyYear": IsStudyYear
    }
    return request(method="get", params=params, headers=headers, url=urls["GetStuSpecialtyCurriculumList"])


def GetExamPaperQuestions(examPaperId: int, StuID: str, StuDetail_ID: str, Examination_ID: int,
                          Curriculum_ID: int, IsBegin: int = None, type: int = None) -> Response:
    """
    获取试卷 Questions
    :param examPaperId:
    :param IsBegin:
    :param StuID:
    :param StuDetail_ID:
    :param Examination_ID:
    :param Curriculum_ID:
    :return:
    """
    params = {
        "examPaperId": examPaperId,
        "StuID": StuID,
        "StuDetail_ID": StuDetail_ID,
        "Examination_ID": Examination_ID,
        "Curriculum_ID": Curriculum_ID
    }
    if IsBegin is None:
        params["IsBegin"] = 1
    if type is None:
        params["type"] = 1

    return request(method="get", url=urls["GetExamPaperQuestions"], headers=headers, params=params)


def SubmitExamPractice(Curriculum_ID: int, EndTime: int, Examination_ID: str, StuDetail_ID: str, StuID: str,
                       list: list, resultId: int) -> Response:
    """
    提交试卷
    :param Curriculum_ID:
    :param EndTime:
    :param Examination_ID:
    :param StuDetail_ID:
    :param StuID:
    :param list:
    :param resultId:
    :return:
    """
    data = {
        "Curriculum_ID": Curriculum_ID,
        "EndTime": EndTime,
        "Examination_ID": Examination_ID,
        "StuDetail_ID": StuDetail_ID,
        "StuID": StuID,
        "list": list,
        "resultId": resultId
    }
    return request(method="post", url=urls["SubmitExamPractice"], headers=headers, json=data)


def GetExamPaperResult(busId: int, resultId: int) -> Response:
    """
    获取试卷解析
    :param busId:
    :param resultId:
    :return:
    """
    params = {
        "busId": busId,
        "resultId": resultId
    }
    return request(method="get", url=urls["GetExamPaperResult"], params=params, headers=headers)


def GetStuStagePaperList(StuID: str, Curriculum_ID: int, ExamPaperType: int = 3) -> Response:
    """
    获取试卷列表
    :param StuID:
    :param ExamPaperType:
    :param Curriculum_ID:
    :return:
    """
    params = {
        "StuID": StuID,
        "ExamPaperType": ExamPaperType,
        "Curriculum_ID": Curriculum_ID
    }
    return request(method="get", url=urls["GetStuStagePaperList"], params=params, headers=headers)


def SubmitSimplePractice(resultId: int, list: list, StuDetail_ID: str, StuID: str, Examination_ID: str) -> Response:
    """
    提交单个题目答案
    :param resultId:
    :param list:
    :param StuDetail_ID:
    :param StuID:
    :param Examination_ID:
    :return:
    """
    data = {
        "resultId": resultId,
        "list": list,
        "StuDetail_ID": StuDetail_ID,
        "StuID": StuID,
        "Examination_ID": Examination_ID
    }
    return request(method="post", url=urls["SubmitSimplePractice"], headers=headers, json=data)


if __name__ == '__main__':
    StuDetail_ID = "84F62DF86EC9462AB3478F353910C0FA"
    StuID = "60B01EDBFFDE421FB3DDC379FEF7914F"
    Curriculum_IDs = [i["Curriculum_ID"] for i in
                      GetStuSpecialtyCurriculumList(StuDetail_ID, StuID).json()["Data"]["list"]]
    for Curriculum_ID in Curriculum_IDs:
        StagePaperList = GetStuStagePaperList(StuID, Curriculum_ID).json()["Data"]
        if StagePaperList:
            for StagePaper in StagePaperList:
                if (StagePaper["EvaluationCount"] > 1 or StagePaper["EvaluationCount"] == 0) and (
                        StagePaper["ExamScore"] is None or StagePaper["ExamScore"] < 60):
                    GetExamPaperQuestions(StagePaper["ExamPaper_ID"], StuID, StuDetail_ID, 0,
                                          StagePaper["Curriculum_ID"], type=1)
                    CheckVerify()
                    PaperQuestions = GetExamPaperQuestions(StagePaper["ExamPaper_ID"], StuID, StuDetail_ID, 0,
                                                           StagePaper["Curriculum_ID"], IsBegin=1).json()["Data"]
                    question = PaperQuestions["QuestionType"][0]["Question"]
                    a_list = QATools.qa_type_1(question, ai_switch=True)
                    logger.info(r"[本次试卷提交答案]：{0}".format(a_list))
                    # 提交单个题目的答案
                    for a in a_list:
                        SubmitSimplePractice(PaperQuestions["ResultId"], [a], StuDetail_ID, StuID, "0")
                    SubmitExamPractice(Curriculum_ID, 7200, 0, StuDetail_ID, StuID, a_list,
                                       PaperQuestions["ResultId"])
                    Result = GetExamPaperResult(PaperQuestions["PaperInfo"]["ID"], PaperQuestions["ResultId"]).json()[
                        "Data"]
                    QATools.qa_update(Result["QuestionType"][0]["Question"])
