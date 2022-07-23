import requests
import os
from json import load, dump

__all__ = ["tdk", "benzer"]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
}


def anlamBilgisi(tdata: list) -> dict:
    if isinstance(tdata, list):
        data = tdata[0]

    anlamlar = []
    for i in data["anlamlarListe"]:
        ornekler = []
        if "orneklerListe" in i.keys():
            for x in i.get("orneklerListe"):
                ornekler.append(x["ornek"])
        anlamlar.append({"anlam": i["anlam"], "ornekler": ornekler})
    ozelmi = True if data["ozel_mi"] == 1 else False
    cogulmu = True if data["cogul_mu"] == 1 else False
    return {
        "kelime": data["madde"],
        "anlamlar": anlamlar,
        "ozel": ozelmi,
        "cogul": cogulmu,
    }


def tdk(kelime: str):
    url = "https://sozluk.gov.tr/gts?ara=" + kelime.strip()
    r = requests.get(url, headers=headers)
    data = r.json()
    return anlamBilgisi(data)


def benzer(kelime: str = None) -> list:
    def kelimeToJson():
        if not os.path.exists("src/tdk/kelimeler.json"):
            url = "https://sozluk.gov.tr/autocomplete.json"
            r = requests.get(url, headers=headers)
            kelimeler = list((i["madde"] for i in r.json()))
            with open("src/tdk/kelimeler.json", "w", encoding="utf-8") as file:
                dump(kelimeler, file, ensure_ascii=False, indent=2)
            return kelimeler

        else:
            with open("src/tdk/kelimeler.json", "r", encoding="utf-8") as file:
                kelimeler = load(file)
            return kelimeler

    def basHarf(kelime: str) -> list:
        kelimeler = kelimeToJson()
        basHarfList = []
        for i in kelimeler:
            if i.startswith(kelime[0]):
                basHarfList.append(i)
        return basHarfList

    def benzer_ara(kelime: str = None) -> list:
        if kelime == "" or kelime is None:
            return []
        benzer_kelime = []
        basHarfList = basHarf(kelime)
        for i in basHarfList:
            if kelime in i[: len(kelime)]:
                if len(benzer_kelime) < 10:
                    benzer_kelime.append(i)
        return sorted(benzer_kelime, key=len)

    return benzer_ara(kelime)
