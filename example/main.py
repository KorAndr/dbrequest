from typing import Tuple

import dbrequest

from user import User
from user_request import UserDBRequest


dbrequest.init(init_script='create_table.sql')


user = User()
user.username = 'simple_user'

request = UserDBRequest()
request.save(user)

user: User = request.load_all(User(), limit=1)[0]
print(user.id)

same_user = User()
same_user.id = user.id
request.load(same_user)
print(same_user.username)

user.last_message = 'Hello world!'
request.update(user)

admin = User()
admin.username = 'admin'
admin.last_message = 'Do you want to be banned?'

request.save(admin)

users: Tuple[User] = request.load_all(User())
for user in users:
    print(f'The user who said "{user.last_message}" has been deleted')
    request.delete(user)

