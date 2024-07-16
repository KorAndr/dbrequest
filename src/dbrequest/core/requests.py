__all__ = ['BaseDBRequest']

from typing import Tuple, List, Any
from types import MethodType

from ..exceptions import SchemaError
from ..interfaces import IDatabaseExecutor, IDBTypeConverter, IDBRequest, IField, MODEL
from ..executors import UniversalExecutor
from ..sql.requests import SQLInsert, SQLSelect, SQLUpdate, SQLDelete
from .serizlizer import DBSerializer 


class BaseDBRequest(IDBRequest[MODEL]):
    def __init__(
            self,
            model_type: type[MODEL],
            table_name: str,
            fields: Tuple[IField],
            key_fields: Tuple[IField],
            *,
            executor: IDatabaseExecutor = UniversalExecutor(),
            type_converters: Tuple[IDBTypeConverter] = [],
            replace_type_converters: bool = False,
        ) -> None:
        
        self._model_type = model_type
        self._table_name = table_name
        self._executor = executor
        self._key_fields = key_fields

        if not replace_type_converters:
            type_converters = tuple(list(type_converters) + list(executor.default_type_converters))

        self._serializer = DBSerializer(
            fields = fields,
            supported_types = executor.supported_types,
            type_converters = type_converters,
        )

        if len(key_fields) == 0:
            raise SchemaError('`key_fields` must contents at least one element.')
        for key_field in key_fields:
            if key_field.name not in [field.name for field in fields]:
                raise SchemaError(f'Key field "{key_field.name}" not found in `fields` tuple.')

    @property
    def model_type(self) -> type[MODEL]:
        return self._model_type

    def save(self, object:MODEL) -> None:
        self._check_type(object)
        
        params, values = self._serializer.get_params_and_values(object)

        request = SQLInsert()
        request.set_args(table=self._table_name, columns=params, values=values)
        self._executor.start(request)
        
    def load(self, object:MODEL) -> bool:
        self._check_type(object)
        is_found = False
        condition = self._get_key_field_condition(object)
        
        request = SQLSelect()
        request.set_args(table=self._table_name, columns='*', where=condition, limit=1)
        response = self._executor.start(request)

        if len(response) > 0:
            is_found = True
            values: list = response[0]
            self._serializer.set_values_to_object(object, values)
        
        return is_found
        
    def update(self, object:MODEL) -> None:
        self._check_type(object)
        condition = self._get_key_field_condition(object)
        
        params, values = self._serializer.get_params_and_values(object)

        request = SQLUpdate()
        request.set_args(table=self._table_name, columns=params, values=values, where=condition)

        self._executor.start(request)
        
    def delete(self, object:MODEL) -> None:
        self._check_type(object)
        condition = self._get_key_field_condition(object)
        
        request = SQLDelete()
        request.set_args(table=self._table_name, where=condition)

        self._executor.start(request)

    def load_all(self, object_sample:MODEL, *, limit:int | None=None, reverse:bool=True, sort_by:IField | str | MethodType | None=None) -> List[MODEL]:
        self._check_type(object_sample)
        objects_list = []
        request = SQLSelect()

        order_by = None

        if sort_by is not None:
            sort_field_name = None
            if isinstance(sort_by, IField):
                sort_field_name = sort_by.name
            elif isinstance(sort_by, str):
                sort_field_name = sort_by
            elif isinstance(sort_by, MethodType):
                sort_field_name = sort_by.__name__
            else:
                raise TypeError(f'The `sort_by` parameter might be IField, str` or MetodType, not {type(sort_by)}.')

            if sort_field_name in [field.name for field in self._serializer.fields]:
                order_by = sort_field_name
            else:
                raise SchemaError(f'Unable to sort by field name "{sort_field_name}": field not exist.')
        else:
            if limit is not None:
                order_by = self._key_fields[0].name

        if order_by is not None:
            if reverse:
                order_by += ' DESC' 

        request.set_args(table=self._table_name, columns='*', order_by=order_by, limit=limit)
        table = self._executor.start(request)
        
        for row in table:
            object = type(object_sample)()
            self._serializer.set_values_to_object(object, row)
            objects_list.append(object)

        return objects_list

    def _check_type(self, object:Any) -> None:
        if not isinstance(object, self._model_type):
            raise TypeError(f'Got unexpected model object type {type(object)}. Expected: {MODEL}.')

    def _get_key_field_condition(self, object:MODEL) -> str:
        condition = ''
        for field in self._key_fields:
            try:
                field.get_value_from_object(object)
            except ValueError: pass
            else:
                if field.value is not None:
                    condition = f'{field.name} = \'{self._escape_sql(field.value)}\''
                    break
        else:
            raise SchemaError(f'Unable to compose SQL condition: all key fields are empty (None type).')

        return condition
    
    def _escape_sql(self, text:str) -> str:
        # Добавить экранирование
        return text
        