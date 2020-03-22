import os

from library.api.api import API


DEFAULT_CONFIG_DIRECTORY = os.path.expanduser("~/Documents/Диплом/.trans/")
DEFAULT_DATABASE_URL = ''.join(["sqlite:///",
                                DEFAULT_CONFIG_DIRECTORY,
                                "trans.db"])


def get_api():
    return API(DEFAULT_DATABASE_URL)
