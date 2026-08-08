# Required Modules
import yt_dlp


class Backend:
    def __init__(self):
        self.cache = {}

    def clear_cache(self):
        self.cache = {}

    def search(self, query: str, limit: int = 10) -> dict:

        queryKey = f"{query}x{limit}"

        final_results = {}
        ydl_opts = {
            "quiet": True,
            "extract_flat": True,
            "noplaylist": True,
        }

        if queryKey in self.cache:
            final_results = self.cache.get(queryKey)
        else:
            search_query = f"ytsearch{limit}:{query}"
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(search_query, download=False)
                entries = info.get("entries", [])
                for entry in entries:
                    final_results[entry.get("id")] = {
                        "id": entry.get("id"),
                        "title": entry.get("title"),
                        "url": entry.get("url"),
                        "channel": entry.get("channel") or entry.get("uploader"),
                        "views": self._parse_views(entry.get("view_count")),
                    }
        self.cache[queryKey] = final_results
        return final_results

    def _parse_views(self, views: int | str):
        try:
            views = int(views)
            if views >= 1_000_000_000:
                return f"{views / 1000_000_000:.2f}B"
            elif views >= 1_000_000:
                return f"{views / 1000_000:.2f}M"
            elif views >= 1_000:
                return f"{views / 1000:.2f}K"

            else:
                return views
        except:
            return views

    def get_channel_name(self, video):
        for key in ["longBylineText", "shortBylineText", "ownerText"]:
            txt = video.get(key, None)
            if txt is not None:
                return txt["runs"][0]["text"]

    def download(self, stream_url, output_path):
        ydl_opts = {
            "format": "best",  # 'best' usually selects the best quality stream available
            "outtmpl": f"{output_path}/%(title)s.%(ext)s",
            "quiet": False,
            "paths": {
                "home": output_path,
            },
        }

        print(f"Download Started On: {output_path}")
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([stream_url])
        except:
            print(f"Download failed")
