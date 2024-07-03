from abc import ABC, abstractmethod


class ISavable(ABC):
    @property
    @abstractmethod
    def id(self) -> int: pass
    
    @id.setter
    @abstractmethod
    def id(self, value) -> None: pass
    
class IUsernameKeySavable:
    @property
    @abstractmethod
    def username(self) -> str: pass

    @username.setter
    @abstractmethod
    def username(self, value) -> None: pass
    
class IJsonable:
    @abstractmethod
    def to_json(self) -> str: pass
    
    @abstractmethod
    def from_json(self, json_str:str) -> None: pass
    
