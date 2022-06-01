from youtubesearchpython.__future__ import VideosSearch
from yt_dlp import YoutubeDL
import asyncio


mp3_data = []


async def mp3_links(url):
    with YoutubeDL() as ydl:
        info = ydl.extract_info(url, download=False)
        mp3_data.append(info["requested_formats"][-1]["url"])
    return


data = []


async def mee(i):
    # for i in v_result["result"]:
    url = i["link"]
    type = i["type"]
    duration = i["duration"]
    view = i["viewCount"]["short"]
    title = i["title"]
    published = i["publishedTime"]
    thumbnails = i["thumbnails"]
    if i["descriptionSnippet"]:
        description = "".join([x["text"] for x in i["descriptionSnippet"] if x != None])
    else:
        description = None
    channel = {
        "name": i["channel"]["name"],
        "url": i["channel"]["link"],
    }
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
    }
    data.append(dict_)


async def search_youtube(query: str = None):
    if query == None:
        return data
    else:
        v_search = VideosSearch(query, limit=5)
        v_result = await v_search.next()
        # urls = [i["link"] for i in v_result["result"]]
        tasks = []
        for i in v_result["result"]:
            print(i["link"])
            tasks.append(asyncio.create_task(mp3_links(i["link"])))
            tasks.append(asyncio.create_task(mee(i)))
        await asyncio.gather(*tasks)
        # mp3_data = await mp3_links(urls)
        # for i, v in enumerate(mp3_data):
        #     data[i]["mp3_url"] = v
        for index, value in enumerate(data):
            value["mp3_url"] = mp3_data[index]
        return data
