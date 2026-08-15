# Python Modules
import sys

# maybe not on all platforms
try:
    import readline
except ImportError:
    pass
# App Modules
from . import Yt2cli


def main():
    app: Yt2cli = Yt2cli()
    while True:
        try:
            args: str = input("Yt2Cli Run: ")
            app.handle(args)
        except (KeyboardInterrupt, EOFError):
            sys.exit("-App Closed-")
