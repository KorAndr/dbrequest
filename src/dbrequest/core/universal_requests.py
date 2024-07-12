__all__ = ['UniversalDBRequest']

from typing import Any, List, Tuple
from types import MethodType

from .interfaces import IDBRequest, MODEL
from .fields import BaseField


class UniversalDBRequest(IDBRequest[Any]):
    def __init__(self, requests: Tuple[IDBRequest]) -> None:
        self._requests = requests

    @property
    def model_type(self) -> tuple[type]:
        return tuple([request.model_type for request in self._requests])

    def save(self, object:MODEL) -> None:
        self._get_request(object).save(object)
    
    def load(self, object:MODEL) -> bool:
        return self._get_request(object).load(object)
    
    def update(self, object:MODEL) -> None:
        self._get_request(object).update(object)

    def delete(self, object:MODEL) -> None:
        self._get_request(object).delete(object)
    
    def load_all(self, object_sample:MODEL, *, limit:int=None, reverse:bool=True, sort_by:BaseField | str | MethodType=None) -> List[MODEL]:
        return self._get_request(object_sample).load_all(object_sample, limit, reverse, sort_by)
    
    def _get_request(self, object:MODEL) -> IDBRequest[MODEL]:
        request: IDBRequest = None
        for request in self._requests:
            if isinstance(object, request.model_type):
                break
        else:
            raise ValueError(f'Can not find request for object type {type(object)}')

        return request
    
    