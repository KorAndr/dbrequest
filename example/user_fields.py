from dbrequest import AbstractField

from user import User


class UserUsernameField(AbstractField):
    def get_value_from_object(self, object:User) -> None:
        self._value = object.username 

    def set_value_to_object(self, object:User) -> None:
        object.username = self._value

class UserLastMessageField(AbstractField):
    def get_value_from_object(self, object:User) -> None:
        self._value = object.last_message 

    def set_value_to_object(self, object:User) -> None:
        object.last_message = self._value

        