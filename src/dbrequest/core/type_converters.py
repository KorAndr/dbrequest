from abc import ABC, abstractmethod
from typing import Any, override
from datetime import datetime as Datetime, date as Date

import json 


class AbstractDBTypeConverter(ABC):
    def __init__(self) -> None:
        self._TYPE: type = None

    @property
    def TYPE(self) -> type:
        return self._TYPE

    @abstractmethod
    def to_database(self, value:Any) -> Any: pass

    @abstractmethod
    def from_database(self, value:Any) -> Any: pass

# Default converters

class BoolDBTypeConverter(AbstractDBTypeConverter):
    def __init__(self) -> None:
        self._TYPE: type = bool

    @override
    def to_database(self, value: bool) -> int:
        return int(value)

    @override
    def from_database(self, value: int) -> bool:
        return value == 1

class DatetimeDBTypeConverter(AbstractDBTypeConverter):
    def __init__(self) -> None:
        self._TYPE: type = Datetime

    @override
    def to_database(self, value: Datetime) -> int:
        timestamp = value.timestamp()
        if value.microsecond == 0:
            timestamp = int(timestamp)

        return timestamp

    @override
    def from_database(self, value: int) -> Datetime:
        if not isinstance(value, int):
            raise TypeError(type(value))
        if value is not None:
            return Datetime.fromtimestamp(value)

class DateDBTypeConverter(AbstractDBTypeConverter):
    def __init__(self) -> None:
        self._TYPE: type = Date

    @override
    def to_database(self, value: Date) -> int:
        return value.toordinal()

    @override
    def from_database(self, value: int) -> Date:
        if value is not None:
            return Date.fromordinal(value)

class AbstractJsonableDBTypeConverter(AbstractDBTypeConverter):
    @override
    def to_database(self, value: Any) -> str:
        return json.dumps(value, ensure_ascii=False, indent=2)

    @override
    def from_database(self, value: str) -> Any:
        if value is not None:
            return json.loads(value)
        
class ListDBTypeConverter(AbstractJsonableDBTypeConverter):
    def __init__(self) -> None:
        self._TYPE: type = list

class TupleDBTypeConverter(AbstractJsonableDBTypeConverter):
    def __init__(self) -> None:
        self._TYPE: type = tuple

class DictDBTypeConverter(AbstractJsonableDBTypeConverter):
    def __init__(self) -> None:
        self._TYPE: type = dict
