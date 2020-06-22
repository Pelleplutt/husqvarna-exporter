import sys
import pprint
from husqvarna import auth

app_id = sys.argv[1]
username = input('username: ')
password = input('password: ')


am = auth.Auth(app_id=app_id)
data = am.login(username, password)
pprint.pprint(data)
