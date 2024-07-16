__all__ = ['init']

from typing import Literal, TypeAlias

from ..exceptions import ConfigError
from ..executors.interfaces import IDatabaseExecutor


Executor: TypeAlias = Literal['sqlite', ]

DATABASE_FILENAME: str = 'database.db'
EXECUTOR: Executor | IDatabaseExecutor = 'sqlite'
LOGGER_NAME: str = 'database'

def init(
        *,
        database_filename: str = 'database.db',
        executor: Executor | IDatabaseExecutor = 'sqlite',
        logger_name: str = 'database',
        init_script: str = None,
    ) -> None:

    global DATABASE_FILENAME
    global EXECUTOR
    global LOGGER_NAME

    if not isinstance(database_filename, str): raise TypeError(type(database_filename))
    if not isinstance(executor, (str, IDatabaseExecutor)): raise TypeError(executor)
    if not isinstance(logger_name, str): raise TypeError(type(logger_name))
    if not isinstance(init_script, (str, type(None))): raise TypeError(type(init_script))

    if database_filename == '': raise ConfigError(database_filename)
    if logger_name == '': raise ConfigError(logger_name)
    if init_script is not None and init_script == '': raise ConfigError(init_script)

    EXECUTOR = executor.lower() if isinstance(executor, str) else executor
    DATABASE_FILENAME = database_filename
    LOGGER_NAME = logger_name

    if init_script is not None:
        from ..executors.universal_executor import UniversalExecutor
        from ..sql_requests import SQLFile

        request = SQLFile()
        request.set_args(filename=init_script)

        executor = UniversalExecutor()
        executor.start(request)

