from typing import Any, Literal, TypeAlias

from ..exceptions import SQLArgsError


EMPTY_STRING_ERROR = '`{param}` parameter can not be empty string.'
All: TypeAlias = Literal['*', 'all']

class TableProp:
    def __init__(self, table:str) -> None:
        if table == '': raise SQLArgsError(EMPTY_STRING_ERROR.format(param='table'))
        self._table = table

    @property
    def table(self) -> str:
        return self._table

class ColumnsProp:
    def __init__(self, columns:tuple[str, ...] | All, *, allow_all:bool) -> None:
        self.__allow_all = allow_all
        self._columns = columns
        
        if columns in ['*', 'all'] and not allow_all:
            raise SQLArgsError('Set `allow_all = True` for use `columns = "all"`')
        if columns == 'all': self._columns = '*'

        if isinstance(columns, tuple):
            for column in columns:
                if column == '':
                    raise SQLArgsError(f'Every column in `columns` parameter can not be empty string. Current columns: {columns}.')

    @property
    def columns(self) -> tuple[str, ...] | All:
        return self._columns

    @property
    def _columns_str(self) -> str:
        return ', '.join(self._columns)

class ValuesProp:
    def __init__(self, values: tuple[Any, ...], *, supported_types: tuple[type] | None = None) -> None:
        self._values = values
        
        if supported_types:
            for value in values:
                if not type(value) in supported_types:
                    raise SQLArgsError(f'Type {type(value)} not supported by current database: {supported_types}.')

    @property
    def values(self) -> tuple[Any, ...]:
        return self._values

    @property
    def _values_template(self) -> str:
        return ', '.join(['?'] * len(self._values))

class WhereProp:
    def __init__(self, where: str | None) -> None:
        if where == '': raise SQLArgsError(EMPTY_STRING_ERROR.format(param='where'))
        self._where = where

    @property
    def where(self) -> str | None:
        return self._where

    @property
    def _where_str(self) -> str:
        where_str = ''
        if self._where is not None:
            where_str = f' WHERE {self._where}'
        return where_str

class OrderByProp:
    def __init__(self, order_by: str | None) -> None:
        if order_by == '': raise SQLArgsError(EMPTY_STRING_ERROR.format(param='order_by'))
        self._order_by = order_by

    @property
    def order_by(self) -> str | None:
        return self._order_by

    @property
    def _order_str(self) -> str:
        order_str = ''
        if self._order_by is not None:
            order_str = f' ORDER BY {self._order_by}'
        return order_str

class LimitProp:
    def __init__(self, limit:int | str | None) -> None:
        if isinstance(limit, int):
            if limit <= 0:
                raise SQLArgsError(f'`limit` parameter must be positive int. Current limit: {limit}.')
        
        self._limit = limit

    @property
    def limit(self) -> int | str | None:
        return self._limit

    @property
    def _limit_str(self) -> str:
        limit_str = ''
        if self._limit is not None:
            limit_str = f' LIMIT {self._limit}'

        return limit_str
