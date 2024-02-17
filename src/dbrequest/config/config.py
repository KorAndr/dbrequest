from enum import Enum
from typing import Union

class Executors(Enum):
    SQLITE = 'SQLite'

DATABASE_FILENAME: str = None
EXECUTOR: Executors = None
LOGGER_NAME: str = 'database'

def init(
        executor: Union[str, Executors] = Executors.SQLITE,
        database_filename: str = None,
        logger_name: str = None
    ) -> None:

    global DATABASE_FILENAME
    global EXECUTOR
    global LOGGER_NAME

    if isinstance(executor, str):
        executor = Executors(executor)
    EXECUTOR = executor
    
    if database_filename is not None: DATABASE_FILENAME = database_filename
    if logger_name is not None: LOGGER_NAME = logger_name

