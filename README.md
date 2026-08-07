# Yt2Cli

A simple command-line (CLI) tool for searching and playing YouTube videos directly from the terminal, without needing to open a browser.

## Features

- Search YouTube videos by keyword
- Display search results (title + channel)
- Play any video from the list through an external player
- Cross-platform: works on Windows, macOS, and Linux

## Requirements

### 1. Python

Recommended version: **Python 3.10** or older (to avoid compatibility issues with some packages).

### 2. mpv for video playback (optinal)

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
poetry run yt2cli
```

## Available Commands

| Command          | Description                                           |
| ---------------- | ----------------------------------------------------- |
| `search <query>` | Search for YouTube videos                             |
| `list`           | Show the currently loaded videos from the last search |
| `open <id>`      | Play a video from the list by its number              |
| `clear`          | Clear the terminal screen                             |
| `help`           | Show a list of available commands                     |
| `exit`           | Close the app                                         |

### Example

```
Yt2Cli Run: search python tutorial
0-Python Basics , BY CHANNEL [Programming Academy]
--------------------
1-Learn Python for Beginners , BY CHANNEL [Code Channel]
--------------------

Yt2Cli Run: open 0
```

## Project Structure

```
yt2cli/
├── __init__.py     # App export entry point
├── App.py          # Core logic and command handling
├── Backend.py
├── Player.py
└── cli.py            # Entry point
```

## Notes

- The app uses [yt-dlp](https://github.com/yt-dlp/yt-dlp) to search and extract video playback URLs.

## License

MIT
