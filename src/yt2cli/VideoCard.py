# Python mods
import re
import shutil

# Required To run
from term_image.image import BlockImage

ANSI_RE = re.compile(r"\033\[[0-9;]*m")


class Card:
    def __init__(self, video: dict) -> None:
        self.video = video

    def print_video_card(self):
        video = self.video
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
