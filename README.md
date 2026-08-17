# Yt2Cli

A simple command-line (CLI) tool for searching and playing YouTube videos directly from the terminal, without needing to open a browser.

## Features

- Search YouTube videos by keyword, with an optional result limit (`--limit=<n>`, default 10)
- Filter results by video type with `--type=short|long|both` (short = 4 minutes or less, long = more than 4 minutes)
- Browse a channel's videos by its YouTube handle: `channel <channeluser>` (supports `--limit=<n>` and `--thumbs=yes|no`)
- Load videos from a YouTube playlist URL: `playlist <url>` (supports `--limit=<n>` and `--thumbs=yes|no`)
- Results are cached per query and options (limit, type, thumbs), so re-searching the same keyword is instant
- Load more results from the last search with `more`
- Display search results as formatted video cards (title, channel, views with `K`/`M`/`B` suffix, duration, and Short/Normal badge) with the video thumbnail rendered as block/pixel art; cards flow into a responsive multi-column grid based on terminal width. Disable thumbnail rendering with `--thumbs=no` for faster results
- Play any video from the list through [mpv](https://mpv.io), falling back to the system's default application if mpv isn't installed
- Play a video directly by URL without searching: `open --url=<youtube-url>`
- Type a YouTube URL directly at the prompt to play it automatically, no command needed (recognizes `youtube.com/watch`, `youtu.be`, `/shorts/`, and `/embed/` links)
- Download one or more videos to an existing folder with `--path=<existing-dir>`: `download <id1> <id2> ... --path=~/Videos`, or download all loaded videos with `download all --path=~/Videos`, including direct URLs: `download --url=<youtube-url> --path=~/Videos`
- Copy a video's URL to the clipboard with `copy <id>` (uses `pyperclip`)
- Clear the in-memory cache and the loaded list with `reset` or `cache:clear`
- Any unrecognized command is treated as a search query
- Command line editing and history via `readline`
- Cross-platform: works on Windows, macOS, and Linux

## Requirements

### 1. Python

Recommended version: **Python 3.10 or newer**.

### 2. mpv for video playback (optional)

The app relies on [mpv](https://mpv.io/installation/) as the default player. If it's not installed, the app will fall back to opening the link with the system's default application.

**Installing mpv:**

| OS               | Command                                              |
| ---------------- | ---------------------------------------------------- |
| Fedora           | `sudo dnf install mpv`                               |
| Ubuntu / Debian  | `sudo apt install mpv`                               |
| macOS (Homebrew) | `brew install mpv`                                   |
| Windows          | Download from [mpv.io](https://mpv.io/installation/) |

## Installation

```bash
pip install yt2cli
```

## Usage

```bash
yt2cli
```

This launches an interactive prompt. Type a command and press Enter.

## Available Commands

| Command         | Description                                                                                                                 |
| --------------- | --------------------------------------------------------------------------------------------------------------------------- |
| `channel <user>` | Browse a channel's videos by its YouTube handle (`channel <channeluser>`); supports `--limit=<n>` and `--thumbs=yes|no`     |
| `playlist <url>` | Load videos from a YouTube playlist URL; supports `--limit=<n>` and `--thumbs=yes|no`                                      |
| `show`          | Show the currently loaded videos from the last search                                                                       |
| `open <id>`     | Play a video from the list by its number; use `open --url=<youtube-url>` to play a direct URL                               |
| `download <id>` | Download one or more videos from the list to an existing folder (`download <id1> <id2> ... --path=<existing-dir>`), or all videos with `download all --path=<existing-dir>`; use `download --url=<youtube-url> --path=<existing-dir>` for a direct URL |
| `copy <id>`     | Copy the URL of a video from the list to the clipboard                                                                      |
| `more`          | Load more videos from the last search (adds 5 more results)                                                                 |
| `reset`         | Clear the loaded video list and the backend cache                                                                           |
| `cache:clear`   | Remove the cached search results only                                                                                       |
| `clear`         | Clear the terminal screen                                                                                                   |
| `help`          | Show a list of available commands                                                                                           |
| `exit`          | Close the app                                                                                                               |

> **Note:** Any input that isn't a recognized command is treated as a search query. A direct YouTube URL (`youtube.com/watch`, `youtu.be/...`, `/shorts/...`, or `/embed/...`) is played automatically instead of being searched.

### Example

```
==================================================
                  AVAILABLE OPTIONS
==================================================
  [channel]  Browse a channel's videos by its YouTube handle
  [copy]  Copy a video's URL to the clipboard (ID required)
  [open]  Play a video from the list by its ID
  [clear]  Clear the terminal screen
  [show]  Show the currently loaded videos
  [exit]  Exit the application
  [help]  Show available commands
  [reset]  Clear the video list and backend cache
  [cache:clear]  Clear cached search results only
  [more]  Load more results from the last search
  [download]  Download a YouTube video
  [playlist]  Load videos from a YouTube playlist URL
  ==================================================

Yt2Cli Run: python tutorial --type=both
Searching...
Results for: python tutorial (limit=10, type=both, thumbs=yes)
 ──────────────────────────────────────────────────────────────
 ┌─────────────── block art ───────────────┐  [0] Python Basics for Beginners
 │ ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │      Programming Academy
 │ ░░░░░░ ░░ ░ ░  ░░   ░  ░░░ ░░░ ░░ ░░░  │      2.34M views
 │ ░ ░░░░ ░ ░░ ░ ░ ░░ ░ ░░ ░ ░░░ ░ ░░░░░  │      18:42 duration
 │ ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │      Normal video
 └─────────────────────────────────────────┘
 ──────────────────────────────────────────────────────────────

# The number in [brackets] is the video's index in the list (used by `open`/`download`/`copy`), not the YouTube video ID

Yt2Cli Run: open 0
```

### Video Card Layout

Each search result is printed as a card:

```
 ──────────────────────────────────────────────────────────────
 ┌─────────────── block art ───────────────┐  [0] Python Basics for Beginners
 │ ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │      Programming Academy
 │ ░░░░░░ ░░ ░ ░  ░░   ░  ░░░ ░░░ ░░ ░░░  │      2.34M views
 │ ░ ░░░░ ░ ░░ ░ ░ ░░ ░ ░░ ░ ░░░ ░ ░░░░░  │      18:42 duration
 │ ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │      Normal video
 └─────────────────────────────────────────┘
 ──────────────────────────────────────────────────────────────
```

- The card is bounded by a horizontal line (`─`)
- **Left side:** the video thumbnail rendered as terminal block/pixel art (~40 columns wide) via `term-image`
- **Right side:** the bold `[index] Title` (truncated to 45 chars), the channel (truncated to 40 chars), the view count formatted with `K`/`M`/`B` suffixes, the video duration, and a `Short`/`Normal` video badge
- Cards are laid out in a responsive grid — as many cards per row as the terminal width allows, and each card is padded so columns align
- The `[index]` is the card's position in the loaded list — the number you pass to `open <id>`, `download <id>`, or `copy <id>`

You can also play a video directly by URL, without searching first:

```
Yt2Cli Run: open --url=https://www.youtube.com/watch?v=id
```

Or simply type the URL itself — it will be detected and played automatically (`youtube.com/watch`, `youtu.be/...`, `/shorts/...`, and `/embed/...` links are recognized):

```
Yt2Cli Run: https://www.youtube.com/watch?v=id
```

You can also browse a channel's videos directly by its YouTube handle:

```
Yt2Cli Run: channel MrBeast --limit=5
```

You can also load videos from a YouTube playlist URL:

```
Yt2Cli Run: playlist https://www.youtube.com/playlist?list=PLxxxx --limit=5
```

## Project Structure

```
yt2cli/
├── src/
│   └── yt2cli/
│       ├── __init__.py      # App export entry point
│       ├── App.py           # Core logic and command handling
│       ├── Backend.py       # Search logic (yt-dlp), result caching, and downloads
│       ├── Logger.py         # Custom silent yt-dlp logger
│       ├── ParamManager.py   # Parses `--option=value` arguments for commands
│       ├── Player.py        # Video playback (mpv with system fallback)
│       ├── SearchResults.py # Renders the video cards and thumbnail block art
│       └── cli.py           # Interactive REPL entry point
```

## Notes

- The app uses [yt-dlp](https://github.com/yt-dlp/yt-dlp) to search and extract video playback URLs.
- `channel <channeluser>` loads a channel's videos from its `/videos` tab using the channel's YouTube handle (`@handle` or just `handle`); it accepts `--limit=<n>` and `--thumbs=yes|no`, and results are cached per channel and options.
- `playlist <url>` loads videos from a YouTube playlist URL; it accepts `--limit=<n>` and `--thumbs=yes|no`, and results are cached per playlist and options.
- Search results are cached per query and options (limit, type, thumbs) in memory; playing a video re-resolves the stream URL with yt-dlp.
- `--type=short|long|both` filters results by duration: `short` videos are 4 minutes or less, `long` videos are more than 4 minutes, `both` returns everything.
- `--thumbs=yes|no` (also accepts `true`/`false`) toggles whether search results render the video thumbnail as block art; `no` skips fetching thumbnails for faster results.
- `more` re-searches the last query with a higher limit (adds 5 results each time).
- `download <id> --path=<existing-dir>` saves the video with `yt-dlp` into the given existing folder. The folder must already exist and is passed with `--path`. It accepts multiple ids at once: `download 0 2 5 --path=~/Videos`. Use `download all --path=<existing-dir>` to download every video currently loaded.
- `copy <id>` copies the video's URL to the clipboard via `pyperclip`.
- `open --url=<youtube-url>` plays any video directly by URL, without needing to search for it first.
- `download --url=<youtube-url> --path=<existing-dir>` downloads any video directly by URL, without needing to search for it first.
- Typing a YouTube URL (`youtube.com/watch`, `youtu.be/...`, `/shorts/...`, or `/embed/...`) directly at the prompt plays it automatically.

## License

MIT
