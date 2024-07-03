from typing import override

from .interfaces import ISavable


class Savable(ISavable):
    def __init__(self) -> None:
        self._id: int = None

    @property
    @override
    def id(self) -> int:
        return self._id
    
    @id.setter
    @override
    def id(self, value:int) -> None:
        if not isinstance(value, int):
            raise TypeError(type(value))
        self._id = value

    