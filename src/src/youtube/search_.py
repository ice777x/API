from youtubesearchpython.__future__ import VideosSearch
import asyncio


async def search_youtube(query: str = None):
    data = []
    if query == None:
        return data
    else:
        v_search = VideosSearch(query, limit=20)
        v_result = await v_search.next()
        for i in v_result["result"]:
            url = i["link"]
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
    return data
