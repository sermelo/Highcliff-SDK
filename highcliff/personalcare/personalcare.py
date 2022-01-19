from highcliff.actions.actions import AIaction


class AlertHairProblem(AIaction):
    effects = {"problem_with_hair": True}
    preconditions = {}

    def behavior(self):
        # custom behavior must be specified by anyone implementing an AI action
        raise NotImplementedError


class RequestHairAdjustment(AIaction):
    effects = {"hair_adjustment_requested": True}
    preconditions = {"problem_with_hair": True,  "alert_care_provider": "Hair needs to be flattened in the back"}

    def behavior(self):
        # custom behavior must be specified by anyone implementing an AI action
        raise NotImplementedError


class ConfirmHairAdjusted(AIaction):
    effects = {"problem_with_hair": False}
    preconditions = {"hair_adjustment_requested": True}

    def behavior(self):
        # custom behavior must be specified by anyone implementing an AI action
        raise NotImplementedError


class AlertEyeProblem(AIaction):
    effects = {"problem_with_eyes": False}
    preconditions = {}

    def behavior(self):
        # custom behavior must be specified by anyone implementing an AI action
        raise NotImplementedError


class RequestEyeCare(AIaction):
    effects = {"eye_care_requested": True}
    preconditions = {"problem_with_eyes": True, "alert_care_provider": "Eyes need attention"}

    def behavior(self):
        # custom behavior must be specified by anyone implementing an AI action
        raise NotImplementedError


class ConfirmEyeCareProvided(AIaction):
    effects = {"problem_with_eyes": False}
    preconditions = {"eye_care_request:": True}

    def behavior(self):
        # custom behavior must be specified by anyone implementing an AI action
        raise NotImplementedError
