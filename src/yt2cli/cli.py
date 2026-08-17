# Python Modules
import sys

# maybe not on all platforms
try:
    import readline
except ImportError:
    pass
# App Modules
# Version
from . import Yt2cli, __version__


def main():
    if "--version" in sys.argv:
        print(__version__)
        return
    app: Yt2cli = Yt2cli()
    while True:
        try:
            args: str = input("Yt2Cli Run: ")
            app.handle(args)
        except (KeyboardInterrupt, EOFError):
            print("Goodbye.")
            sys.exit(0)
