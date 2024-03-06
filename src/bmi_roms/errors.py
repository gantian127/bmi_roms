from __future__ import annotations


class RomsError(Exception):
    pass


class DataError(RomsError):
    def __init__(self, msg):
        self._msg = msg

    def __str__(self):
        return self._msg
