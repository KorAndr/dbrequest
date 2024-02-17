from typing import Tuple

import dbrequest
from dbrequest import UniversalExecutor
from dbrequest.sql_requests import SQLFile

from user import User
from user_request import UserDBRequest


dbrequest.init(executor='SQLite', database_filename='database.db')


# Creating a table

request = SQLFile()
request.setArgs(filename='create_table.sql')

executor = UniversalExecutor()
executor.start(request)


# Demo user operations

user = User()
user.username = 'simple_user'

request = UserDBRequest()
request.save(user)

user: User = request.loadAll(User(), limit=1)[0]
print(user.id)

sameUser = User()
sameUser.id = user.id
request.load(sameUser)
print(sameUser.username)

user.lastMessage = 'Hello world!'
request.update(user)

admin = User()
admin.username = 'admin'
admin.lastMessage = 'Do you want to be banned?'

request.save(admin)

users: Tuple[User] = request.loadAll(User())
for user in users:
    print(f'The user who said "{user.lastMessage}" has been deleted')
    request.delete(user)

