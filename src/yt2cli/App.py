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
        player = Player()
        self.player = player
        self.options = {
            "copy": {
                "desc": "Use it to Copy the Youtube Video Url, Id Required",
                "_callable": self._copy,
            },
            "open": {
                "desc": "Use It to Open A video From the List of Searched Videos",
                "_callable": self._load,
            },
            "clear": {
                "desc": "Clear The Terminal Screen",
                "_callable": lambda x=0: self._clear(),
            },
            "show": {
                "desc": "Show The Current Loaded Videos",
                "_callable": lambda x=0: self._list(),
            },
            "exit": {
                "desc": "Close the App",
                "_callable": lambda x=0: sys.exit(" App Closed "),
            },
            "help": {
                "desc": "Show A List of Available Commands",
                "_callable": lambda x=0: self.show_options(),
            },
            "reset": {
                "desc": "Remove The Saved Search And Backend Cache",
                "_callable": lambda x=0: self._reset(),
            },
            "cache:clear": {
                "desc": "Remove the Cached Search Results",
                "_callable": lambda x=0: self._clear_cache(),
            },
            "more": {
                "desc": "Get More Videos from the Last Searched Query",
                "_callable": lambda x=0: self._more(),
            },
            "download": {
                "desc": "Download A Youtube Video",
                "_callable": self._download,
            },
        }
        self.videos = []
        self.lastQueury = []  # [query , options]
        self.backend = Backend()
        self.show_options()

    def _more(self):
        if len(self.lastQueury) < 1:
            print("There is no History To Search From")
            return
        self._clear()  # Clear Terminal
        query_str = self.lastQueury[0]
        options = self.lastQueury[1]

        options["limit"] = options["limit"] + 5
        print(" Now Loading...")
        new_vids = list(self.backend.search(query_str, options).values())
        self.videos = new_vids
        self._list()

    def _copy(self, params):
        parser = Params({}, params)
        strs = parser.get_normal_strings()
        if len(strs) == 0:
            print("id is Required")
            return
        target = None
        try:
            id = int(strs[0])
            target = self.videos[id]
        except:
            print("Invalid Id Or Id not in the Videos List")
            return

        if not target:
            return

        pyperclip.copy(target["url"])

        print("Copied Successfully")

    def _clear_cache(self):
        self.backend.clear_cache()

    def _clear_list(self):
        self.videos = []

    def _reset(self):
        self._clear_cache()
        self._clear_list()

    def handle(self, args: list | str):
        if not args:
            return
        if type(args) is str:
            args = args.split()
        command = args[0]

        params = args[1:]

        target_option = self.options.get(command)
        # Now the Search is the Default Option

        if target_option is None:
            if self.backend.is_valid_url(command) and "youtube.com/watch" in command:
                self.player.play(command)
                return
            params.insert(0, command)
            self._search(params)
            return
        callable = target_option.get("_callable")
        callable(params)

    def show_options(self):
        print("=" * 50)
        print(f"{'AVAILABLE OPTIONS':^50}")
        print("=" * 50)

        for option in self.options:
            desc = self.options[option]["desc"]
            print(f"  [{option}] {desc}")

        print("=" * 50)

    def _search(self, params: list = []):
        self._clear()
        search_options = {"limit": 10, "type": "both", "thumbs": "yes"}
        v_types = ["short", "long", "both"]
        th_opts = ["yes", "no", "false", "true"]

        # key : type
        search_allowed_options = {"--limit": int, "--type": str, "--thumbs": str}

        search_params_parser = Params(search_allowed_options, params)

        if search_params_parser.failed():
          return
        search_options = search_options | search_params_parser.get_params_with_values()

        query_str = " ".join(search_params_parser.get_normal_strings())

        if search_options["limit"] > 100:
            print("Invalid Limit , The max is 100")
            return

        if search_options.get("type") and search_options["type"] not in v_types:
            print("Invalid Video Type , Available Types: " + " | ".join(v_types))
            return

        if not query_str:
            print("Type Something To search")
            return
        if search_options["thumbs"].lower() not in th_opts:
            print("--thumbs can only Recive " + " / ".join(th_opts))
            return

        self.lastQueury = [query_str, search_options]

        print(" Now Loading...")
        videos = self.backend.search(query_str, search_options)
        self._clear()

        applied_opts_str = " ".join(
            [
                f"{option_name} = {search_options[option_name]}"
                for option_name in list(search_options)
            ]
        )
        print(
            "*" * 10
            + f" Search Results For: {query_str} , {applied_opts_str} "
            + "*" * 10
        )
        self.videos = list(videos.values())

        self._list()

    def _list(self):
        for i, target in enumerate(self.videos):
            target["id"] = i

        results_view = Results(self.videos)
        print(" Now Showing ...")
        results_view.print_video_cards()

    def _load(self, params: list = []):
        if not params or len(params) == 0:
            print("id or url Required")
            return
        video_options = {}
        video_allowed_options = {"--url": str}
        open_parser = Params(video_allowed_options, params)

        video_options = video_options | open_parser.get_params_with_values()

        if video_options.get("url"):
            try:
                self.player.play(video_options["url"])
                return
            except:
                print("Something Went Wrong While Trying to Open the Video")
                return
        try:
            id = int(open_parser.get_normal_strings()[0])
        except ValueError:
            print("Invalid Id , Should be a Number")
            return

        if id >= len(self.videos) or id < 0:
            print("Invalid Id, Should Be in the List of the Videos ")
            return

        target = self.videos[id]

        if target is None:
            print("Video With That id Wasnt Found Please Try Again")

        url = target["url"]

        player.play(url)

    def _download(self, params: list = []):
        if not params or len(params) == 0:
            print("id or url Required")
            return

        download_options = {}
        download_allowed_options = {"--url": str}

        download_parser = Params(download_allowed_options, params)
        download_options = download_parser.get_params_with_values()

        if download_options.get("url"):
            try:
                self.backend.download(download_options["url"])
            except:
                print("Something Went Wrong While Trying to Download The Video ")
            return

        targets = []

        for id in download_parser.get_normal_strings():
            try:
                targets.append(self.videos[int(id)])
            except:
                print(f"Cant Find Video with id {id}")
        if len(targets) == 0:
            print("Nothing to Download")
            return

        for target in targets:
            url = target["url"]
            self.backend.download(url)

    def _clear(self):
        os.system("cls" if os.name == "nt" else "clear")
