import aiohttp
import asyncio
import requests

__all__ = ["tdk"]

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
