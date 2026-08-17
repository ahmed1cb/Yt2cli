# Python Mods
import os
import sys

import pyperclip

# App Modules
from .Backend import Backend
from .ParamManager import Params
from .Player import Player
from .SearchResults import Results


class Yt2cli:
    def __init__(self) -> None:
        self._clear()
        self.player = Player()
        self.options = {
            "channel": {
                "desc": "Browse a channel's videos by its YouTube handle",
                "_callable": self._get_channel_videos,
            },
            "copy": {
                "desc": "Copy a video's URL to the clipboard (ID required)",
                "_callable": self._copy,
            },
            "open": {
                "desc": "Play a video from the list by its ID",
                "_callable": self._load,
            },
            "clear": {
                "desc": "Clear the terminal screen",
                "_callable": lambda x=0: self._clear(),
            },
            "show": {
                "desc": "Show the currently loaded videos",
                "_callable": lambda x=0: self.show_search_results(),
            },
            "exit": {
                "desc": "Exit the application",
                "_callable": lambda x=0: self._exit(),
            },
            "help": {
                "desc": "Show available commands",
                "_callable": lambda x=0: self.show_options(),
            },
            "reset": {
                "desc": "Clear the video list and backend cache",
                "_callable": lambda x=0: self._reset(),
            },
            "cache:clear": {
                "desc": "Clear cached search results only",
                "_callable": lambda x=0: self._clear_cache(),
            },
            "more": {
                "desc": "Load more results from the last search",
                "_callable": lambda x=0: self._more(),
            },
            "download": {
                "desc": "Download a YouTube video",
                "_callable": self._download,
            },
            "playlist": {
                "desc": "Load videos from a YouTube playlist URL",
                "_callable": self._get_playlist,
            },
        }

        self.videos = []
        self.last_query = []  # [query , options]
        self.backend = Backend()
        self.show_options()

    def handle(self, args: str):
        if not args.strip():
            return

        args = args.split()
        command = args[0]

        params = args[1:]

        target_option = self.options.get(command)
        # Now the Search is the Default Option

        if target_option is None:
            if self.backend.is_valid_url(command) and self.backend.is_youtube_video_url(
                command
            ):
                print("Resolving video...")
                self.player.play(command)
                return
            params.insert(0, command)
            self._search(params)
            return
        _callable = target_option.get("_callable")
        _callable(params)

    def _exit(self):
        print("Goodbye.")
        sys.exit()

    def _get_playlist(self, params):
        play_list_allowed_opts = {"--limit": int, "--thumbs": str}
        parser = Params(play_list_allowed_opts, params)
        if parser.failed():
            return
        strs = parser.get_normal_strings()
        options = {"limit": 10, "thumbs": "yes"} | parser.get_params_with_values()
        if not strs:
            print("Playlist URL is required.")
            return
        try:
            url = strs[0]
            if (
                not self.backend.is_valid_url(url)
                and not "?list=" in url
                and not "/playlist" in url
            ):
                print("Invalid playlist URL.")
                return
            print("Loading playlist videos...")

            vids = self.backend.get_playlist_videos(url, options)

            self.videos = list(vids.values())

            self._show()
        except Exception:
            print("Failed to load playlist. Check the URL and try again.")

    def _more(self):
        if not self.last_query:
            print("No previous search to extend.")
            return
        self._clear()  # Clear Terminal
        query_str = self.last_query[0]
        options = self.last_query[1]

        options["limit"] = options["limit"] + 5
        print("Loading...")
        new_vids = list(self.backend.search(query_str, options).values())
        self.videos = new_vids
        self._show()

    def _get_channel_videos(self, params):
        channel_allowed_options = {"--thumbs": str, "--limit": int}
        channel_options = {"limit": 10, "thumbs": "yes"}
        parser = Params(channel_allowed_options, params)
        channel_options = channel_options | parser.get_params_with_values()
        if not parser.get_normal_strings():
            print("Channel name is required.")
            return
        if parser.failed():
            return

        channel_name = parser.get_normal_strings()[0]
        try:
            self.videos = list(
                self.backend.get_channel_videos(channel_name, channel_options).values()
            )

            if not self.videos:
                print("No results found.")
                return
            self._clear()
            print(f"Showing videos from {channel_name}.")
            self._show()
        except Exception:
            print("Failed to load channel videos.")

    def _copy(self, params):
        parser = Params({}, params)
        strs = parser.get_normal_strings()
        if not strs:
            print("Video ID is required.")
            return
        try:
            id = int(strs[0])
            target = self.videos[id]
        except Exception:
            print("Invalid or unknown video ID.")
            return

        pyperclip.copy(target["url"])

        print("URL copied to clipboard.")

    def _clear_cache(self):
        self.backend.clear_cache()

    def _clear_list(self):
        self.videos = []

    def _reset(self):
        self._clear_cache()
        self._clear_list()

    def show_options(self):
        print("=" * 50)
        print(f"{'AVAILABLE OPTIONS':^50}")
        print("=" * 50)

        for option in self.options:
            desc = self.options[option]["desc"]
            print(f"  [{option}] {desc}")

        print("=" * 50)

    def _search(self, params: list | None = None):
        if params is None:
            params = []
        self._clear()
        search_options = {"limit": 10, "type": "both", "thumbs": "yes"}
        v_types = ["short", "long", "both"]
        th_opts = ["yes", "no", "false", "true"]

        # key : type
        search_allowed_options = {"--limit": int, "--type": str, "--thumbs": str}

        search_params_parser = Params(search_allowed_options, params)

        search_options = search_options | search_params_parser.get_params_with_values()

        if search_params_parser.failed():
            return
        query_str = " ".join(search_params_parser.get_normal_strings())

        if search_options.get("type") not in v_types:
            print("Invalid type. Available: short, long, both")
            return

        # when there is a params But no query
        if not query_str:
            print("Enter a search query.")
            return

        if search_options["thumbs"].lower() not in th_opts:
            print("--thumbs accepts: yes, no, true, false")
            return

        self.last_query = [query_str, search_options]

        print("Searching...")

        self.videos = list(self.backend.search(query_str, search_options).values())
        self._clear()

        if not self.videos:
            print("No results found.")
            return
        print(
            f"Results for: {query_str} (limit={search_options['limit']}, type={search_options['type']}, thumbs={search_options['thumbs']})"
        )

        self._show()

    def show_search_results(self):
        if not self.videos:
            print("No videos loaded.")
            return
        print("Displaying loaded videos...")
        self._show()

    def _show(self):
        for i, target in enumerate(self.videos):
            target["id"] = i
        results_view = Results(self.videos)
        results_view.print_video_cards()

    def _load(self, params: list | None = None):
        if params is None:
            params = []
        if not params:
            print("Video ID or URL is required.")
            return
        video_allowed_options = {
            "--url": str,
        }
        open_parser = Params(video_allowed_options, params)

        video_options = open_parser.get_params_with_values()
        if video_options.get("url"):
            try:
                self.player.play(video_options["url"])
                return
            except Exception:
                print("Failed to play video.")
                return
        try:
            id = int(open_parser.get_normal_strings()[0])
            target = self.videos[id]
        except Exception:
            print("Invalid or unknown video ID.")
            return

        url = target.get("url")

        self.player.play(url)

    def _download(self, params: list | None = None):
        if params is None:
            params = []
        download_allowed_options = {"--url": str, "--path": str}

        download_parser = Params(download_allowed_options, params)
        download_options = download_parser.get_params_with_values()
        url = download_options.get("url")
        save_path = download_options.get("path")
        if download_parser.failed():
            return
        if (
            not save_path
            or not os.path.exists(save_path)
            or not os.path.isdir(save_path)
        ):
            print("A valid directory path is required. Usage: --path=<dir>")
            return
        if url:
            try:
                self.backend.download(url, save_path)
            except Exception:
                print("Failed to download video.")
            return

        targets = []
        strs = download_parser.get_normal_strings()
        if strs and strs[0] == "all":
            for vid in self.videos:
                self.backend.download(vid.get("url"), save_path)
            return
        for id in strs:
            try:
                targets.append(self.videos[int(id)])
            except Exception:
                print(f"Video with ID {id} not found.")
        if not targets:
            print("No videos to download.")
            return

        for target in targets:
            url = target.get("url")
            self.backend.download(url, save_path)

    def _clear(self):
        os.system("cls" if os.name == "nt" else "clear")
