import json

from data import get_data


class JsonFileHandler:
    def __init__(self, filename):
        self.filename = filename

    def read_json(self):
        try:
            with open(self.filename, 'r') as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            print(f"文件 '{self.filename}' 不存在.")
            return None
        except json.JSONDecodeError:
            print(f"文件 '{self.filename}' 不是有效的JSON格式.")
            return None

    def write_json(self, data):
        with open(self.filename, 'w') as file:
            json.dump(data, file, indent=4)
            print(f"已将数据写入文件 '{self.filename}'.")

    def update_json(self, update_dict):
        current_data = self.read_json()
        if current_data:
            current_data.update(update_dict)
            self.write_json(current_data)


class DataTools(object):
    # 获取下一个url
    def __init__(self, file):
        self.json_file_handler = JsonFileHandler(file)

    def get_next_data(self):
        data = self.json_file_handler.read_json()["data"]
        for i in data:
            if i["IsLook"] < i["Duration"]:
                return {
                    "uri": "{0}-{1}-{2}-{3}".format(i["ID"], i["Course_ID"], i["CourseWare_ID"], i["Curriculum_ID"]),
                    "data": i}

    # 更新状态
    def update_data(self):
        get_data()


if __name__ == '__main__':
    print(DataTools("./data.json").get_next_data())
