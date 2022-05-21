import requests
from bs4 import BeautifulSoup


def get_yandex_photo(query: str) -> list:
    url: str = "https://yandex.com.tr/gorsel/search?p=1&text=" + query
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"

    }
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, "html.parser")
    resim_list = ["https:" + i["src"] for i in soup.select("img.serp-item__thumb")]
    return resim_list