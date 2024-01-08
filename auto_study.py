import random
import time
from data_tools import DataTools
from collections import namedtuple
from config import headers
from tools.request_base import request

URLS = namedtuple('url_tuple', ['name', 'url'])
urls = {
    "SaveCourse_Look": "https://xtdx.web2.superchutou.com/service/datastore/WebCourse/SaveCourse_Look",
    "GetCourse_ChaptersNodeList": "https://xtdx.web2.superchutou.com/service/datastore/WebCourse/GetCourse_ChaptersNodeList",
    "GetStuSpecialtyCurriculumList": "https://xtdx.web2.superchutou.com/service/eduSuper/Specialty/GetStuSpecialtyCurriculumList",
    "qos": "https://prtas.videocc.net/qos",
    "Specialty_GetStuSpecialtyCurriculumList": "https://xtdx.web2.superchutou.com/service/eduSuper/Specialty/GetStuSpecialtyCurriculumList",
    "Question_GetCourse_ChaptersNodeList": "https://xtdx.web2.superchutou.com/service/eduSuper/Question/GetCourse_ChaptersNodeList"
}


def SaveCourse_Look(LookType, CourseChapters_ID):
    body = {"CourseChapters_ID": CourseChapters_ID, "LookType": LookType, "LookTime": 60, "IP": "127.0.0.1"}
    res = request("post", url=urls["SaveCourse_Look"], headers=headers, json=body)
    return res


def qos(vid, href=""):
    pid = str(int(time.time())) + "X" + str(int(random.random() * 1e6 + 1e6))
    params = {
        "pid": pid,
        "vid": vid,
        "uid": "26a8e2a07f",
        "href": href,
        "domain": "dpv.videocc.net",
        "type": "end",
        "pn": "HTML5",
        "pv": "v1.36.0"
    }
    res = request("get", url=urls["qos"], headers=headers, params=params)

    return res


data_tools = DataTools("./data.json")

while True:
    data_tools.update_data()
    curr_data = data_tools.get_next_data()
    for _ in range(int(curr_data["data"]["Duration"] / 10) + 1):
        time.sleep(3)
        SaveCourse_Look_res = SaveCourse_Look(LookType=0, CourseChapters_ID=curr_data["data"]["ID"])
