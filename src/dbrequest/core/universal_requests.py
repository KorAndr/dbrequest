__all__ = ['UniversalDBRequest']

from typing import Any
from types import MethodType

from ..exceptions import FactoryError
from ..interfaces import IDBRequest, IField, MODEL


class UniversalDBRequest(IDBRequest[Any]):
    def __init__(self, requests: tuple[IDBRequest]) -> None:
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
    
    def load_all(self, object_sample:MODEL, *, limit:int | None=None, reverse:bool=True, sort_by:IField | str | MethodType | None=None) -> list[MODEL]:
        return self._get_request(object_sample).load_all(object_sample, limit, reverse, sort_by)
    
    def _get_request(self, object:MODEL) -> IDBRequest[MODEL]:
        request: IDBRequest = None
        for request in self._requests:
            if isinstance(object, request.model_type):
                break
        else:
            raise FactoryError(f'Can not find request for object type {type(object)}')

        return request
    
    