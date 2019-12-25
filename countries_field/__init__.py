# coding=utf-8
VERSION = (0, 6)


def get_version():
    return '.'.join(map(str, VERSION))

__version__ = get_version()
