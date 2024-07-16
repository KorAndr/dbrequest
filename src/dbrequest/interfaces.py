__all__ = [
    'ISQLRequest',
    'IDBTypeConverter',
    'IDatabaseExecutor',
    'IField',
    'IDBRequest',
    'SOURCE_TYPE',
    'DB_TYPE',
    'MODEL',
    'FIELD_TYPE',
]

from abc import ABC, abstractmethod
from typing import Tuple, Any, List, TypeVar, Generic
from types import MethodType


class ISQLRequest(ABC):
    @abstractmethod
    def set_args(self, *kwargs) -> None: pass

    @abstractmethod
    def get_request(self) -> Tuple[str, Tuple[Any]]: pass


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
    

class IDatabaseExecutor(ABC):
    @abstractmethod
    def __init__(self, database_filename: str | None = None) -> None: pass

    @abstractmethod
    def start(self, sql_request:ISQLRequest) -> List[Tuple[Any]]: pass

    @property
    @abstractmethod
    def supported_types(self) -> Tuple[type]: pass

    @property
    def default_type_converters(self) -> Tuple[IDBTypeConverter]: pass


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
    ) -> List[MODEL]:
        pass
    
