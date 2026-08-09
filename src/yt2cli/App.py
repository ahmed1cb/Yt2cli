# Python Mods
import os
import sys

from .Backend import Backend
from .Player import Player

# App Modules
from .VideoCard import Card


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
        queryStr = self.lastQueury[0]
        limit = self.lastQueury[1]
        self.lastQueury[1] = limit + 5
        print(" Now Loading...")
        newVids = list(self.backend.search(queryStr, limit + 5).values())
        self.videos = newVids
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

    def _search(self, params: str | list = ""):
        params = params or []
        self._clear()
        self.videos = []
        limit = 10
        queryParts = []
        for param in params:
            if param.startswith("--limit"):
                try:
                    limit = int(param[param.index("=") + 1 :])
                    if limit > 100:
                        print("Invalid Limit Param , Max Limit is 100")
                        return
                except:
                    print("Invalid limit. Usage: search <query> --limit=<limit>")
                    return
            else:
                queryParts.append(param)

        queryStr = " ".join(queryParts)
        self.lastQueury = [queryStr, limit]
        if not queryStr:
            print("Query String Is Required")
            return

        print(" Now Loading...")
        videos = self.backend.search(queryStr, limit)
        self._clear()

        print(
            "*" * 10 + f" Search Results For: {queryStr} , Limit= {limit} " + "*" * 10
        )
        self.videos = list(videos.values())
        self._list()

    def _list(self):
        for i, target in enumerate(self.videos):
            target["id"] = i
            card = Card(target)
            card.print_video_card()
            print()  # Empty Line

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
