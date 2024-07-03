from abc import ABC, abstractmethod
from typing import Tuple, Any


class ISQLRequest(ABC):
    @abstractmethod
    def set_args(self, *kwargs) -> None: pass

    @abstractmethod
    def get_request(self) -> Tuple[str, Tuple[Any]]: pass

