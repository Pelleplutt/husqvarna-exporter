import configparser
import logging
import os
import pprint
import time
from prometheus_client import start_http_server, Gauge
from prometheus_client.core import GaugeMetricFamily, CounterMetricFamily, REGISTRY
from husqvarna import am, mower, auth

PORT = 9109
CONFIG_FILE = 'husqvarna-exporter.ini'

class UnifiCollector(object):
    def __init__(self, app_id, refresh_token):
        logging.info('Startup')

        self.am = am.AM(app_id=app_id, refresh_token=refresh_token)

    def setup_mower_metrics(self,  metrics):
        metrics['mower_battery_percent']            = GaugeMetricFamily('mower_battery_percent',            'Current battery level', labels=['serial', 'name', 'model'])
        metrics['mower_connected']                  = GaugeMetricFamily('mower_connected',                  'Connected status', labels=['serial', 'name', 'model'])
        metrics['mower_status_update_age_seconds']  = GaugeMetricFamily('mower_status_update_age_seconds',  'Seconds since last status update', labels=['serial', 'name', 'model'])
        metrics['mower_status_update_ts']           = GaugeMetricFamily('mower_status_update_ts',           'Unix ts of last status update', labels=['serial', 'name', 'model'])
        metrics['mower_activity']                   = GaugeMetricFamily('mower_activity',                   'Current mower activity', labels=['serial', 'name', 'model'])
        metrics['mower_errorcode']                  = GaugeMetricFamily('mower_errorcode',                  'Current errorcode', labels=['serial', 'name', 'model'])
        metrics['mower_errorcode_age_seconds']      = GaugeMetricFamily('mower_errorcode_age_seconds',      'Seconds since errorcode was set', labels=['serial', 'name', 'model'])
        metrics['mower_errorcode_ts']               = GaugeMetricFamily('mower_errorcode_ts',               'Unix ts of errorcode being set', labels=['serial', 'name', 'model'])
        metrics['mower_mode']                       = GaugeMetricFamily('mower_mode',                       'Current mowing mode', labels=['serial', 'name', 'model'])
        metrics['mower_state']                      = GaugeMetricFamily('mower_state',                      'Current mower state', labels=['serial', 'name', 'model'])
        metrics['mower_next_start_seconds']         = GaugeMetricFamily('mower_next_start_seconds',         'Planned number of seconds until next start', labels=['serial', 'name', 'model'])
        metrics['mower_next_start_ts']              = GaugeMetricFamily('mower_next_start_ts',              'Planned unix ts of next start', labels=['serial', 'name', 'model'])

    def add_mower_metrics(self,  metrics, mower):
        labels = [ str(mower.serial), mower.name, mower.model ]
        metrics['mower_battery_percent'].add_metric(labels, int(mower.battery_percent))
        metrics['mower_connected'].add_metric(labels, int(mower.connected))
        metrics['mower_status_update_age_seconds'].add_metric(labels, int(mower.status_update_age_seconds()))
        metrics['mower_status_update_ts'].add_metric(labels, int(mower.status_update_ts))
        metrics['mower_activity'].add_metric(labels, int(mower.activity_id))
        metrics['mower_errorcode'].add_metric(labels, int(mower.errorcode))
        metrics['mower_errorcode_age_seconds'].add_metric(labels, int(mower.errorcode_age_seconds()))
        metrics['mower_errorcode_ts'].add_metric(labels, int(mower.errorcode_ts))
        metrics['mower_mode'].add_metric(labels, int(mower.mode_id))
        metrics['mower_state'].add_metric(labels, int(mower.state_id))
        metrics['mower_next_start_seconds'].add_metric(labels, int(mower.next_start_seconds()))
        metrics['mower_next_start_ts'].add_metric(labels, int(mower.next_start_ts))

    def collect(self):
        logging.info('Collect')
        metrics = {}

        self.setup_mower_metrics(metrics)
        mowers = self.am.mowers()
        for mower in mowers:
            self.add_mower_metrics(metrics, mower)

        for key, val in metrics.items():
            yield val
        logging.info('Collect done')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    port = int(os.environ.get('AM_PORT', PORT))
    configfile = os.environ.get('AM_CONFIG', CONFIG_FILE)

    config = configparser.ConfigParser()
    config.read(configfile)

    app_id = config['auth']['app_id']
    if app_id is None or app_id == '':
        raise ValueError('Missing app_id, generate one at https://developer.1689.cloud')

    refresh_token = config['auth']['refresh_token']
    username = config['auth']['username']
    password = config['auth']['password']

    if refresh_token is None or refresh_token == '':
        if username is None or password is None or username == '' or password == '':
            raise ValueError('Missing refresh_token and username/password')
        rt_auth = auth.Auth(app_id)
        rt_data = rt_auth.Login(username, password)
        refresh_token = rt_data['refresh_token']
        logging.info('Logged in, fresh_token == {0}, add to config and remove usernane/password'.format(refresh_token))

    REGISTRY.register(UnifiCollector(app_id, refresh_token))
    start_http_server(port)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Break")

exit(0)



