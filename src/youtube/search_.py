from youtubesearchpython.__future__ import VideosSearch
from yt_dlp import YoutubeDL
import asyncio


async def search_youtube(query: str = None):
    data = []
    if query == None:
        return data
    else:
        v_search = VideosSearch(query, limit=7)
        v_result = await v_search.next()
        for i in v_result["result"]:
            type = i["type"]
            duration = i["duration"]
            view = i["viewCount"]["short"]
            title = i["title"]
            published = i["publishedTime"]
            thumbnails = i["thumbnails"]
            if i["descriptionSnippet"]:
                description = "".join(
                    [x["text"] for x in i["descriptionSnippet"] if x != None]
                )
            else:
                description = None
            channel = {
                "name": i["channel"]["name"],
                "url": i["channel"]["link"],
            }
            url = i["link"]
            with YoutubeDL() as ydl:
                info = ydl.extract_info(url, download=False)
            dict_ = {
                "type": type,
                "title": title,
                "description": description,
                "url": url,
                "view": view,
                "duration": duration,
                "published": published,
                "thumbnails": thumbnails,
                "channel": channel,
                "mp3_link": info["requested_formats"][-1]["url"],
            }
            data.append(dict_)
        return data
