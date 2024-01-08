from openAI.open_ai import OpenAI


class AITools(OpenAI):
    def __init__(self):
        super().__init__()

    def ai_qa(self, q: str, aes: str) -> str:
        content = "请在以下选项中选出一个最合适的答案（只要一个）,告诉我编号即可（只要编号ABCDEF...！）\n{0}\n{1}".format(q, aes)
        ai_res = self.chat(content)
        a = ""
        if ai_res.status_code == 200:
            ai_a = ai_res.json()["choices"][0]["message"]["content"]
            if len(ai_a) == 1:
                a = ai_a
            elif ai_a[0] in ["A", "B", "C", "D", "E", "F", "G"]:
                a = ai_a[0]
        return a
