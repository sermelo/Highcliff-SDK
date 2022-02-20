from highcliff.actions import AIaction

# TODO: change the instance variables of all specific actions


class MonitorBodyTemperature(AIaction):

    def __init__(self, infrastructure):
        super().__init__(infrastructure)
        self.effects = {"is_body_temperature_monitored": True, "is_room_temperature_comfortable": False}
        self.preconditions = {"is_body_temperature_monitored": False}

    def behavior(self):
        # custom behavior must be specified by anyone implementing an AI action
        raise NotImplementedError


class ChangeRoomTemperature(AIaction):
    effects = {"is_room_temperature_comfortable": True}
    preconditions = {"is_room_temperature_change_authorized": True}

    def behavior(self):
        # custom behavior must be specified by anyone implementing an AI action
        raise NotImplementedError


class AuthorizeRoomTemperatureChange(AIaction):
    effects = {"is_room_temperature_change_authorized": True}
    preconditions = {"is_room_temperature_comfortable": False}

    def behavior(self):
        # custom behavior must be specified by anyone implementing an AI action
        raise NotImplementedError


class AlertCareProvider(AIaction):
    effects = {"alert_care_provider": ...}
    preconditions = {}

    def behavior(self):
        # custom behavior must be specified by anyone implementing an AI action
        raise NotImplementedError


class LogBodyTemperatureData(AIaction):
    effects = {"log_body_temperature_data": ...}
    preconditions = {}

    def behavior(self):
        # custom behavior must be specified by anyone implementing an AI action
        raise NotImplementedError
