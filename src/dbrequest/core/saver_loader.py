from typing import Tuple, List, Any, Dict

from .fields import AbstractField
from .type_converters import *


class DatabaseSaverLoader:
    def __init__(self) -> None:
        self._FIELDS = None
        self._SUPPORTED_TYPES = (int, float, str, bytes, type(None))
        self._type_converters: List[AbstractDBTypeConverter] = [
            BoolDBTypeConverter(),
            DatetimeDBTypeConverter(),
            DateDBTypeConverter(),
            ListDBTypeConverter(),
            TupleDBTypeConverter(),
            DictDBTypeConverter()
        ]
    
    @property
    def FIELDS(self) -> Tuple[AbstractField]:
        return self._FIELDS
    
    @FIELDS.setter
    def FIELDS(self, value:Tuple[AbstractField]) -> None:
        if not isinstance(value, tuple):
            raise TypeError(type(value))
        self._FIELDS = value

    def set_type_converters(self, converters:Tuple[AbstractDBTypeConverter], replace:bool=False) -> None:
        if replace:
            self._type_converters = list(converters)
        else:
            self._type_converters += list(converters)

    def get_params_and_values(self, object:Any) -> Tuple[Tuple[str], Tuple[Any]]:
        params_list: List[str] = []
        values_list: List[Any] = []
        for field in self._FIELDS:
            field.get_value_from_object(object)
            params_list.append(field.NAME)
            values_list.append(self._get_field_value(field))
        
        return tuple(params_list), tuple(values_list)
    
    def set_values_to_object(self, object:Any, values:Tuple[Any]) -> None:
        if len(self._FIELDS) != len(values):
            raise ValueError(len(self._FIELDS), len(values))
        
        data: Dict[AbstractField, Any] = dict(zip(self._FIELDS, values))

        for field in data.keys():
            self._set_field_value(field, data[field])
            field.set_value_to_object(object)

    def _get_field_value(self, field:AbstractField) -> Any:
        value = field.value
        if not type(value) in self._SUPPORTED_TYPES:
            for converter in self._type_converters:
                if isinstance(value, converter.TYPE):
                    value = converter.to_database(value)
                    break
            else:
                raise TypeError(type(value))

        return value

    def _set_field_value(self, field:AbstractField, value) -> None:
        if value is None:
            if not field._ALLOWED_NONE:
                raise ValueError(f'Field "{field.NAME}" not allowed None type')
            field.value = None
        else:
            if not field.TYPE in self._SUPPORTED_TYPES:
                for converter in self._type_converters:
                    if converter.TYPE == field.TYPE:
                        value = converter.from_database(value)
                        break
                else:
                    raise TypeError(field.TYPE)
            
            field.value = value


