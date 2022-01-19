from highcliff.actions.actions import AIaction


class AlertCareProvider(AIaction):
    effects = {"alert_care_provider": ...}
    preconditions = {}

    def behavior(self):
        # custom behavior must be specified by anyone implementing an AI action
        raise NotImplementedError
