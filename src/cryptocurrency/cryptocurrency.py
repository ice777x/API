import requests
from bs4 import BeautifulSoup
import aiohttp
import asyncio


class CoinGecko:
    def __init__(self):
        self.base = "https://www.coingecko.com"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
        }
        self.urls = [self.base + "/?page=" + str(i) for i in range(1, 2)]
        self.data = []

    async def get_page(self, session, url):
        async with session.get(url) as response:
            return await response.text()

    async def print_response(self, session, url):
        html = await self.get_page(session, url)
        soup = BeautifulSoup(html, "html.parser")
        tables = soup.select("div.coin-table")[0].select("tbody")[0].select("tr")
        for i in tables:
            name, link = i.select("a")[0].text.strip("\n"), self.base + i.select("a")[
                0
            ].get("href")
            dict = {"name": name, "link": link}
            col_ = ["coin", "Price", "1h", "24h", "7d", "24h_Volume", "Marketcap"]
            for index, v in enumerate(i.select("span")):
                dict[col_[index]] = v.text.strip("\n")
            dict["chart"] = i.select("td")[-1].select("img")[0].get("src")
            self.data.append(dict)

    async def parse(self):
        async with aiohttp.ClientSession(headers=self.headers) as session:
            tasks = [
                asyncio.create_task(self.print_response(session, url))
                for url in self.urls
            ]
            await asyncio.gather(*tasks)
        return self.data
