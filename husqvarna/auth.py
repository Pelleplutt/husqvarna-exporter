import requests
import logging
import pprint

class Auth:
    base_url = 'https://api.authentication.husqvarnagroup.dev/v1/'

    def __init__(self, app_id, username=None, password=None, refresh_token=None):
        self.app_id = app_id
        self.username = username
        self.password = password
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
        if self.app_refresh_token is None:
            data = self.login()
        else:
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
                if data.get('error') == 'invalid_grant':
                    self.app_refresh_token = None

                raise RuntimeError(data.get('error_description'))

        try:
            self.app_token = data['access_token']
            self.app_token_type = data['token_type']
            self.app_token_provider = data['provider']
        except KeyError as err:
            logging.error('Cannot refresh token: {0}'.format(err))
            logging.debug('No good return data when refreshing token {0}'.format(pprint.pformat(data)))
            raise RuntimeError('Cannot refresh token')

    def login(self):
        rdata = {
            'grant_type': 'password',
            'client_id': self.app_id,
            'username': self.username,
            'password': self.password
        }

        logging.debug('POST oauth2/token password')
        r = requests.post(self.base_url + 'oauth2/token', data=rdata)
        data = r.json()

        if data.get('error') is not None:
            logging.error('Login call failed: {} ({})'.format(data.get('error'), data.get('error_description')))

            raise RuntimeError(data.get('error_description'))

        self.app_refresh_token = data['refresh_token']
        logging.info('Logged in')

        return data
