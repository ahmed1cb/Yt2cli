# Required Modules
from urllib.parse import quote, urlparse

import yt_dlp

from .Logger import Logger


class Backend:
    def __init__(self):
        self.cache = {}
        self.data_opts = {
            "quiet": True,
            "extract_flat": "in_playlist",
            "noplaylist": True,
            "no_warnings": True,
            "ignoreerrors": True,
            "logger": Logger(),
        }

    def get_playlist_videos(self, url: str, options: dict):
        limit = options.get("limit", 10)
        get_thumbnails = options.get("thumbs", "yes")
        opts = "_".join([f"{o}={options[o]}" for o in list(options.keys())])
        cache_key = f"{url.strip().strip(' ')}_{opts}"
        if self.cache.get(cache_key):
            return self.cache[cache_key]

        dl_opts = self.data_opts | {"playlistend": limit}
        results = self.get_url_videos(url, dl_opts, get_thumbnails)

        self.cache[cache_key] = results
        return results

    def get_url_videos(self, url, dl_opts, get_thumbnails):
        results = {}
        with yt_dlp.YoutubeDL(dl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if info and "entries" in info:
                for entry in info.get("entries", []):
                    if entry is None:
                        continue

                    duration_seconds = int(entry.get("duration") or 0)

                    results[entry.get("id")] = {
                        "id": entry.get("id"),
                        "title": entry.get("title"),
                        "url": entry.get("url"),
                        "channel": entry.get("uploader", "-"),
                        "views": self._parse_views(entry.get("view_count", 0)),
                        "duration": self._parse_duration(duration_seconds),
                        "thumbnail": self._get_thumbnail(entry)
                        if get_thumbnails.lower() in ["yes", "true"]
                        else None,
                        "is_short": duration_seconds <= (60 * 4),
                    }
        return results

    def get_channel_videos(self, channel: str, options: dict):
        limit = options.get("limit", 10)
        get_thumbnails = options.get("thumbs", "yes")
        url = f"https://youtube.com/@{channel.strip().strip('@')}/videos"
        opts = "_".join([f"{o}={options[o]}" for o in list(options.keys())])
        cache_key = f"{url.strip().strip(' ')}_{opts}"

        if self.cache.get(cache_key):
            return self.cache[cache_key]

        dl_opts = self.data_opts | {"playlistend": limit}
        results = self.get_url_videos(url, dl_opts, get_thumbnails)
        self.cache[cache_key] = results
        return results

    def is_valid_url(self, url: str):
        result = urlparse(url)
        return all([result.scheme, result.netloc])

    def clear_cache(self):
        self.cache = {}

    def search(self, query: str, options: dict):
        limit = options.get("limit", 10)
        type_filter = options.get("type", "both")
        get_thumbnails = options.get("thumbs", "yes")
        opts = "_".join([f"{o}={options[o]}" for o in list(options.keys())])
        cache_key = f"{query.strip().strip(' ')}_{opts}"

        if self.cache.get(cache_key):
            return self.cache.get(cache_key)
        url = f"https://www.youtube.com/results?search_query={quote(query)}{'&sp=EgIYAQ%3D%3D' if type_filter == 'short' else ''}"  # Less Than 4 Mins is a short
        opts = self.data_opts | {"playlistend": limit}
        final_results = self.get_url_videos(url, opts, get_thumbnails)
        self.cache[cache_key] = final_results
        return final_results

    def _parse_duration(self, seconds: int) -> str:
        seconds = int(seconds)
        hrs, remainder = divmod(seconds, 3600)
        mins, secs = divmod(remainder, 60)

        if hrs > 0:
            return f"{hrs}:{mins:02d}:{secs:02d}"
        return f"{mins}:{secs:02d}"

    def _get_thumbnail(self, entry):
        thumbnails = entry.get("thumbnails")
        if thumbnails:
            return thumbnails[-1].get("url")
        return entry.get("thumbnail")

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
                return views or "-"  # Cant Show Playlists Views
        except Exception:
            return views or "-"  # Cant Show Playlists Views

    def download(self, stream_url, output_path: str):
        if not self.is_valid_url(stream_url):
            print("Invalid URL.")
            return

        ydl_opts = {
            "format": "best",  # 'best' usually selects the best quality stream available
            "outtmpl": f"{output_path}/%(title)s.%(ext)s",
            "quiet": False,
            "paths": {
                "home": output_path,
            },
            "downloader_args": {"ffmpeg": ["-loglevel", "error"]},
        }

        print(f"Downloading to: {output_path}")
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([stream_url])
        except Exception:
            print("Download failed.")

    def is_youtube_video_url(self, url: str) -> bool:
        parsed = urlparse(url)
        host = parsed.netloc.lower().replace("www.", "").replace("m.", "")

        if host == "youtu.be":
            return len(parsed.path.strip("/")) > 0

        if host == "youtube.com":
            return parsed.path.startswith(("/watch", "/shorts/", "/embed/"))

        return False
