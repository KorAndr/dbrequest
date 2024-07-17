from typing import Any

from ..exceptions import SQLArgsError


class TableProp:
    def __init__(self) -> None:
        self._table: str = None

    @property
    def table(self) -> str:
        return self._table
    
    @table.setter
    def table(self, value:str) -> None:
        if not isinstance(value, str): raise TypeError(type(value))
        if value == '': raise SQLArgsError(value)
        self._table = value

class ColumnsProp:
    def __init__(self, allow_all:bool) -> None:
        if not isinstance(allow_all, bool): raise TypeError(type(allow_all))
        self.__allow_all = allow_all
        self._columns: tuple[str] = ()

    @property
    def columns(self) -> tuple | str:
        return self._columns
    
    @columns.setter
    def columns(self, value:tuple | str) -> None:
        if isinstance(value, tuple):
            if len(value) == 0:
                raise SQLArgsError(value)
            for column in value:
                if not isinstance(column, str):
                    raise SQLArgsError(type(column))
                if column == '':
                    raise SQLArgsError(column)
        elif isinstance(value, str) and self.__allow_all:
            if value != '*':
                raise SQLArgsError(value)
        else:
            raise TypeError(type(value))
        
        self._columns = value

    @property
    def _columns_str(self) -> str:
        return ', '.join(self._columns)

class ValuesProp:
    def __init__(self) -> None:
        self._values: tuple[Any] = None
        self._SUPPORTED_TYPES = (int, float, str, bytes, type(None))

    @property
    def values(self) -> tuple[Any]:
        return self._values
    
    @values.setter
    def values(self, value:tuple[Any]) -> None:
        if not isinstance(value, tuple):
            raise TypeError(type(value))
        if len(value) == 0:
            raise SQLArgsError(value)
        for v in value:
            if not type(v) in self._SUPPORTED_TYPES:
                raise TypeError(f'Type {type(v)} not in supported types: {self._SUPPORTED_TYPES}')
            
        self._values = value

    @property
    def _values_template(self) -> str:
        return ', '.join(['?'] * len(self._values))

class WhereProp:
    def __init__(self) -> None:
        self._where:str = None

    @property
    def where(self) -> str:
        return self._where
    
    @where.setter
    def where(self, value:str) -> None:
        if not isinstance(value, str):
            raise TypeError(type(value))
        if value == '':
            raise SQLArgsError(value)
        self._where = value

    @property
    def _where_str(self) -> str:
        where_str = ''
        if self._where is not None:
            where_str = f' WHERE {self._where}'
        return where_str

class OrderByProp:
    def __init__(self) -> None:
        self._order_by: str = None

    @property
    def order_by(self) -> str:
        return self._order_by
    
    @order_by.setter
    def order_by(self, value:str) -> None:
        if not isinstance(value, str):
            raise TypeError(type(value))
        if value == '':
            raise SQLArgsError(value)
        self._order_by = value

    @property
    def _order_str(self) -> str:
        order_str = ''
        if self._order_by is not None:
            order_str = f' ORDER BY {self._order_by}'
        return order_str

class LimitProp:
    def __init__(self) -> None:
        self._limit: int | str = None

    @property
    def limit(self) -> int | str:
        return self._limit
    
    @limit.setter
    def limit(self, value:int | str) -> None:
        if isinstance(value, int):
            if value <= 0:
                raise SQLArgsError(value)
        elif not isinstance(value, str):
            raise TypeError(type(value))
        self._limit = value

    @property
    def _limit_str(self) -> str:
        limit_str = ''
        if self._limit is not None:
            limit_str = f' LIMIT {self._limit}'

        return limit_str
