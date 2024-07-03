from abc import ABC, abstractmethod
from typing import List, Tuple, Any

from ..sql.interfaces import ISQLRequest


class IDatabaseExecutor(ABC):
    @abstractmethod
    def __init__(self, database_filename:str=None) -> None: pass

    @abstractmethod
    def start(self, sql_request:ISQLRequest) -> List[Tuple[Any]]: pass
    
