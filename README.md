# dbrequest

dbrequest is a simple ORM library for easy database handling. The library is primarily designed for simple projects where complex SQL queries are not needed and SQLite can be used as the DBMS (although the library supports other DBMS as well).

The library provides an abstraction from the DBMS and allows working with storing, loading, modifying, and deleting model objects without explicit use of SQL.

[Read this in Russian](https://github.com/korandr/dbrequest/blob/main/README.ru.md) 

## Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Documentation](#documentation)
- [Feedback](#feedback)

## Installation

Installation from the PyPI repository:

```bash
$ pip install dbrequest
```

Installation from a GitHub repository (requires pip version 20 and above).

```bash
$ pip install git+https://github.com/korandr/dbrequest.git
```

Library import:

```python
import dbrequest
```

## Quick Start

For example, let's create a table `users`. Let's describe it in the `tables.sql` file:

```sql
create table IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    last_message TEXT DEFAULT NULL
);

```

Let's initialize the library:

```python
import dbrequest

dbrequest.init(init_script='tables.sql')
```

Next, define the model as `User` class:

```python
class User:
    def __init__(self, id: int | None = None, username: str | None = None) -> None:
        self.id = id
        self.username = username
        self.last_message: str | None = None
```

Now let's create `IField` objects for all saved fields of the class:

```python
from dbrequest import AutoField

id_field = AutoField('id', int, allowed_none=True)
username_field = AutoField('username', str)
last_message_field = AutoField('last_message', str, allowed_none=True)
```

Here the `dbrequest.AutoField` class is using, becouse the names of the fields and the corresponding columns in the table are the same.   
In more complex cases, you can use the `dbrequest.BaseField` class and explicitly specify the name matches.   

All that remains is to create an object for queries to the database:

```python
from dbrequest import BaseDBRequest

user_db_request = BaseDBRequest[User](
    model_type = User,
    table_name = 'users',
    fields = (
        id_field,
        username_field,
        last_message_field,
    ),
    key_fields = (
        id_field,
        username_field,
    ),
)
```
In the `fields` parameter we specify a tuple of all fields in the order in which the columns were created in the table.   
`key_fields` - fields with unique values ​​that can be used to find a specific object in the database.

The Generic parameter of the `BaseDBRequest` class is not required, but will help in typing the return of the `load_all` method.

Now you can conveniently perform operations with the `User` class and the database:

```python
user = User(username='simple_user')
user_db_request.save(user)

user = user_db_request.load_all(User(), limit=1, reverse=True)[0]
print(user.id)

same_user = User(id=user.id)
user_db_request.load(same_user)
print(same_user.username)

user.last_message = 'Hello world!'
user_db_request.update(user)

admin = User(username='admin')
admin.last_message = 'Do you want to be banned?'
user_db_request.save(admin)

users = user_db_request.load_all(User())
for user in users:
    print(f'The user who said "{user.last_message}" has been deleted')
    user_db_request.delete(user)
```

[See the code for this and other examples](https://github.com/korandr/dbrequest/tree/main/examples)

## Documentation

Basic documentation is contained in the library (docstring).   
Full documentation for the library is only [available in Russian](https://github.com/korandr/dbrequest/wiki).   
(Use Google Translate as a browser extension, as it works really well)

## Feedback

Developer: Andrey Korovyanskiy | [andrey.korovyansky@gmail.com](mailto:andrey.korovyansky@gmail.com)
