import aiohttp
from bs4 import BeautifulSoup


async def get_kur_data():
    async with aiohttp.ClientSession() as client:
        async with client.get("https://kur.doviz.com/") as resp:
            html = await resp.text()
    soup = BeautifulSoup(html, "html.parser")
    kur_data = []
    for i in soup.select("table#currencies > tbody tr"):
        if i.find("a") == None:
            continue
        name = i.find("a").get_text(strip=True)
        alis, satis, oran = (
            x.get_text(strip=True) for x in i.find_all("td", attrs={"class": "text-bold"})
        )
        kur_data.append({"name": name, "alis": alis, "satis": satis, "oran": oran})
    return kur_data
