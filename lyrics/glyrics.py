import requests
import re
import json
import aiohttp
import asyncio

dataDict: list = []


def scrape_lyrics(response):
    text_html = response.split("window.__PRELOADED_STATE__ = JSON.parse('")[1].split(
        "');"
    )[0]
    yeni = (
        text_html.replace('\\"', '"')
        .replace("\\\\n", "\\n")
        .replace('\\"', '"')
        .replace("\\'", "'")
    )
    data = json.loads(yeni)
    text = data["songPage"]["lyricsData"]["body"]["html"]
    lyrics_text = re.sub("<[^<]+?>", "", str(text))
    return lyrics_text


def querySong(query: str):
    global dataDict
    url = "https://genius.com/api/search/song?page=1&q=" + query
    r = requests.get(url)
    data: dict = r.json().get("response").get("sections")
    songs = [i for i in data if i.get("type") == "song"][0].get("hits")
    for i, v in enumerate(songs):
        result = v["result"]
        image = result["song_art_image_url"]
        url = result["url"]
        song = f"{result['artist_names']} - {result['title']}"
        artist = result["primary_artist"]
        artist_name = artist["name"]
        artist_image = artist["image_url"]
        artist_url = artist["url"]
        dataDict.append(
            {
                "title": song,
                "artist": artist,
                "url": url,
                "image": image,
                "artist": {
                    "artist_name": artist_name,
                    "artist_image": artist_image,
                    "artist_url": artist_url,
                },
            }
        )
    return dataDict


async def get_page(session, url):
    async with session.get(url) as response:
        return await response.text()


async def print_page(session, url, i):
    global dataDict
    page = await get_page(session, url)
    # dataDict[str(i + 1)] = _get_api(page)
    dataDict[i]["lyrics"] = scrape_lyrics(page)


async def get_lyrics(query: str):
    global dataDict
    data2 = querySong(query)
    async with aiohttp.ClientSession() as session:
        task = (
            asyncio.ensure_future(print_page(session, v["url"], i))
            for i, v in enumerate(data2)
        )
        data = await asyncio.gather(*task)
    return dataDict
