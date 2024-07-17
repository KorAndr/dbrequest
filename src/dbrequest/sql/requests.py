__all__ = ['SQLInsert', 'SQLSelect', 'SQLUpdate', 'SQLDelete', 'SQLCustom', 'SQLFile']

from typing import Any, override

from ..exceptions import SQLArgsError
from ..interfaces import ISQLRequest
from .properties import TableProp, ColumnsProp, ValuesProp, WhereProp, OrderByProp, LimitProp, All


class SQLInsert(ISQLRequest, TableProp, ColumnsProp, ValuesProp):
    def __init__(
            self,
            table: str,
            *,
            columns: tuple[str, ...],
            values: tuple[Any, ...],
            is_default: bool = False,
            is_replace: bool = False,
        ) -> None:
        TableProp.__init__(self, table)
        ColumnsProp.__init__(self, columns, allow_all=False)
        ValuesProp.__init__(self, values)
        self._is_default = is_default
        self._is_replace = is_replace

    def set_default_values(self) -> None:
        self._is_default = True

    def set_replace_mode(self) -> None:
        self._is_replace = True

    @override
    def get_request(self) -> tuple[str, tuple[Any]] | tuple[str]:
        request: tuple[str, tuple[Any]] | tuple[str]

        command = 'INSERT'
        if self._is_replace:
            command = 'REPLACE'
        
        request_str = f'{command} INTO {self._table} ({self._columns_str}) '

        if self._is_default:
            request_str += 'DEFAULT VALUES;'
            request = (request_str, )
        else:
            request_str += f'VALUES ({self._values_template});'

            request = (request_str, self.values)

        return request
    
class SQLSelect(ISQLRequest, TableProp, ColumnsProp, WhereProp, OrderByProp, LimitProp):
    def __init__(
            self,
            table: str,
            *,
            columns: tuple[str, ...] | All,
            where: str | None = None,
            is_distinct: bool | None = None,
            order_by: str | None = None,
            limit: int | str | None = None,
        ) -> None:
        TableProp.__init__(self, table)
        ColumnsProp.__init__(self, columns, allow_all=True)
        WhereProp.__init__(self, where)
        OrderByProp.__init__(self, order_by)
        LimitProp.__init__(self, limit)
        self._is_distinct = is_distinct 

    def set_distinct(self) -> None:
        self._is_distinct = True
        
    @override
    def get_request(self) -> tuple[str]:
        distinct = ''
        if self._is_distinct:
            distinct = ' DISTINCT'

        request_str = f'SELECT{distinct} {self._columns_str} FROM {self._table}{self._where_str}{self._order_str}{self._limit_str};'

        return (request_str, )

class SQLUpdate(ISQLRequest, TableProp, ColumnsProp, ValuesProp, WhereProp):
    def __init__(
            self,
            table: str,
            *,
            columns: tuple[str, ...],
            values: tuple[Any, ...],
            where: str | None = None,
        ) -> None:
        TableProp.__init__(self, table)
        ColumnsProp.__init__(self, columns, allow_all=False)
        ValuesProp.__init__(self, values)
        WhereProp.__init__(self, where)

    @override
    def get_request(self) -> tuple[str, tuple[Any]]:
        columns_and_values = ', '.join([f'{column} = ?' for column in self._columns])
        request_str = f'UPDATE {self._table} SET {columns_and_values}{self._where_str};'

        request = (request_str, self._values)

        return request

class SQLDelete(ISQLRequest, TableProp, WhereProp):
    def __init__(self, table:str, where:str | None = None) -> None:
        TableProp.__init__(self, table)
        WhereProp.__init__(self, where)

    @override
    def get_request(self) -> tuple[str]:
        request_str = f'DELETE FROM {self._table}{self._where_str};'

        return (request_str, )

class SQLCustom(ISQLRequest):
    def __init__(self, request_str:str) -> None:
        if request_str == '':
            raise SQLArgsError('`request_str` parameter can not be empty string.')

        self._request_str = request_str

    @override
    def get_request(self) -> tuple[str]:
        return (self._request_str, )

class SQLFile(ISQLRequest):
    def __init__(self, file_name:str) -> None:
        with open(file_name, 'r') as file:
            self._request_str = file.read()  

        if ';' not in self._request_str:
            raise SQLArgsError(f'`{file_name}` file doesn\'t contains complete SQL request because ";" not in file.')      

    @override                
    def get_request(self) -> tuple[str]:
        return (self._request_str, )

