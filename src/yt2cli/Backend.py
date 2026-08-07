# Required Modules
import yt_dlp


class Backend:
    def __init__(self):
        self.cache = {}

    def search(self, query: str) -> dict:
        final_results = {}
        ydl_opts = {
            "quiet": True,
            "extract_flat": True,
            "noplaylist": True,
        }

        if query in self.cache:
            final_results = self.cache.get(query)
        else:
            search_query = f"ytsearch{60}:{query}"
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(search_query, download=False)
                entries = info.get("entries", [])
                for entry in entries:
                    final_results[entry.get("id")] = {
                        "id": entry.get("id"),
                        "title": entry.get("title"),
                        "url": entry.get("url"),
                        "channel": entry.get("channel") or entry.get("uploader"),
                    }
        self.cache[query] = final_results
        return final_results

    def get_channel_name(self, video):
        for key in ["longBylineText", "shortBylineText", "ownerText"]:
            txt = video.get(key, None)
            if txt is not None:
                return txt["runs"][0]["text"]
