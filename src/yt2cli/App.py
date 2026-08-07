# Python Mods
import os
from asyncio.taskgroups import TaskGroup

# App Modules
from .Backend import Backend


class Yt2cli:
    def __init__(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")
        self.options = {
            "search": {
                "desc": "Use it To Search for Youtube Videos , usage: search :query",
                "_callable": self._search,
            },
            "open": {
                "desc": "Use It to Open A video From the List of Searched Videos",
                "_callable": self._load,
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
        self.videos = []
        queryStr = " ".join(query)

        videos = self.backend.search(queryStr)
        i = 0
        print("\n\n")
        for vid in videos:
            target = videos[vid]
            self.videos.append(target)
            print(f"{i}-{target['title']} , BY CHANNEL [{target['channelName']}]")
            print("-" * 20)
            i += 1

    def _load(self, id: int | str = ""): ...
