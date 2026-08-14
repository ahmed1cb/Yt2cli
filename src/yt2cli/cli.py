# Python Modules
import readline
import sys

# App Modules
from . import Yt2cli


def main():
    app = Yt2cli()
    while True:
        try:
            args = input("Yt2Cli Run: ")
            app.handle(args)
        except KeyboardInterrupt:
            sys.exit("-App Closed-")
