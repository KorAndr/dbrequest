from typing import Dict

from .interfaces import ISavable
from .idb_request import IDBRequest
from .fields import AbstractField


class AbstractUniversalDBRequest(IDBRequest):
    def __init__(self) -> None:
        self._REQUESTS: Dict[ISavable, IDBRequest] = {}

    def save(self, object:ISavable) -> None:
        self._get_storage_request(object).save(object)
    
    def load(self, object:ISavable) -> bool:
        return self._get_storage_request(object).load(object)
    
    def update(self, object:ISavable) -> None:
        self._get_storage_request(object).update(object)

    def delete(self, object:ISavable) -> None:
        self._get_storage_request(object).delete(object)
    
    def load_all(self, object_sample:ISavable, limit:int=None, reverse:bool=True, sort_field:AbstractField=None) -> list:
        return self._get_storage_request(object_sample).load_all(object_sample, limit, reverse, sort_field)
    
    def _get_storage_request(self, object:ISavable) -> IDBRequest:
        request: IDBRequest = None
        for object_type in self._REQUESTS.keys():
            if isinstance(object, object_type):
                request = self._REQUESTS[object_type]
                break
        else:
            raise TypeError(type(object))

        return request
    
    