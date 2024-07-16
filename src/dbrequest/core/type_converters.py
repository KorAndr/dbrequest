__all__ = [
    'BaseDBTypeConverter',
    'BaseJsonDBTypeConverter',
    'BoolDBTypeConverter',
    'ListDBTypeConverter',
    'TupleDBTypeConverter',
    'DictDBTypeConverter',
    'DatetimeDBTypeConverter',
    'DateDBTypeConverter',
    'TimedeltaSecondsDBTypeConverter',
]

from typing import override, Callable
from datetime import datetime as Datetime, date as Date, timedelta as Timedelta

import json 

from ..exceptions import TypeConverterError
from ..interfaces import IDBTypeConverter, SOURCE_TYPE, DB_TYPE


class BaseDBTypeConverter(IDBTypeConverter[SOURCE_TYPE, DB_TYPE]):
    def __init__(
            self,
            source_type: type[SOURCE_TYPE],
            db_type: type[DB_TYPE],
            *,
            to_database_func: Callable[[SOURCE_TYPE], DB_TYPE] = None,
            from_database_func: Callable[[DB_TYPE], SOURCE_TYPE] = None
        ) -> None:

        self._source_type = source_type
        self._db_type = db_type
        self._to_database_func = to_database_func if to_database_func else lambda value: self._db_type(value)
        self._from_database_func = from_database_func if from_database_func else lambda value: self._source_type(value)
    
    @property
    @override
    def source_type(self) -> type[SOURCE_TYPE]:
        return self._source_type

    @override
    def to_database(self, value: SOURCE_TYPE) -> DB_TYPE:
        if not isinstance(value, self._source_type):
            raise TypeConverterError(
                f'TypeConverter got unexpected source type {type(value)}. '
                f'Expected: {self._source_type}'
            )

        db_value = self._to_database_func(value)

        if not isinstance(db_value, self._db_type):
            raise TypeConverterError(
                f'`to_database_func` in TypeConverter `{self.__class__.__name__}` '
                f'returned unexpected type {type(db_value)}. ' 
                f'Expected: {self._db_type}.'
            )
        
        return db_value
    
    @override
    def from_database(self, value: DB_TYPE) -> SOURCE_TYPE:
        if not isinstance(value, self._db_type):
            raise TypeConverterError(
                f'TypeConverter got unexpected database type {type(value)}. ' 
                f'Expected: {self._db_type}'
            )
        
        source_value = self._from_database_func(value)

        if not isinstance(source_value, self._source_type):
            raise TypeConverterError(
                f'`from_database_func` in TypeConverter `{self.__class__.__name__}`'
                f'returned unexpected type {type(source_value)}. ' 
                f'Expected: {self._source_type}.'
            )
        
        return source_value


class BaseJsonDBTypeConverter(BaseDBTypeConverter[SOURCE_TYPE, str]):
    def __init__(self, source_type:type[SOURCE_TYPE], **json_kwargs:dict) -> None:
        to_database_func = lambda value: json.dumps(value, **json_kwargs)
        from_database_func = lambda value: source_type(json.loads(value))
        super().__init__(
            source_type = source_type,
            db_type = str,
            to_database_func = to_database_func,
            from_database_func = from_database_func
        )

# Default converters

class BoolDBTypeConverter(BaseDBTypeConverter[bool, int]):
    def __init__(self) -> None:
        super().__init__(source_type=bool, db_type=int)

class ListDBTypeConverter(BaseJsonDBTypeConverter[list]): 
    def __init__(self, **json_kwargs: dict) -> None:
        super().__init__(source_type=list, **json_kwargs)

class TupleDBTypeConverter(BaseJsonDBTypeConverter[tuple]):
    def __init__(self, **json_kwargs: dict) -> None:
        super().__init__(source_type=tuple, **json_kwargs)

class DictDBTypeConverter(BaseJsonDBTypeConverter[dict]):
    def __init__(self, **json_kwargs: dict) -> None:
        super().__init__(source_type=dict, **json_kwargs)

class DatetimeDBTypeConverter(BaseDBTypeConverter[Datetime, DB_TYPE]):
    def __init__(self, db_type:type[DB_TYPE]) -> None:
        to_database_func = lambda value: db_type(value.timestamp())
        from_database_func = lambda value: Datetime.fromtimestamp(value)
        super().__init__(
            source_type = Datetime,
            db_type = db_type,
            to_database_func = to_database_func,
            from_database_func = from_database_func
        )

class DateDBTypeConverter(BaseDBTypeConverter[Date, int]):
    def __init__(self) -> None:
        to_database_func = lambda value: value.toordinal()
        from_database_func = lambda value: Date.fromordinal(value)
        super().__init__(
            source_type = Date,
            db_type = int,
            to_database_func = to_database_func,
            from_database_func = from_database_func
        )

class TimedeltaSecondsDBTypeConverter(BaseDBTypeConverter[Timedelta, int]):
    # Возможно переписать на total_seconds
    def __init__(self) -> None:
        to_database_func = lambda value: value.seconds
        from_database_func = lambda value: Timedelta(seconds=value)
        super().__init__(
            source_type = Timedelta,
            db_type = int,
            to_database_func = to_database_func,
            from_database_func = from_database_func
        )
