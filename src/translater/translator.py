import requests


class Translator:
    def __init__(
        self,
    ) -> dict:
        pass

    def __repr__(self) -> str:
        return """
Use this:
>>> translator = Translator()
>>> translator.translate(text="Hello, World!", src="en", dest="ko") 
>>> Good Morning --> 안녕하세요."""

    def translate(self, text: str, src="auto", dest=""):
        """<translator.translate(text="Hello, World!",src="en",dest="ko")>

        Result:
        {'result': 'success', 'original_text': 'Good Morning.', 'lang': 'en', 'translated_text': '안녕하세요.', 'translated_lang': 'ko', 'word': 2}

        Good Morning --> 안녕하세요.
        """
        session = requests.Session()
        data1 = {
            "detect_new_text": 0,
            "rtk_priv": "none",
            "rtk_p": "%7B%7D",
            "_gat_gtag_UA_3411294_31": 1,
            "text_to_translate": text,
        }
        if src == "auto":
            auto_detect = session.post(
                "https://www.translate.com/translator/ajax_lang_auto_detect", data=data1
            ).json()
            lang = auto_detect["language"]
        else:
            lang = src

        if dest == "":
            dest = "en"

        url = "https://www.translate.com/translator/ajax_translate"
        cevir_req = session.post(
            url,
            data={
                "text_to_translate": text,
                "source_lang": lang,
                "translated_lang": dest,
            },
        )
        translated_lang = dest
        translate_result = cevir_req.json()
        result = {}
        # if translate_result["result"] == "success":
        try:
            result["status_code"] = 200
            result["result"] = "success"
            result["original_text"] = text
            result["lang"] = lang
            result["translated_text"] = translate_result["translated_text"]
            result["translated_lang"] = translated_lang
            result["word"] = len(result["original_text"].split())
        # elif translate_result["result"] == "error":
        except Exception as e:
            result["error"] = e
            result["status_code"] = 404
        return result
