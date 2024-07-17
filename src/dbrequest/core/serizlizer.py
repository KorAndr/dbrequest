__all__ = ['DBSerializer']

from typing import Tuple, List, Any, Dict

from ..exceptions import InternalError
from ..interfaces import IDBTypeConverter, IField


class DBSerializer:
    '''
    Retrieve values from `IField` objects and prepare for writing to the database.
    Prepare values from the database for saving to `IField` objects.
    Convert unsupported values using `IDBTypeConverter` objects.
    '''
    def __init__(
            self,
            fields: Tuple[IField],
            supported_types: Tuple[type],
            type_converters: Tuple[IDBTypeConverter],
        ) -> None:
        '''
        Class constructor.

        Positional arguments:
        :param fields: `IField` objects in the order in which parameters are declared in the database
        :param supported_types: types supported by a specific database
        :param type_converters: `IDBTypeConverter` objects for converting unsupported types
        '''
        self._fields = fields
        self._supported_types = supported_types
        self._type_converters = type_converters
    
    @property
    def fields(self) -> Tuple[IField]:
        '''Return current `IField` objects.'''
        return self._fields

    def get_params_and_values(self, object:Any) -> Tuple[Tuple[str], Tuple[Any]]:
        '''Return prepared parameters and values tuples from input object for writing to the database.'''
        params_list: List[str] = [field.name for field in self._fields]
        values_list: List[Any] = []

        for field in self._fields:
            field.get_value_from_object(object)
            value = self._get_field_value(field)
            values_list.append(value)
        
        return tuple(params_list), tuple(values_list)
    
    def set_values_to_object(self, object:Any, values:Tuple[Any]) -> None:
        '''Prepare and set values from database to object.'''
        if len(self._fields) != len(values):
            raise InternalError(f'Number of values ({len(self._fields)}) not equal to number of fields ({len(values)}).')
        
        data: Dict[IField, Any] = dict(zip(self._fields, values))

        for field in data.keys():
            self._set_field_value(field, data[field])
            field.set_value_to_object(object)

    def _get_field_value(self, field:IField) -> Any:
        '''Retrieve value from the `IField` object and convert if necessary.'''
        value = field.value
        if not type(value) in self._supported_types:
            for converter in self._type_converters:
                if issubclass(field.type, converter.source_type):
                    value = converter.to_database(value)
                    break
            else:
                raise TypeError(
                    f'Object type {type(value)} not supported by current database. '
                    'You can set a custom `DBTypeConverter` for this type.'
                )

        return value

    def _set_field_value(self, field:IField, value:Any) -> None:
        '''Set database value to the `IField` object and convert if necessary.'''
        if not field.type in self._supported_types:
            for converter in self._type_converters:
                if issubclass(converter.source_type, field.type):
                    value = converter.from_database(value)
                    break
            else:
                raise TypeError(
                    f'Can not convert value type {type(value)} '
                    f'to required field type {field.type}. '
                    'You can set a custom `DBTypeConverter` for this type.'
                )
        
        field.value = value


