from highcliff.actions.actions import AIaction


class MonitorAirflow(AIaction):
    def __init__(self, ai):
        super().__init__(ai)
        self.effects = {"is_airflow_adjustment_needed": True}
        self.preconditions = {}

    def behavior(self):
        # decide if adjustment is needed and update the world accordingly
        raise NotImplementedError

    def no_adjustment_needed(self):
        # this should be called by custom behavior if it determines that no adjustment is needed
        self.actual_effects["is_airflow_adjustment_needed"] = False


class AuthorizeAirflowAdjustment(AIaction):
    def __init__(self, ai):
        super().__init__(ai)
        self.effects = {"is_airflow_adjustment_authorized": True}
        self.preconditions = {"is_airflow_adjustment_needed": True}

    def behavior(self):
        # custom behavior must be specified by anyone implementing an AI action
        raise NotImplementedError

    def authorization_failed(self):
        # this should be called by custom behavior if it fails to authorize the adjustment
        self.effects["is_airflow_adjustment_authorized"] = False


class AdjustAirflow(AIaction):
    def __init__(self, ai):
        super().__init__(ai)
        self.effects = {"is_airflow_comfortable": True}
        self.preconditions = {"is_airflow_adjustment_authorized": True}

    def behavior(self):
        # custom behavior must be specified by anyone implementing an AI action
        raise NotImplementedError

    def adjustment_failed(self):
        # this should be called by custom behavior if it fails to complete the adjustment
        self.effects["is_airflow_comfortable"] = False
