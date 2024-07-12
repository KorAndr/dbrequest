__all__ = ['IDBTypeConverter', 'IDBRequest', 'SOURCE_TYPE', 'DB_TYPE', 'MODEL']

from abc import ABC, abstractmethod
from typing import List, TypeVar, Generic
from types import MethodType

from .fields import BaseField


SOURCE_TYPE = TypeVar('SOURCE_TYPE')
DB_TYPE = TypeVar('DB_TYPE')

class IDBTypeConverter(ABC, Generic[SOURCE_TYPE, DB_TYPE]):
    @property
    @abstractmethod
    def source_type(self) -> type[SOURCE_TYPE]: pass

    @abstractmethod
    def to_database(self, value:SOURCE_TYPE) -> DB_TYPE: pass

    @abstractmethod
    def from_database(self, value:DB_TYPE) -> SOURCE_TYPE: pass
    

MODEL = TypeVar('MODEL')

class IDBRequest(ABC, Generic[MODEL]):
    @property
    @abstractmethod
    def model_type(self) -> type[MODEL]: pass
    
    @abstractmethod
    def save(self, object:MODEL) -> None: pass

    @abstractmethod
    def load(self, object:MODEL) -> bool: pass
    
    @abstractmethod
    def update(self, object:MODEL) -> None: pass

    @abstractmethod
    def delete(self, object:MODEL) -> None: pass
    
    @abstractmethod
    def load_all(
        self,
        object_sample: MODEL,
        *,
        limit: int = None,
        reverse: bool = True,
        sort_by: BaseField | str | MethodType = None
    ) -> List[MODEL]:
        pass
    
