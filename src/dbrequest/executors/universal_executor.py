from typing import Any, List, Tuple, Dict

from ..config import config
from ..exceptions import FactoryError
from ..sql.interfaces import ISQLRequest
from ..core.interfaces import IDBTypeConverter
from .interfaces import IDatabaseExecutor
from .sqlite_executor import SQLiteExecutor


class UniversalExecutor(IDatabaseExecutor):
    def __init__(self, database_filename: str | None = None) -> None:
        self._EXECUTORS: Dict[config.Executor, IDatabaseExecutor] = {
            'sqlite': SQLiteExecutor(database_filename),
        }
        self._executor: IDatabaseExecutor = None
   
        if isinstance(config.EXECUTOR, IDatabaseExecutor):
            self._executor = config.EXECUTOR
        else:
            self._executor = self._EXECUTORS.get(config.EXECUTOR, None)
            if self._executor is None:
                raise FactoryError(f'Unknown executor "{config.EXECUTOR}"')

    def start(self, sql_request: ISQLRequest) -> List[Tuple[Any]]:
        return self._executor.start(sql_request)
    
    @property
    def supported_types(self) -> Tuple[type]:
        return self._executor.supported_types
    
    @property
    def default_type_converters(self) -> Tuple[IDBTypeConverter]:
        return self._executor.default_type_converters
    
    