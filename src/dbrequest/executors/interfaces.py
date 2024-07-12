from abc import ABC, abstractmethod
from typing import List, Tuple, Any

from ..sql.interfaces import ISQLRequest
from ..core.interfaces import IDBTypeConverter

class IDatabaseExecutor(ABC):
    @abstractmethod
    def __init__(self, database_filename: str = None | None) -> None: pass

    @abstractmethod
    def start(self, sql_request:ISQLRequest) -> List[Tuple[Any]]: pass

    @property
    @abstractmethod
    def supported_types(self) -> Tuple[type]: pass

    @property
    def default_type_converters(self) -> Tuple[IDBTypeConverter]: pass
    
