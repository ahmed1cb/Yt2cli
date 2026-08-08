# Yt2Cli

A simple command-line (CLI) tool for searching and playing YouTube videos directly from the terminal, without needing to open a browser.

## Features

- Search YouTube videos by keyword, with an optional result limit (`--limit=<n>`, default 10, max 100)
- Results are cached per query, so re-searching the same keyword is instant
- Display search results as formatted video cards (title, ID, channel, views with `K`/`M`/`B` suffix)
- Play any video from the list through [mpv](https://mpv.io), falling back to the system's default application if mpv isn't installed
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

| Command          | Description                                           |
| ---------------- | ----------------------------------------------------- |
| `search <query>` | Search YouTube videos (`--limit=<n>` optional)        |
| `list`           | Show the currently loaded videos from the last search |
| `open <id>`      | Play a video from the list by its number              |
| `clear`          | Clear the terminal screen                             |
| `help`           | Show a list of available commands                     |
| `exit`           | Close the app                                         |

> **Note:** Any input that isn't a recognized command is treated as a search query.

### Example

```
Yt2Cli Run: search python tutorial
 Now Loading...
********** Search Results For: python tutorial , Limit= 10 **********
 ──────────────────────────────────────────────────────────────
  Python Basics for Beginners
  ID       : 0
  Channel  : Programming Academy
  Views    : 2.34M
 ──────────────────────────────────────────────────────────────

# The id here is not the id of the video its the video index on the list

Yt2Cli Run: open 0
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
- Search results are cached per query in memory; playing a video re-resolves the stream URL with yt-dlp.
- Download the Deno Javascript Runtime to get the best Video Quality

## License

MIT
