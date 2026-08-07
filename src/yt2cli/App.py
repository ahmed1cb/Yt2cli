# Python Mods
import os
import sys

# App Modules
from .Backend import Backend
from .Player import Player


class Yt2cli:
    def __init__(self) -> None:
        self._clear()
        self.options = {
            "search": {
                "desc": "Use it To Search for Youtube Videos , usage: search :query",
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
        }
        self.videos = []
        self.backend = Backend()
        self.show_options()

    def handle(self, args: list | str):
        if type(args) is str:
            args = args.split()
        command = args[0]
        params = args[1:]

        targetOption = self.options.get(command)
        if targetOption is None:
            print("Option Not Found")
            self.show_options()
            return
        targetOption.get("_callable")(params)

    def show_options(self):
        print("*" * 5 + " Available Options " + "*" * 5)
        for option in self.options:
            print(f"{option} : {self.options.get(option)['desc']} ")

    def _search(self, query: str | list = ""):
        self._clear()
        self.videos = []
        queryStr = " ".join(query)

        videos = self.backend.search(queryStr)
        i = 0
        for vid in videos:
            target = videos[vid]
            self.videos.append(target)
            print(f"{i}-{target['title']} , BY CHANNEL [{target['channel']}]")
            print("-" * 20)
            i += 1

    def _list(self):
        i = 0
        for target in self.videos:
            print(f"{i}-{target['title']} , BY CHANNEL [{target['channel']}]")
            print("-" * 20)
            i += 1

    def _load(self, params: list = []):

        if not params or len(params) == 0:
            print("Id Is Required")
            return

        id = int(params[0])
        target = self.videos[id]
        if target is None:
            print("Video With That id Wasnt Found Please Try Again")

        url = target["url"]
        player = Player()

        player.play(url)

    def _clear(self):
        os.system("cls" if os.name == "nt" else "clear")
