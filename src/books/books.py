import requests
from bs4 import BeautifulSoup
import aiohttp
import asyncio


class Libgen:
    def __init__(self, query: str):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
        }
        self.query = query.strip()
        self.url = f"https://libgen.li/index.php?req={self.query}&columns%5B%5D=t&columns%5B%5D=a&columns%5B%5D=s&columns%5B%5D=y&columns%5B%5D=p&columns%5B%5D=i&objects%5B%5D=f&objects%5B%5D=e&objects%5B%5D=s&objects%5B%5D=a&objects%5B%5D=p&objects%5B%5D=w&topics%5B%5D=l&topics%5B%5D=c&topics%5B%5D=f&topics%5B%5D=a&topics%5B%5D=m&topics%5B%5D=r&topics%5B%5D=s&res=100&filesuns=all&curtab=f&order=&ordermode=desc&filesuns=all&page="
        self.base = "https://libgen.li"
        self.rocks = "https://libgen.rocks/"
        self.urls = []
        self.data = []
        self.data_url: list = []
        self.count = 0

    async def print_data(self, session, url):
        html = await self.get_page(session, url)
        soup = BeautifulSoup(html, "html.parser")
        if soup.select("table.table"):
            for i in soup.select("table.table tbody tr"):
                url = i.select("td")[-1].find("a").get("href")
                self.data_url.append(url)
                try:
                    self.data.append(
                        {
                            "title": i.select("td a")[0].text,
                            "author": i.select("td")[1].text,
                            "year": i.select("td")[3].text,
                            "language": i.select("td")[4].text,
                            "url": url,
                        }
                    )
                except Exception as e:
                    continue

    async def get_urls(self) -> None:
        urls = [self.url + str(i) for i in range(2, 3)]
        async with aiohttp.ClientSession() as session:
            tasks = [asyncio.create_task(self.print_data(session, url)) for url in urls]
            await asyncio.gather(*tasks)

    async def get_page(self, session, url):
        async with session.get(url) as response:
            return await response.text()

    async def print_response(self, session, url):
        html = await self.get_page(session, url)
        soup = BeautifulSoup(html, "html.parser")
        down_url = self.rocks + soup.select("td a")[0].get("href")
        self.data[self.count]["download"] = down_url
        self.count += 1

    async def get_books(self):
        await self.get_urls()
        async with aiohttp.ClientSession(headers=self.headers) as session:
            tasks = [
                asyncio.create_task(self.print_response(session, url)) for url in self.data_url
            ]
            await asyncio.gather(*tasks, return_exceptions=True)
        return self.data
