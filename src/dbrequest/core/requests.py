from typing import Tuple

from ..executors.universal_executor import UniversalExecutor
from ..executors.interfaces import IDatabaseExecutor
from ..sql.requests import SQLInsert, SQLSelect, SQLUpdate, SQLDelete
from .saver_loader import DatabaseSaverLoader
from .interfaces import ISavable, IUsernameKeySavable
from .idb_request import IDBRequest
from .fields import AbstractField


class AbstractDBRequest(IDBRequest):
    def __init__(self) -> None:
        self._TABLE_NAME: str = None
        self._saver_loader = DatabaseSaverLoader()
        self._executor: IDatabaseExecutor = UniversalExecutor()

    def save(self, object:ISavable) -> None:
        if not isinstance(object, ISavable):
            raise TypeError(type(object))
        
        params, values = self._saver_loader.get_params_and_values(object)

        request = SQLInsert()
        request.set_args(table=self._TABLE_NAME, columns=params, values=values)
        self._executor.start(request)
        
    def load(self, object:ISavable) -> bool:
        if not isinstance(object, ISavable):
            raise TypeError(type(object))
        
        is_found = False
        condition = ''

        if object.id is not None:
            condition = f'id = {object.id}'
        else:
            if isinstance(object, IUsernameKeySavable) and object.username is not None:
                condition = f'username = \'{object.username}\''
            else:
                raise ValueError(object.id)
        
        request = SQLSelect()
        request.set_args(table=self._TABLE_NAME, columns='*', where=condition, limit=1)
        response = self._executor.start(request)

        if len(response) > 0:
            is_found = True
            values: list = response[0]
            self._saver_loader.set_values_to_object(object, values)
        
        return is_found
        
    def update(self, object:ISavable) -> None:
        if not isinstance(object, ISavable):
            raise TypeError(type(object))
        if object.id is None:
            raise ValueError(object.id)
        
        params, values = self._saver_loader.get_params_and_values(object)

        request = SQLUpdate()
        request.set_args(table=self._TABLE_NAME, columns=params, values=values, where=f'id = {object.id}')

        self._executor.start(request)
        
    def delete(self, object:ISavable) -> None:
        if not isinstance(object, ISavable):
            raise TypeError(type(object))
        if object.id is None:
            raise ValueError(object.id)
        
        request = SQLDelete()
        request.set_args(table=self._TABLE_NAME, where=f'id = {object.id}')

        self._executor.start(request)

    def load_all(self, object_sample:ISavable, limit:int=None, reverse:bool=True, sort_field:AbstractField=None) -> list:
        if not isinstance(object_sample, ISavable):
            raise TypeError(type(object_sample))

        objects_list = []
        request = SQLSelect()

        order_by = None

        if sort_field is not None:
            for field in self._FIELDS:
                if type(field) == sort_field:
                    order_by = field.NAME
                    break
            else:
                raise ValueError(sort_field)
        else:
            if limit is not None:
                order_by = 'id'

        if order_by is not None:
            if reverse:
                order_by += ' DESC' 

        request.set_args(table=self._TABLE_NAME, columns='*', order_by=order_by, limit=limit)
        table = self._executor.start(request)
        
        for row in table:
            object = type(object_sample)()
            self._saver_loader.set_values_to_object(object, row)
            objects_list.append(object)

        return objects_list

    @property
    def _FIELDS(self) -> Tuple[AbstractField]:
        return self._saver_loader.FIELDS
    
    @_FIELDS.setter
    def _FIELDS(self, value:Tuple[AbstractField]) -> None:
        self._saver_loader.FIELDS = value

        