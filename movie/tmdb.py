import aiohttp
import asyncio
from dotenv import load_dotenv
import os

load_dotenv("./config.env")
API_KEY = str(os.environ.get("API_KEY"))


async def get_page(session, url):
    async with session.get(url) as response:
        return await response.json()


def write_dict(movie_result: dict):
    adult = movie_result["adult"]
    original_title = movie_result["original_title"]
    release_date = (
        movie_result["release_date"] if "release_date" in movie_result.keys() else "N/A"
    )
    overview = movie_result["overview"]
    popularity = movie_result["popularity"]
    language = movie_result["original_language"]
    if movie_result["poster_path"] == None:
        poster_path = "N/A"
    else:
        poster_path = "https://image.tmdb.org/t/p/w500" + movie_result["poster_path"]
    return {
        "adult": adult,
        "title": original_title,
        "release_date": release_date,
        "overview": overview,
        "poster_path": poster_path,
        "language": language,
        "popularity": popularity,
    }


new_res = []


async def print_response(session, url):
    new_res.clear()
    data = await get_page(session, url)
    if "results" in data.keys():
        new_res.extend([write_dict(i) for i in data["results"]])


async def get_tmdb_data():
    url_link = f"https://api.themoviedb.org/3/discover/movie?api_key={API_KEY}&sort_by=popularity.desc&include_adult=false&include_video=false&page="
    urls = [url_link + str(i) for i in range(1, 10)]
    async with aiohttp.ClientSession() as session:
        task = [asyncio.ensure_future(print_response(session, url)) for url in urls]
        await asyncio.gather(*task)
    return new_res
