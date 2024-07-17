__all__ = ['BaseField', 'AutoField']

from typing import Callable

from ..exceptions import InternalError
from ..interfaces import IField, MODEL, FIELD_TYPE


class BaseField(IField[MODEL, FIELD_TYPE]):
    def __init__(
            self,
            name: str,
            field_type: type[FIELD_TYPE],
            *,
            getter: Callable[[MODEL], FIELD_TYPE],
            setter: Callable[[MODEL, FIELD_TYPE | None], None],
            allowed_none: bool = False,
        ) -> None:

        self._name = name
        self._type = field_type
        self._allowed_none = allowed_none
        self._getter = getter
        self._setter = setter
        self._value: FIELD_TYPE | None = None

    @property
    def name(self) -> str:
        return self._name
    
    @property
    def type(self) -> type[FIELD_TYPE]:
        return self._type
    
    @property
    def value(self) -> FIELD_TYPE | None:
        if self._value is None and not self._allowed_none:
            raise InternalError(self._value)
        return self._value

    @value.setter
    def value(self, value:FIELD_TYPE) -> None:
        if not isinstance(value, self._type):
            if not value is None: 
                raise TypeError(f'Field {self.name} got unexpected value type {type(value)}. Expected: {self._type}')
            elif not self._allowed_none:                
                raise TypeError(f'Field {self.name} not allowed None type.')

        self._value = value

    def get_value_from_object(self, object:MODEL) -> None: 
        self.value = self._getter(object)

    def set_value_to_object(self, object:MODEL) -> None:
        self._setter(object, self.value)


class AutoField(BaseField[MODEL, FIELD_TYPE]):
    def __init__(self, name: str, field_type: type[FIELD_TYPE], *, allowed_none: bool = False) -> None:
        getter = lambda obj: getattr(obj, name)
        setter = lambda obj, value: setattr(obj, name, value)

        super().__init__(name, field_type, getter=getter, setter=setter, allowed_none=allowed_none)

