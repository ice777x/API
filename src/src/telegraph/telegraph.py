import requests
import json

acc_token = "f843b1b0ac9e6f63ce150907c258b9ab41ce156e410a593a512ce9d8e00b"


class Telegraph:
    def __init__(self, text):
        self.text = text
        self.content = None

    def make_content(self):
        dedi = {"tag": "p", "children": [self.text]}
        al = json.dumps(dedi)
        self.content = "[{}]".format(al)

    def get_page(self):
        self.make_content()
        if self.content:
            url = f"https://api.telegra.ph/createPage?access_token={acc_token}&title=Sample+Page&author_name=Anonymous&content={self.content}&return_content=true"
            r = requests.get(url)
            data = r.json()
            return data
        else:
            return None
