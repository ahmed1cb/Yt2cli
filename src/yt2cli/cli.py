# Python Modules
import sys

# App Modules
from . import Yt2cli


def main():
    app = Yt2cli()
    while True:
        try:
            args = input("Enter Command to Continue: ")
            app.handle(args)
        except KeyboardInterrupt:
            sys.exit(" App Closed")
        except Exception:
            print("Something Went Wrong")
