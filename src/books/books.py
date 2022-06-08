import requests
from bs4 import BeautifulSoup
import os
import asyncio
import aiohttp


class Libgen:
    def __init__(self, query):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
        }
        self.query = query
        self.url = f"https://libgen.is/search.php?req={query}&lg_topic=libgen&open=0&view=detailed&res=100&phrase=1&column=def"
        self.base = "https://libgen.is"
        self.urls = []
        self.data = []
        self.count = 0

    def get_urls(self):
        r = requests.get(self.url)
        soup = BeautifulSoup(r.content, "html.parser")

        for i in soup.find_all("table", attrs={"rules": "cols"}):
            try:
                title = i.select("tr")[1].select("td")[2].text
                author = i.select("tr")[2].select("td")[-1].text
                urls = self.base + i.select("tr")[1].find("a").get("href")
                dicte = {"title": title, "author": author, "url": urls}
                self.data.append(dicte)
                self.urls.append(self.base + i.select("tr")[1].find("a").get("href"))
            except:
                pass

    async def get_page(self, session, url):
        async with session.get(url) as response:
            return await response.text()

    async def print_response(self, session, url):
        html = await self.get_page(session, url)
        soup = BeautifulSoup(html, "html.parser")
        if soup.select("div#download"):
            for x in range(3):
                try:
                    down_link = (
                        soup.select("div#download")[0].select("a")[x].get("href")
                    )
                except:
                    pass
        else:
            down_link = None
        self.data[self.count]["download"] = down_link
        self.count += 1
        return

    async def get_books(self):
        self.get_urls()
        async with aiohttp.ClientSession(headers=self.headers) as session:
            tasks = [
                asyncio.create_task(self.print_response(session, url))
                for url in self.urls
            ]
            await asyncio.gather(*tasks)
        return self.data
