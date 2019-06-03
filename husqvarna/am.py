import requests
import pprint
from . import auth, mower

class AM:
    base_url = 'https://api.amc.husqvarna.dev/v1/'

    def __init__(self, app_id, refresh_token):
        self.app_id = app_id
        self.auth = auth.Auth(app_id, refresh_token)

    def api_post_request(self, endpoint, **kwargs):
        data = {}
        for key, value in kwargs.items():
            data[key] = value

        r = requests.post(self.base_url + endpoint, data=data)
        return r.json()

    def api_get(self, endpoint):
        headers = self.auth.headers()
        r = requests.get(self.base_url + endpoint, headers=headers)
        return r.json()

    def mowers(self):
        data = self.api_get('mowers')
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

