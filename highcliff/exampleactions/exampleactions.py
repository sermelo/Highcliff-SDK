from highcliff.actions import AIaction


class MonitorBodyTemperature(AIaction):

    def __init__(self, infrastructure):
        super().__init__(infrastructure)
        self.effects = {"is_body_temperature_monitored": True, "is_room_temperature_comfortable": False}
        self.preconditions = {"is_body_temperature_monitored": False}

    def behavior(self):
        # custom behavior must be specified by anyone implementing an AI action
        raise NotImplementedError


class ChangeRoomTemperature(AIaction):

    def __init__(self, infrastructure):
        super().__init__(infrastructure)
        self.effects = {"is_room_temperature_comfortable": True}
        self.preconditions = {"is_room_temperature_change_authorized": True}

    def behavior(self):
        # custom behavior must be specified by anyone implementing an AI action
        raise NotImplementedError


class AuthorizeRoomTemperatureChange(AIaction):

    def __init__(self, infrastructure):
        super().__init__(infrastructure)
        self.effects = {"is_room_temperature_change_authorized": True}
        self.preconditions = {"is_room_temperature_comfortable": False}

    def behavior(self):
        # custom behavior must be specified by anyone implementing an AI action
        raise NotImplementedError
