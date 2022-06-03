import requests
from bs4 import BeautifulSoup
import aiohttp
import asyncio


class Instagramify:
    def __init__(self, name) -> None:
        self.base = "https://gramhir.com/"
        self.search_url = self.base + "search/"
        self.name = name
        self.profile_url = None
        self.urls = None

    def get_profile_url(self):
        soup = self.make_requests(self.search_url + self.name)
        self.profile_url = (
            soup.select("div.profile-result")[0].select("a")[0].get("href")
        )
        return

    def make_requests(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        return soup

    def profile_photos(self) -> list:
        self.get_profile_url()
        soup = self.make_requests(self.profile_url) if self.profile_url else None
        if not soup:
            return "No profile found"
        a = soup.select("div.box-photo")
        self.urls = [i.select("a")[0].get("href") for i in a]
        descriptions = [i.select("div.photo-description")[0].text for i in a]
        return descriptions

    async def get_page(self, session, url):
        async with session.get(url) as response:
            return await response.text()

    async def print_response(self, session, url):
        html = await self.get_page(session, url)
        soup = BeautifulSoup(html, "html.parser")

        if soup.select("div.single-photo"):
            if soup.select("div.single-photo")[0].select("img"):
                return soup.select("div.single-photo")[0].select("img")[0].get("src")
            else:
                return soup.select("div.single-photo")[0].select("source")[0].get("src")
        elif soup.select("owl-item"):
            return [
                i.select("source")[0].get("src")
                if i.select("video")
                else i.select("img")[0].get("src")
                for i in soup.select("owl-item")
            ]
        else:
            return None

    async def main(self):
        if self.urls == None:
            return self.urls
        async with aiohttp.ClientSession() as session:
            tasks = [
                asyncio.ensure_future(self.print_response(session, url))
                for url in self.urls
            ]
            return await asyncio.gather(*tasks)

    async def instagramify(self) -> None | list:
        descriptions = self.profile_photos()
        result = await self.main()
        if result != None:
            return [i for i in zip(descriptions, result)]
        else:
            return None
