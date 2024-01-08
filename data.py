import json

from logger_base import logger
from config import headers
from tools.request_base import request

urls = {
    "GetStuSpecialtyCurriculumList": "https://xtdx.web2.superchutou.com/service/eduSuper/Specialty/GetStuSpecialtyCurriculumList",
    "GetCourse_ChaptersNodeList": "https://xtdx.web2.superchutou.com/service/eduSuper/Question/GetCourse_ChaptersNodeList"
}

StuDetail_ID = "84F62DF86EC9462AB3478F353910C0FA"
StuID = "60B01EDBFFDE421FB3DDC379FEF7914F"


def GetStuSpecialtyCurriculumList(StuDetail_ID, IsStudyYear, StuID, result=None):
    params = {
        "StuDetail_ID": StuDetail_ID,
        "IsStudyYear": IsStudyYear,
        "StuID": StuID
    }
    res = request("get", urls["GetStuSpecialtyCurriculumList"], params=params, headers=headers)
    if res.status_code == 200:
        result = res.json()
    return result


def GetCourse_ChaptersNodeList(Valid, Course_ID, StuID, Curriculum_ID, Examination_ID, StuDetail_ID, result=None):
    params = {
        "Valid": Valid,
        "Course_ID": Course_ID,
        "StuID": StuID,
        "Curriculum_ID": Curriculum_ID,
        "Examination_ID": Examination_ID,
        "StuDetail_ID": StuDetail_ID,
    }
    res = request("get", urls["GetCourse_ChaptersNodeList"], params=params, headers=headers)

    if res.status_code == 200:
        result = res.json()
    return result


def get_data():
    data = []
    _ = GetStuSpecialtyCurriculumList(StuDetail_ID, 1, StuID)
    if _ is not None:
        courses_info = _["Data"]["list"]

        for course in courses_info:
            if course["Course_ID"] != 0:
                _ = GetCourse_ChaptersNodeList(1, course["Course_ID"], StuID, course["Curriculum_ID"],
                                               course["Examination_ID"],
                                               StuDetail_ID)
                if _ is not None:
                    course_data = [item for sublist in _["Data"] for item in sublist["ChildNodeList"]]

                    _data = [{
                        "ID": i["ID"],
                        "Name": i["Name"],
                        "Course_ID": i["Course_ID"],
                        "CourseWare_ID": i["CourseWare_ID"],
                        "Curriculum_ID": course["Curriculum_ID"],
                        "TotalSecond": i["TotalSecond"],
                        "PolyvVID": i["PolyvVID"],
                        "Duration": i["Duration"],
                        "LookTime": i["LookTime"],
                        "IsLook": i["IsLook"]
                    } for i in course_data]
                    data = data + _data

    logger.info("总时长：{0}".format(sum([item["Duration"] for item in data])))
    logger.info("已观看有效时长：{0}".format(sum([item["TotalSecond"] for item in data])))
    with open('data.json', 'w', encoding="utf-8") as file:
        data_dict = {"data": data}
        logger.info("更新data.json 数据, len:{0}".format(len(data_dict["data"])))
        file.write(json.dumps(data_dict))


if __name__ == '__main__':
    get_data()
