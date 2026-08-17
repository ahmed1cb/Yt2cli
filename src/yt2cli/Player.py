# Python Mods
import os
import platform
import shutil
import subprocess

# Required Libs
import yt_dlp


class Player:
    def play(self, basic_url: str):
        stream_url = self._get_stream_url(basic_url)

        if not stream_url:
            return
        self.open_with_player(stream_url)

    def open_with_player(self, stream_url: str):
        if shutil.which("mpv"):
            subprocess.run(
                ["mpv", stream_url],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return

        system = platform.system()
        if system == "Windows":
            os.startfile(stream_url)
        elif system == "Darwin":
            subprocess.run(
                ["open", stream_url],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        else:
            subprocess.run(
                ["xdg-open", stream_url],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

    def _get_stream_url(self, basic: str):
        try:
            ydl_opts = {
                "format": "best",
                "quiet": True,
                "merge_output_format": "mp4",
                "noplaylist": True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(basic, download=False)
                return info["url"]
        except Exception:
            print("Failed to resolve stream URL.")
            return None
