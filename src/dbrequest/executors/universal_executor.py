from typing import Any, List, Tuple, Dict

from ..config import config
from ..sql.interfaces import ISQLRequest
from .interfaces import IDatabaseExecutor
from .sqlite_executor import SQLiteExecutor


class UniversalExecutor(IDatabaseExecutor):
    def __init__(self, database_filename:str=None) -> None:
        self._EXECUTORS: Dict[config.Executors, IDatabaseExecutor] = {
            config.Executors.SQLITE: SQLiteExecutor()
        }
   
        if isinstance(config.EXECUTOR, IDatabaseExecutor):
            self._executor = type(config.EXECUTOR)(database_filename)
        else:
            self._executor = type(self._EXECUTORS[config.EXECUTOR])(database_filename)

    def start(self, sql_request: ISQLRequest) -> List[Tuple[Any]]:
        return self._executor.start(sql_request)
    
    