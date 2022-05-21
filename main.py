from fastapi import FastAPI, HTTPException, exceptions
from tdk.tdk import tdk
from wallpaper.wallpapers import get_wallpaper
from yandexpic.yandex import get_yandex_photo
from lyrics.glyrics import get_lyrics
from translater.translator import Translator
from movie.tmdb import get_tmdb_data
from typing import Any
import uvicorn


app = FastAPI()


def convert_api_response(detail: str, response: Any) -> dict:
    return {
        "detail": detail,
        "response": response,
        "github": "https://github.com/ice777x",
    }


@app.get("/")
async def read_root():
    return {
        "detail": "Open-API",
        "API_LIST": [{"lyrics": "/lyrics/"}],
        "github": "https://github.com/ice777x",
    }


@app.get("/tdk/")
async def read_item(query: str):
    if query == "":
        raise HTTPException(status_code=400, detail="Query is empty")
    try:
        return tdk(query)
    except:
        raise HTTPException(status_code=404, detail="Word not found")


@app.get("/wallpaper/")
def read_wallpaper(query: str):
    try:
        return convert_api_response("Get Wallpaper", get_wallpaper(query))
    except Exception as e:
        return {"status_code": 404, "error": str(e)}


@app.get("/yandexpic/")
def read_yandexpic(query: str):
    try:
        return convert_api_response("Get Yandex Pictures", get_yandex_photo(query))
    except Exception as e:
        return {"status_code": 404, "error": str(e)}


@app.get("/lyrics/")
async def read_lyrics(query: str):
    try:
        return convert_api_response("Get Lyrics", await get_lyrics(query))
    except Exception as e:
        return {"status_code": 404, "error": str(e)}


@app.get("/translate/")
def translate(query: str, src: str = "auto", lang: str = "tr"):
    translator = Translator()
    result = translator.translate(
        text=query,
        src=src,
        dest=lang,
    )
    try:
        return convert_api_response("Translate", result)
    except Exception as e:
        return {"status_code": 404, "error": str(e)}


@app.get("/movie/")
async def movie():
    data = await get_tmdb_data()
    try:
        retu = convert_api_response("Get Movie", data)
        retu.update({"item_count": len(data)})
        return retu
    except Exception as e:
        return {"status_code": 404, "error": str(e)}