# Python Mods
import os
import sys

# App Modules
from .Backend import Backend
from .ParamManager import Params
from .Player import Player
from .SearchResults import Results


class Yt2cli:
    def __init__(self) -> None:
        self._clear()
        self.options = {
            "search": {
                "desc": "Use it To Search for Youtube Videos , usage: search :query \:limits",
                "_callable": self._search,
            },
            "open": {
                "desc": "Use It to Open A video From the List of Searched Videos",
                "_callable": self._load,
            },
            "clear": {
                "desc": "Clear The Terminal Screen",
                "_callable": lambda x=0: self._clear(),
            },
            "list": {
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
        self.lastQueury = []  # [query , limit]
        self.backend = Backend()
        self.show_options()

    def _more(self):
        if len(self.lastQueury) < 1:
            print("There is no History To Search From")
            return
        self._clear()  # Clear Terminal
        query_str = self.lastQueury[0]
        limit = self.lastQueury[1]
        self.lastQueury[1] = limit + 5
        print(" Now Loading...")
        new_vids = list(self.backend.search(query_str, limit + 5).values())
        self.videos = new_vids
        self._list()

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

        targetOption = self.options.get(command)
        # Now the Search is the Default Option
        if targetOption is None:
            params.insert(0, command)
            self._search(params)
            return
        targetOption.get("_callable")(params)

    def show_options(self):
        print("=" * 50)
        print(f"{'AVAILABLE OPTIONS':^50}")
        print("=" * 50)

        for option in self.options:
            desc = self.options.get(option)["desc"]
            print(f"  [{option}]  {desc}")

        print("=" * 50)

    def _search(self, params: list = []):
        self._clear()
        search_options = {"limit": 10, "type": "both"}
        v_types = ["short", "long", "both"]

        # key : type
        search_allowed_options = {"--limit": int, "--type": str}

        search_params_parser = Params(search_allowed_options, params)

        search_options = search_options | search_params_parser.get_params_with_values()

        query_str = " ".join(search_params_parser.get_normal_strings())

        if search_options["limit"] > 100:
            print("Invalid Limit , The max is 100")
            return

        if search_options.get("type") and search_options["type"] not in v_types:
            print("Invalid Video Type , Available Types: " + " | ".join(v_types))

            return
        if not query_str:
            print("Query String Is Required")
            return

        self.lastQueury = [query_str, search_options["limit"]]
        print(" Now Loading...")
        videos = self.backend.search(query_str, search_options)
        self._clear()

        print(
            "*" * 10
            + f" Search Results For: {query_str} , Limit = {search_options['limit']} , type = {search_options['type']}"
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
            print("Params Are Required")
            return
        video_native_url = ""
        for param in params:
            if param.startswith("--url"):
                video_native_url = param[param.index("=") + 1 :]

        player = Player()

        if video_native_url:
            try:
                player.play(video_native_url)
                return
            except:
                print("Something Went Wrong While Trying to Open the Video")
                return
        try:
            id = int(params[0])
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
            print("Id Is Required")
            return

        try:
            id = int(params[0])
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
        self.backend.download(url)

    def _clear(self):
        os.system("cls" if os.name == "nt" else "clear")
