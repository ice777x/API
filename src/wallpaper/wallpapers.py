import requests
from bs4 import BeautifulSoup


def get_wallpaper(query: str) -> list:
    r = requests.get("https://hdqwalls.com/search?q=" + query)
    soup = BeautifulSoup(r.content, "html.parser")
    resim_dict = []
    for i in soup.select("img.wallpaper"):
        resim_dict.append({"url": i["src"], "title": i["alt"]})
    if soup.select("a#next"):
        re = requests.get("https://hdqwalls.com" + soup.select("a#next")[0].get("href"))
        soup2 = BeautifulSoup(re.content, "html.parser")
        for i in soup2.select("img.thumbnail"):
            resim_dict.append({"url": i["src"], "title": i["alt"]})
    return resim_dict
