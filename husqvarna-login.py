import sys
import pprint
from husqvarna import am

app_id = sys.argv[1]
username = input('username: ')
password = input('password: ')


am = am.AM_Auth(app_id=app_id)
data = am.login(username, password)
pprint.pprint(data)