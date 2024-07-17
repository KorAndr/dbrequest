__all__ = [
    'ISQLRequest',
    'ITypeConverter',
    'IDatabaseExecutor',
    'IField',
    'IDBRequest',
    'SOURCE_TYPE',
    'DB_TYPE',
    'MODEL',
    'FIELD_TYPE',
]

from abc import ABC, abstractmethod
from typing import Any, TypeVar, Generic
from types import MethodType


class ISQLRequest(ABC):
    @abstractmethod
    def get_request(self) -> tuple[str, tuple[Any]] | tuple[str]: pass


SOURCE_TYPE = TypeVar('SOURCE_TYPE')
DB_TYPE = TypeVar('DB_TYPE')

class ITypeConverter(ABC, Generic[SOURCE_TYPE, DB_TYPE]):
    @property
    @abstractmethod
    def source_type(self) -> type[SOURCE_TYPE]: pass

    @abstractmethod
    def to_database(self, value:SOURCE_TYPE) -> DB_TYPE: pass

    @abstractmethod
    def from_database(self, value:DB_TYPE) -> SOURCE_TYPE: pass
    

class IDatabaseExecutor(ABC):
    @abstractmethod
    def __init__(self, database_filename: str | None = None) -> None: pass

    @abstractmethod
    def start(self, sql_request:ISQLRequest) -> list[tuple[Any]]: pass

    @property
    @abstractmethod
    def supported_types(self) -> tuple[type, ...]: pass

    @property
    @abstractmethod
    def default_type_converters(self) -> tuple[ITypeConverter, ...]: pass


MODEL = TypeVar('MODEL')
FIELD_TYPE = TypeVar('FIELD_TYPE')

class IField(ABC, Generic[MODEL, FIELD_TYPE]):
    @property
    @abstractmethod
    def name(self) -> str: pass
    
    @property
    @abstractmethod
    def type(self) -> type[FIELD_TYPE]: pass
    
    @property
    @abstractmethod
    def value(self) -> FIELD_TYPE: pass

    @value.setter
    @abstractmethod
    def value(self, value:FIELD_TYPE) -> None: pass

    @abstractmethod
    def get_value_from_object(self, object:MODEL) -> None: pass

    @abstractmethod
    def set_value_to_object(self, object:MODEL) -> None: pass


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
        limit: int | None = None,
        reverse: bool = True,
        sort_by: IField | str | MethodType | None = None
    ) -> list[MODEL]:
        pass
    
