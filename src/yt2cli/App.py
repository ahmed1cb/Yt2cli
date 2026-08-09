# Python Mods
import os
import re
import shutil
import sys

# Required To Work
from term_image.image import BlockImage

# App Modules
from .Backend import Backend
from .Player import Player

ANSI_RE = re.compile(r"\033\[[0-9;]*m")


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
            self.print_video_card(target)
            print()

    def print_video_card(self, video: dict):
        title = video.get("title") or "Untitled"
        channel = video.get("channel") or "Unknown"
        views = video.get("views") or "-"
        duration = video.get("duration")
        vid = video.get("id")

        info_lines = [
            f"\033[1m[{vid}] {self._truncate(title, 45)}\033[0m",
            "",
            f"      {self._truncate(channel, 40)}",
            f"      {views} views",
            f"      {duration} duration",
        ]

        img_lines = []
        if video.get("thumbnail"):
            img = self.get_image(video["thumbnail"])
            img_lines = str(img).split("\n")

        content_width = (
            max((self._visible_len(l) for l in img_lines), default=0)
            + max((self._visible_len(l) for l in info_lines), default=0)
            + 3
        )

        separator = "─" * min(content_width, shutil.get_terminal_size().columns)
        print(separator)
        self._print_side_by_side(img_lines, info_lines)
        print(separator)

    def _print_side_by_side(self, left_lines, right_lines, gap=3):
        img_width = max((self._visible_len(l) for l in left_lines), default=0)

        max_lines = max(len(left_lines), len(right_lines))
        left_lines = left_lines + [""] * (max_lines - len(left_lines))
        right_lines = right_lines + [""] * (max_lines - len(right_lines))

        for left, right in zip(left_lines, right_lines):
            padding = " " * (img_width - self._visible_len(left) + gap)
            print(f"{left}{padding}{right}")

    def _visible_len(self, text):
        return len(ANSI_RE.sub("", text))

    def _truncate(self, text, max_len):
        return text if len(text) <= max_len else text[: max_len - 1] + "…"

    def get_image(self, path: str):
        return BlockImage.from_url(path, width=40)

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
