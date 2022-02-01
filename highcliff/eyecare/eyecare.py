from highcliff.actions.actions import AIaction


class MonitorEyes(AIaction):
    effects = {"problem_with_eyes": True}
    preconditions = {}

    def behavior(self):
        # custom behavior must be specified by anyone implementing an AI action
        raise NotImplementedError


class RequestEyeCare(AIaction):
    effects = {"eye_care_requested": True}
    preconditions = {"problem_with_eyes": True}

    def behavior(self):
        # custom behavior must be specified by anyone implementing an AI action
        raise NotImplementedError


class ConfirmEyeCare(AIaction):
    effects = {"problem_with_eyes": False}
    preconditions = {"eye_care_requested": True}

    def behavior(self):
        # custom behavior must be specified by anyone implementing an AI action
        raise NotImplementedError
