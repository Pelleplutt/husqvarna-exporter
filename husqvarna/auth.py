import requests
import logging
import pprint

class Auth:
    base_url = 'https://api.authentication.husqvarnagroup.dev/v1/'

    def __init__(self, app_id, refresh_token=None):
        self.app_id = app_id
        self.app_refresh_token = refresh_token
        self.app_token = None

    def headers(self):
        if self.app_token is None:
            self.refresh_token()

        return {
            'X-Api-Key': self.app_id,
            'Authorization': '{0} {1}'.format(self.app_token_type, self.app_token),
            'Authorization-Provider': self.app_token_provider
        }

    def refresh_token(self):
        rdata = { 
            'grant_type': 'refresh_token',
            'client_id': self.app_id,
            'refresh_token': self.app_refresh_token
        }

        logging.debug('POST oauth2/token refresh_token')
        r = requests.post(self.base_url + 'oauth2/token', data=rdata)
        data = r.json()

        if data.get('error') is not None:
            logging.error('Refresh token call failed: {} ({})'.format(data.get('error'), data.get('error_description')))
            raise RuntimeError(data.get('error_description'))
        else:
            try:
                self.app_token = data['access_token']
                self.app_token_type = data['token_type']
                self.app_token_provider = data['provider']
            except KeyError as err:
                logging.error('Cannot refresh token: {}'.format(err))
                logging.debug('No good return data when refreshing token {0}'.format(pprint.pformat(data)))
                raise RuntimeError('Cannot refresh token')

    def login(self, username, password):
        rdata = { 
            'grant_type': 'password',
            'client_id': self.app_id,
            'username': username,
            'password': password
        }

        logging.debug('POST oauth2/token password')
        r = requests.post(self.base_url + 'oauth2/token', data=rdata)
        data = r.json()

        return data
