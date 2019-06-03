import os
import pprint
import configparser
from husqvarna import am

configfile = os.environ['AM_CONFIG']
config = configparser.ConfigParser()
config.read(configfile)

app_id = config['auth']['app_id']
refresh_token = config['auth']['refresh_token']

am = am.AM(app_id=app_id, refresh_token=refresh_token)
mowers = am.mowers()
