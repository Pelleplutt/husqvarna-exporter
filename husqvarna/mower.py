import time

class Mower:
    activities = [ "UNKNOWN", "NOT_APPLICABLE", "MOWING", "GOING_HOME", "CHARGING",  "LEAVING", "PARKED_IN_CS", "STOPPED_IN_GARDEN" ]
    states =  [ "UNKNOWN", "NOT_APPLICABLE", "PAUSED", "IN_OPERATION", "WAIT_UPDATING", "WAIT_POWER_UP", "RESTRICTED", "OFF", "STOPPED", "ERROR", "FATAL_ERROR", "ERROR_AT_POWER_UP" ]
    modes = [ "MAIN_AREA", "SECONDARY_AREA", "HOME", "DEMO", "UNKNOWN" ]

    def __init__(self, data):
        if data['type'] != 'mower':
            raise ValueError('Not a mower')

        self.id = data['id']
        self.set_battery(data['attributes']['battery'])
        self.set_calendar(data['attributes']['calendar'])
        self.set_metadata(data['attributes']['metadata'])
        self.set_mower(data['attributes']['mower'])
        self.set_planner(data['attributes']['planner'])
        self.set_system(data['attributes']['system'])

    def set_battery(self, data):
        self.battery_percent = data['batteryPercent']

    def set_calendar(self, data):
        # TODO When we see a use for it, add this body
        pass

    def set_metadata(self, data):
        self.connected = 1 if data['connected'] else 0
        self.status_update_ts = data['statusTimestamp'] / 1000

    def set_mower(self, data):
        self.activity = data['activity']
        self.activity_id = self.activities.index(self.activity)
        self.errorcode = data['errorCode']
        self.errorcode_ts = data['errorCodeTimestamp']
        self.mode = data['mode']
        self.mode_id = self.modes.index(self.mode)
        self.state = data['state']
        self.state_id = self.states.index(self.state)

    def set_planner(self, data):
        self.next_start_ts = data['nextStartTimestamp'] / 1000

    def set_system(self, data):
        self.model = data['model']
        self.name = data['name']
        self.serial = data['serialNumber']

    def status_update_age_seconds(self):
        if self.status_update_ts == 0:
            return 0

        return max(0, time.time() - self.status_update_ts)

    def errorcode_age_seconds(self):
        if self.errorcode_ts == 0:
            return 0

        return max(0, time.time() - self.errorcode_ts)

    def next_start_seconds(self):
        if self.next_start_ts == 0:
            return 0
        return max(0, self.next_start_ts - time.time())
        
