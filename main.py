from fastapi import FastAPI, HTTPException, exceptions
from tdk.tdk import tdk
from wallpaper.wallpapers import get_wallpaper
from yandexpic.yandex import get_yandex_photo
from lyrics.glyrics import get_lyrics
from translater.translator import Translator
from movie.tmdb import get_tmdb_data
from typing import Any
from pydantic import BaseModel


class Translate(BaseModel):
    text: str
    lang: str


app = FastAPI()

api_list = [
    {"lyrics":"/lyrics/","example":"/lyrics/?query=padişah"},
    {"translate":"/translate/","example":["/translate/?query=환영&src=ko&lang=tr","/translate/?query=환영&lang=en"]},
    {"movie":"/movie/","example":"/movie/"},
    {"wallpaper":"/wallpaper/","example":"/wallpaper/?query=spiderman"},
    {"yandex":"/yandex/","example":"/yandex/?query=galatasaray"},
    {"tdk":"/tdk/","example":"/tdk/?query=merak"},
]


def convert_api_response(detail: str,status_code:int, response: Any) -> dict:
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
async def read_item(query: str = None):
    if query == None:
        return convert_api_response("Word not found",404,api_list[5])
    try:
        return tdk(query)
    except:
        raise HTTPException(status_code=404, detail="Word not found")


@app.get("/wallpaper/")
def read_wallpaper(query: str= None):
    if query == None:
        return convert_api_response("Query is required",404,api_list[3])
    try:
        return convert_api_response("Get Wallpaper",200, get_wallpaper(query))
    except Exception as e:
        return {"status_code": 404, "error": str(e)}


@app.get("/yandex/")
def read_yandexpic(query: str = None):
    if query == None:
        return convert_api_response("Query is required",404,api_list[4])
    try:
        return convert_api_response("Get Yandex Pictures", 200,get_yandex_photo(query))
    except Exception as e:
        return {"status_code": 404, "error": str(e)}


@app.get("/lyrics/")
async def read_lyrics(query: str = None):
    if query == None:
        return {"status_code": 231, "error": api_list[0]}
    try:
        return convert_api_response("Get Lyrics", 200,await get_lyrics(query))
    except Exception as e:
        return {"status_code": 404, "error": str(e)}


@app.get("/translate/")
def translate(query: str = None, src: str = "auto", lang: str = "tr"):
    if query == None:
        return convert_api_response("Parameters not found",404,api_list[1])
    translator = Translator()
    result = translator.translate(
        text=query,
        src=src,
        dest=lang,
    )
    try:
        return convert_api_response("Translate",200, result)
    except Exception as e:
        return {"status_code": 404, "error": str(e)}

@app.get("/movie/")
async def movie():
    data = await get_tmdb_data()
    if data == []:
        return convert_api_response("API doesn't work",404,None)
    try:
        requ = convert_api_response("Get Movie", 200,data)
        requ.update({"item_count": len(data)})
        return requ
    except Exception as e:
        return {"status_code": 404, "error": str(e)}