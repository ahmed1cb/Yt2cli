from importlib.metadata import PackageNotFoundError, version

from .App import Yt2cli

try:
    __version__ = version("yt2cli")
except PackageNotFoundError:
    __version__ = "0.0.0"
