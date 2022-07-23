from bs4 import BeautifulSoup
import asyncio
import aiohttp

url = "https://www.discudemy.com/language/Turkish"


class DiscUdemy:
    def __init__(self, q):
        self.data = []
        self.tokenlist = []
        if q == None:
            self.links = [
                "https://www.discudemy.com/all/" + str(i) for i in range(1, 4)
            ]
        else:
            self.links = [
                "https://www.discudemy.com/category/" + q + "/" + str(i)
                for i in range(1, 4)
            ]

    async def get_page(self, session, url):
        async with session.get(url) as response:
            return await response.text()

    async def print_response(self, session, url):
        html = await self.get_page(session, url)
        soup = BeautifulSoup(html, "html.parser")
        if soup.select("a#couponLink"):
            self.data.append(soup.select("a#couponLink")[0].get("href"))
        else:
            self.tokenlist.extend(
                [
                    "https://www.discudemy.com/go/" + i.get("href").split("/")[-1]
                    for i in soup.select("a.card-header")
                ]
            )
        return

    async def get_discudemy(self):
        async with aiohttp.ClientSession() as session:
            tasks = [
                asyncio.ensure_future(self.print_response(session, url))
                for url in self.links
            ]
            await asyncio.gather(*tasks)
            task2 = [
                asyncio.ensure_future(self.print_response(session, url))
                for url in self.tokenlist
            ]
            await asyncio.gather(*task2)
        return self.data

    async def category_list(self):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://www.discudemy.com/category") as response:
                html = await response.text()
                soup = BeautifulSoup(html, "html.parser")
                return [
                    "/discudemy/?query=" + i.get("href").split("/")[-1]
                    for i in soup.select("a.ui")
                ]
