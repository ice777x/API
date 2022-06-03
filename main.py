from fastapi import FastAPI, HTTPException, exceptions
from src.tdk.tdk import tdk, benzer
from src.wallpaper.wallpapers import get_wallpaper
from src.yandexpic.yandex import get_yandex_photo
from src.lyrics.glyrics import get_lyrics
from src.translater.translator import Translator
from src.movie.tmdb import get_tmdb_data
from src.youtube.search_ import search_youtube
from src.instagramify.instagramer import Instagramify
from typing import Any


app = FastAPI()

api_list = {
    "lyrics": {"url": "/lyrics/", "example": "/lyrics/?query=padişah"},
    "translate": {
        "url": "/translate/",
        "example": [
            "/translate/?query=환영&src=ko&lang=tr",
            "/translate/?query=환영&lang=en",
        ],
    },
    "movie": {"url": "/movie/", "example": "/movie/"},
    "wallpaper": {"url": "/wallpaper/", "example": "/wallpaper/?query=spiderman"},
    "yandex": {"url": "/yandex/", "example": "/yandex/?query=galatasaray"},
    "tdk": {"url": "/tdk/", "example": ["/tdk/?query=merak", "/tdk/?oneri=merak"]},
    "youtube": {"url": "/youtube/", "example": "/youtube/?query=machine%20learning"},
    "instagram": {"url": "/instagram/", "example": "/instagram/?query=therock"},
}


def convert_api_response(detail: str, status_code: int, response: Any) -> dict:
    if response == None:
        return {
            "status_code": status_code,
            "detail": detail,
            "github": "https://github.com/ice777x",
        }
    return {
        "status_code": status_code,
        "detail": detail,
        "response": response,
        "github": "https://github.com/ice777x",
    }


@app.get("/")
async def read_root():
    return {
        "detail": "ice777 API v1.0",
        "API_LIST": api_list,
        "github": "https://github.com/ice777x",
    }


@app.get("/tdk/")
async def read_item(query: str = None, oneri: str = None):
    if (oneri == None or oneri == "") and (query == None or query == ""):
        return convert_api_response("Word not found", 404, api_list["tdk"])
    elif oneri == None and query != None:
        return convert_api_response("Words found", 200, tdk(query))
    elif oneri != None and query == None:
        return convert_api_response("Words found", 200, benzer(oneri))
    else:
        return convert_api_response("Parameters not found", 404, api_list["tdk"])


@app.get("/youtube/")
async def youtube(query: str = None):
    print(query)
    if query == None or query == "":
        return convert_api_response(
            "Query parameter is invalid", 404, api_list["youtube"]
        )
    else:
        return convert_api_response(
            "Youtube Search List",
            200,
            await search_youtube(query),
        )


@app.get("/wallpaper/")
def read_wallpaper(query: str = None):
    if query == None:
        return convert_api_response("Query is required", 404, api_list["wallpaper"])
    try:
        return convert_api_response("Get Wallpaper", 200, get_wallpaper(query))
    except Exception as e:
        return {"status_code": 404, "error": str(e)}


@app.get("/yandex/")
def read_yandexpic(query: str = None):
    if query == None:
        return convert_api_response("Query is required", 404, api_list["yandex"])
    try:
        return convert_api_response("Get Yandex Pictures", 200, get_yandex_photo(query))
    except Exception as e:
        return {"status_code": 404, "error": str(e)}


@app.get("/lyrics/")
async def read_lyrics(query: str = None):
    if query == None:
        return {"status_code": 231, "error": api_list["lyrics"]}
    try:
        return convert_api_response("Get Lyrics", 200, await get_lyrics(query))
    except Exception as e:
        return {"status_code": 404, "error": str(e)}


@app.get("/translate/")
def translate(query: str = None, src: str = "auto", lang: str = "tr"):
    if query == None:
        return convert_api_response("Parameters not found", 404, api_list["translate"])
    translator = Translator()
    result = translator.translate(
        text=query,
        src=src,
        dest=lang,
    )
    try:
        return convert_api_response("Translate", 200, result)
    except Exception as e:
        return {"status_code": 404, "error": str(e)}


@app.get("/movie/")
async def movie():
    data = await get_tmdb_data()
    if data == []:
        return convert_api_response("API doesn't work", 404, None)
    try:
        requ = convert_api_response("Get Movie", 200, data)
        requ.update({"item_count": len(data)})
        return requ
    except Exception as e:
        return {"status_code": 404, "error": str(e)}


@app.get("/instagram/")
async def instagram(query: str = None):
    if query == None or query == "":
        return convert_api_response(
            "Query parameter is invalid", 404, api_list["instagram"]
        )
    else:
        result = await Instagramify(query).instagramify()
        if result == None:
            return convert_api_response("API doesn't work", 404, None)
        return convert_api_response("Instagramify", 200, result)
