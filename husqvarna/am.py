import logging
import requests
import time
from . import auth, mower

class AM:
    base_url = 'https://api.amc.husqvarna.dev/v1/'

    # As husqvarna limits the number of requests per month to 10000 we 
    # need to behave and not overstep that. Kling on to data for at 
    # least 10000 / 31 / 24 / 60 ~= 224s
    data_cache_thresold = 300

    def __init__(self, app_id, refresh_token):
        self.app_id = app_id
        self.auth = auth.Auth(app_id, refresh_token)
        self.cache = {}
        self.cache_age = {}

    def api_post_request(self, endpoint, **kwargs):
        data = {}
        for key, value in kwargs.items():
            data[key] = value

        r = requests.post(self.base_url + endpoint, data=data)
        return r.json()

    def api_get(self, endpoint):
        headers = self.auth.headers()
        logging.debug('GET {0}'.format(endpoint))

        r = requests.get(self.base_url + endpoint, headers=headers)

        if r.status_code == 401: # unauthorized
            self.auth.refresh_token()

            headers = self.auth.headers()
            logging.debug('GET {0} (retry)'.format(endpoint))
            r = requests.get(self.base_url + endpoint, headers=headers)
 
        return r.json()

    def get(self, endpoint):
        if self.cache_age.get(endpoint) is not None:
            if time.time() - self.cache_age[endpoint] < self.data_cache_thresold:
                return self.cache[endpoint]

        self.cache_age[endpoint] = time.time()
        self.cache[endpoint] = self.api_get(endpoint)
        return self.cache[endpoint]

    def mowers(self):
        data = self.get('mowers')
        mowers = []
        for m in data['data']:
            mowers.append(mower.Mower(m))
        return mowers


"""
{'data': [{'attributes': {'battery': {'batteryPercent': 47},
                          'calendar': {'tasks': [{'duration': 780,
                                                  'friday': True,
                                                  'monday': True,
                                                  'saturday': False,
                                                  'start': 360,
                                                  'sunday': False,
                                                  'thursday': False,
                                                  'tuesday': False,
                                                  'wednesday': True}]},
                          'metadata': {'connected': True,
                                       'statusTimestamp': 1559573810629},
                          'mower': {'activity': 'CHARGING',
                                    'errorCode': 0,
                                    'errorCodeTimestamp': 0,
                                    'mode': 'MAIN_AREA',
                                    'state': 'IN_OPERATION'},
                          'planner': {'nextStartTimestamp': 1559584619000,
                                      'override': {'action': 'MOWER_CHARGING'},
                                      'restrictedReason': 'NOT_APPLICABLE'},
                          'system': {'model': '315X',
                                     'name': 'Automower',
                                     'serialNumber': 18180xxxx}},
           'id': 'df92aec5-07ab-xxxx-xxxx-xxxxxxxxxxxx',
           'type': 'mower'}]}
"""

