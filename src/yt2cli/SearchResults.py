import os
import re
import shutil

from term_image.image import BlockImage

ANSI_RE = re.compile(r"\033\[[0-9;]*m")


class Results:
    def __init__(self, videos: list[dict]) -> None:
        self.videos = videos

    def _clear(self):
        os.system("cls" if os.name == "nt" else "clear")

    def print_video_cards(self, gap=2):
        if not self.videos:
            return

        raw_cards = [self._build_card_lines(v) for v in self.videos]

        card_width = max(
            max((self._visible_len(l) for l in card), default=0) for card in raw_cards
        )

        terminal_width = shutil.get_terminal_size().columns
        cols = max(1, terminal_width // (card_width + gap))

        padded_cards = [
            [self._pad(l, card_width, gap) for l in card] for card in raw_cards
        ]

        for row_start in range(0, len(padded_cards), cols):
            row_cards = padded_cards[row_start : row_start + cols]
            max_height = max(len(c) for c in row_cards)

            for c in row_cards:
                c.extend([" " * (card_width + gap)] * (max_height - len(c)))
            for line_idx in range(max_height):
                line = "".join(c[line_idx] for c in row_cards)
                print(line)

    def _build_card_lines(self, video: dict):
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
            img = self._get_image(video["thumbnail"])
            img_lines = str(img).split("\n")

        merged = self._merge_side_by_side(img_lines, info_lines)

        content_width = max((self._visible_len(l) for l in merged), default=0)
        separator = "─" * content_width

        return [separator] + merged + [separator]

    def _merge_side_by_side(self, left_lines, right_lines, gap=3):
        img_width = max((self._visible_len(l) for l in left_lines), default=0)
        max_lines = max(len(left_lines), len(right_lines))
        left_lines = left_lines + [""] * (max_lines - len(left_lines))
        right_lines = right_lines + [""] * (max_lines - len(right_lines))

        merged = []
        for left, right in zip(left_lines, right_lines):
            padding = " " * (img_width - self._visible_len(left) + gap)
            merged.append(f"{left}{padding}{right}")
        return merged

    def _pad(self, text, width, gap=2):
        return text + " " * (width - self._visible_len(text) + gap)

    def _visible_len(self, text):
        return len(ANSI_RE.sub("", text))

    def _truncate(self, text, max_len):
        return text if len(text) <= max_len else text[: max_len - 1] + "…"

    def _get_image(self, path: str):
        return BlockImage.from_url(path, width=40)
