# Required Modules
import platform
import subprocess
from urllib.parse import urlparse

import yt_dlp


class Backend:
    def __init__(self):
        self.cache = {}
        self.output_path = None

    def is_valid_url(self, url):
        result = urlparse(url)
        return all([result.scheme, result.netloc])

    def clear_cache(self):
        self.cache = {}

    def search(self, query: str, options: dict) -> dict:

        limit = options["limit"]
        type = options["type"]
        get_thumbnails = options["thumbs"]
        opts = "_".join([f"{o}={options[o]}" for o in list(options.keys())])
        queryKey = f"{query.strip().strip(' ')}_{opts}"
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
                    duration_seconds = int(entry.get("duration") or 0)

                    base_data = {
                        "id": entry.get("id"),
                        "title": entry.get("title"),
                        "url": entry.get("url"),
                        "channel": entry.get("channel") or entry.get("uploader"),
                        "views": self._parse_views(entry.get("view_count")),
                        "duration": self._parse_duration(duration_seconds),
                        "thumbnail": self._get_thumbnail(entry)
                        if get_thumbnails.lower() in ["yes", "true"]
                        else None,
                    }

                    if type == "long":
                        if duration_seconds > 60:
                            final_results[entry.get("id")] = {
                                **base_data,
                                "is_short": False,
                            }

                    elif type == "short":
                        if duration_seconds <= 60:
                            final_results[entry.get("id")] = {
                                **base_data,
                                "is_short": True,
                            }

                    else:
                        final_results[entry.get("id")] = {
                            **base_data,
                            "is_short": duration_seconds <= 60,
                        }

        self.cache[queryKey] = final_results
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
                return views
        except:
            return views

    def get_channel_name(self, video):
        for key in ["longBylineText", "shortBylineText", "ownerText"]:
            txt = video.get(key, None)
            if txt is not None:
                return txt["runs"][0]["text"]

    def download(self, stream_url):
        output_path = self.output_path or self.open_dialog()
        ydl_opts = {
            "format": "best",  # 'best' usually selects the best quality stream available
            "outtmpl": f"{output_path}/%(title)s.%(ext)s",
            "quiet": False,
            "paths": {
                "home": output_path,
            },
            "downloader_args": {"ffmpeg": ["-loglevel", "error"]},
        }

        print(f"Download Started On: {output_path}")
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([stream_url])
        except:
            print(f"Download failed")

    def open_dialog(self):
        system = platform.system()

        if system == "Linux":
            result = subprocess.run(
                [
                    "zenity",
                    "--file-selection",
                    "--directory",
                    "--title=Choose Directory to Save the Video inside",
                ],
                capture_output=True,
                text=True,
            )

            self.output_path = result.stdout.strip()

        elif system == "Darwin":  # macOS
            result = subprocess.run(
                [
                    "osascript",
                    "-e",
                    'POSIX path of (choose folder with prompt "Choose Directory to Save the Video inside")',
                ],
                capture_output=True,
                text=True,
            )
            self.output_path = result.stdout.strip()

        elif system == "Windows":
            ps_script = """
                                Add-Type -AssemblyName System.Windows.Forms
                                $dialog = New-Object System.Windows.Forms.FolderBrowserDialog
                                $dialog.ShowDialog() | Out-Null
                                $dialog.SelectedPath
                        """
            result = subprocess.run(
                ["powershell", "-Command", ps_script], capture_output=True, text=True
            )

            self.output_path = result.stdout.strip()

        return self.output_path
