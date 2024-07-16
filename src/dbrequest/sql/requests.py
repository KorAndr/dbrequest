__all__ = ['SQLInsert', 'SQLSelect', 'SQLUpdate', 'SQLDelete', 'SQLCustom', 'SQLFile']

from typing import Tuple, Union, Any, override

from ..exceptions import SQLArgsError
from ..interfaces import ISQLRequest
from .properties import TableProp, ColumnsProp, ValuesProp, WhereProp, OrderByProp, LimitProp


ERROR_NONE = '`{obj}` parameter can not be None type.'
ERROR_EMPTY = '`{obj}` parameter can not be empty string.'

class SQLInsert(ISQLRequest, TableProp, ColumnsProp, ValuesProp):
    def __init__(self) -> None:
        TableProp.__init__(self)
        ColumnsProp.__init__(self, allow_all=False)
        ValuesProp.__init__(self)
        self._is_default = False
        self._is_replace = False

    def set_default_values(self) -> None:
        self._is_default = True

    def set_replace_mode(self) -> None:
        self._is_replace = True

    @override
    def set_args(
            self,
            table: str | None = None,
            columns: Tuple[str] | None = None,
            values: Tuple[Any] | None = None,
            is_default: bool | None = None,
            is_replace: bool | None = None
        ) -> None:

        if table is not None: self.table = table
        if self._table is None: raise SQLArgsError(ERROR_NONE.format(obj='table'))
        if columns is not None: self.columns = columns
        if self._columns is None: raise SQLArgsError(ERROR_NONE.format(obj='columns'))
        if values is not None: self.values = values
        if self._values is None: raise SQLArgsError(ERROR_NONE.format(obj='values'))
        if isinstance(is_default, bool): self._is_default = is_default
        if isinstance(is_replace, bool): self._is_replace = is_replace

    @override
    def get_request(self) -> Tuple[str, Tuple[Any]]:
        request: Tuple[str, str] = ()

        command = 'INSERT'
        if self._is_replace:
            command = 'REPLACE'
        
        request_str = f'{command} INTO {self._table} ({self._columns_str}) '

        if self._is_default:
            request_str += 'DEFAULT VALUES;'
            request = (request_str, )
        else:
            request_str += f'VALUES ({self._values_template});'

            request = (request_str, self._values)

        return request
    
class SQLSelect(ISQLRequest, TableProp, ColumnsProp, WhereProp, OrderByProp, LimitProp):
    def __init__(self) -> None:
        TableProp.__init__(self)
        ColumnsProp.__init__(self, allow_all=True)
        WhereProp.__init__(self)
        OrderByProp.__init__(self)
        LimitProp.__init__(self)
        self._is_distinct: bool = False 

    def set_distinct(self) -> None:
        self._is_distinct = True

    @override
    def set_args(
            self,
            table: str = None,
            columns: Union[Tuple[str], str] = None,
            where: str = None,
            is_distinct: bool = None,
            order_by: str = None,
            limit: Union[int, str] = None
        ) -> None:

        if table is not None: self.table = table
        if self._table is None: raise SQLArgsError(ERROR_NONE.format(obj='table'))
        if columns is not None: self.columns = columns
        if self._columns is None: raise SQLArgsError(ERROR_NONE.format(obj='columns'))
        if where is not None: self.where = where
        if isinstance(is_distinct, bool): self._is_distinct = is_distinct
        if order_by is not None: self.orderBy = order_by
        if limit is not None: self.limit = limit
        
    @override
    def get_request(self) -> Tuple[str]:
        distinct = ''
        if self._is_distinct:
            distinct = ' DISTINCT'

        request_str = f'SELECT{distinct} {self._columns_str} FROM {self._table}{self._where_str}{self._order_str}{self._limit_str};'

        return (request_str, )

class SQLUpdate(ISQLRequest, TableProp, ColumnsProp, ValuesProp, WhereProp):
    def __init__(self) -> None:
        TableProp.__init__(self)
        ColumnsProp.__init__(self, allow_all=False)
        ValuesProp.__init__(self)
        WhereProp.__init__(self)

    @override
    def set_args(self, table:str=None, columns:Tuple[str]=None, values:tuple=None, where:str=None) -> None:
        if table is not None: self.table = table
        if self._table is None: raise SQLArgsError(ERROR_NONE.format(obj='table'))
        if columns is not None: self.columns = columns
        if self._columns is None: raise SQLArgsError(ERROR_NONE.format(obj='columns'))
        if values is not None: self.values = values
        if self._values is None: raise SQLArgsError(ERROR_NONE.format(obj='values'))
        if where is not None: self.where = where

    @override
    def get_request(self) -> Tuple[str, Tuple[Any]]:
        request: Tuple[str, str] = ()

        columns_and_values = ', '.join([f'{column} = ?' for column in self._columns])
        request_str = f'UPDATE {self._table} SET {columns_and_values}{self._where_str};'

        request = (request_str, self._values)

        return request

class SQLDelete(ISQLRequest, TableProp, WhereProp):
    def __init__(self) -> None:
        TableProp.__init__(self)
        WhereProp.__init__(self)

    @override
    def set_args(self, table:str=None, where:str=None) -> None:
        if table is not None: self.table = table
        if self._table is None: raise SQLArgsError(ERROR_NONE.format(obj='table'))
        if where is not None: self.where = where

    @override
    def get_request(self) -> Tuple[str]:
        request_str = f'DELETE FROM {self._table}{self._where_str};'

        return (request_str, )

class SQLCustom(ISQLRequest):
    def __init__(self) -> None:
        self._request_str:str = None

    @override
    def set_args(self, request:str) -> None:
        if not isinstance(request, str):
            raise TypeError(request)
        if request == '':
            raise SQLArgsError(ERROR_EMPTY.format(obj='request'))
        self._request_str = request

    @override
    def get_request(self) -> Tuple[str]:
        return (self._request_str, )

class SQLFile(ISQLRequest):
    def __init__(self) -> None:
        self._request_str = None

    @override
    def set_args(self, filename:str) -> None:
        with open(filename, 'r') as file:
            self._request_str = file.read()

    @override                
    def get_request(self) -> Tuple[str]:
        return (self._request_str, )

