# Yt2Cli

A simple command-line (CLI) tool for searching and playing YouTube videos directly from the terminal, without needing to open a browser.

## Features

- Search YouTube videos by keyword, with an optional result limit (`--limit=<n>`, default 10, max 100)
- Results are cached per query and limit, so re-searching the same keyword is instant
- Load more results from the last search with `more`
- Display search results as formatted video cards (title, ID, channel, views with `K`/`M`/`B` suffix) with the video thumbnail rendered as block/pixel art
- Play any video from the list through [mpv](https://mpv.io), falling back to the system's default application if mpv isn't installed
- Play a video directly by URL without searching: `open --url=<youtube-url>`
- Download videos directly to a folder you pick (native folder dialog per OS)
- Clear the in-memory cache and the loaded list with `reset` or `cache:clear`
- Any unrecognized command is treated as a search query
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

| Command          | Description                                                                                   |
| ---------------- | --------------------------------------------------------------------------------------------- |
| `search <query>` | Search YouTube videos (`--limit=<n>` optional)                                                |
| `list`           | Show the currently loaded videos from the last search                                         |
| `open <id>`      | Play a video from the list by its number; use `open --url=<youtube-url>` to play a direct URL |
| `download <id>`  | Download a video from the list to a folder you choose                                         |
| `more`           | Load more videos from the last search (adds 5 more results)                                   |
| `reset`          | Clear the loaded video list and the backend cache                                             |
| `cache:clear`    | Remove the cached search results only                                                         |
| `clear`          | Clear the terminal screen                                                                     |
| `help`           | Show a list of available commands                                                             |
| `exit`           | Close the app                                                                                 |

> **Note:** Any input that isn't a recognized command is treated as a search query.

### Example

```
==================================================
                 AVAILABLE OPTIONS
==================================================
  [search]  Use it To Search for Youtube Videos , usage: search :query \:limits
  [open]  Use It to Open A video From the List of Searched Videos
  [clear]  Clear The Terminal Screen
  [list]  Show The Current Loaded Videos
  [exit]  Close the App
  [help]  Show A List of Available Commands
  [reset]  Remove The Saved Search And Backend Cache
  [cache:clear]  Remove the Cached Search Results
  [more]  Get More Videos from the Last Searched Query
  [download]  Download A Youtube Video
==================================================

Yt2Cli Run: search python tutorial
********** Search Results For: python tutorial , Limit= 10 **********
 ──────────────────────────────────────────────────────────────
 ┌─────────────── block art ───────────────┐  [0] Python Basics for Beginners
 │ ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │
 │ ░░░░░░ ░░ ░ ░  ░░   ░  ░░░ ░░░ ░░ ░░░  │  📺  Programming Academy
 │ ░ ░░░░ ░ ░░ ░ ░ ░░ ░ ░░ ░ ░░░ ░ ░░░░░  │  👁   2.34M views
 │ ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │
 └─────────────────────────────────────────┘
 ──────────────────────────────────────────────────────────────

# The number in [brackets] is the video's index in the list (used by `open`/`download`), not the YouTube video ID

Yt2Cli Run: open 0
```

### Video Card Layout

Each search result is printed as a card:

```
 ──────────────────────────────────────────────────────────────
 ┌─────────────── block art ───────────────┐  [0] Python Basics for Beginners
 │ ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │
 │ ░░░░░░ ░░ ░ ░  ░░   ░  ░░░ ░░░ ░░ ░░░  │  📺  Programming Academy
 │ ░ ░░░░ ░ ░░ ░ ░ ░░ ░ ░░ ░ ░░░ ░ ░░░░░  │  👁   2.34M views
 │ ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ │
 └─────────────────────────────────────────┘
 ──────────────────────────────────────────────────────────────
```

- The card is bounded by a horizontal line (`─`)
- **Left side:** the video thumbnail rendered as terminal block/pixel art (~40 columns wide) via `term-image`
- **Right side:** the bold `[index] Title` (truncated to 45 chars), the channel with 📺 (truncated to 40 chars), and the view count with 👁, formatted with `K`/`M`/`B` suffixes
- The `[index]` is the card's position in the loaded list — the number you pass to `open <id>` or `download <id>`

You can also play a video directly by URL, without searching first:

```
Yt2Cli Run: open --url=https://www.youtube.com/watch?v=id
```

## Project Structure

```
yt2cli/
├── src/
│   └── yt2cli/
│       ├── __init__.py     # App export entry point
│       ├── App.py          # Core logic and command handling
│       ├── Backend.py      # Search logic (yt-dlp) and result caching
│       ├── Player.py       # Video playback (mpv with system fallback)
│       └── cli.py          # Interactive REPL entry point
```

## Notes

- The app uses [yt-dlp](https://github.com/yt-dlp/yt-dlp) to search and extract video playback URLs.
- Search results are cached per query and limit in memory; playing a video re-resolves the stream URL with yt-dlp.
- `more` re-searches the last query with a higher limit (adds 5 results each time).
- `download <id>` opens a native folder-picker dialog (zenity on Linux, osascript on macOS, PowerShell on Windows) and saves the video with `yt-dlp`.
- `open --url=<youtube-url>` plays any video directly by URL, without needing to search for it first.

## License

MIT
