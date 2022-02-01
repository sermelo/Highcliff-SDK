from highcliff.actions.actions import AIaction


class LogData(AIaction):
    effects = {"logged_data": ...}
    preconditions = {}

    def behavior(self):
        # custom behavior must be specified by anyone implementing an AI action
        raise NotImplementedError
