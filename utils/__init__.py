import pathlib
import sys


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Image:
    def __init__(self, url):
        self.url: str = url


def get_path():
    try:
        return sys._MEIPASS + '/'
    except AttributeError:
        return str(pathlib.Path(__file__).parent.parent.absolute()).replace('\\', '/') + '/'


def all_pokemon():
    return []
