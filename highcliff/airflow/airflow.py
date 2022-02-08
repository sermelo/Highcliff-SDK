from highcliff.actions.actions import AIaction


class MonitorAirflow(AIaction):
    effects = {"monitor_airflow": True, "problem_with_airflow": False}
    preconditions = {"monitor_airflow": False}

    def behavior(self):
        # decide if medication is needed and update the world accordingly
        raise NotImplementedError

    def adjustment_needed(self):
        # this should be called by custom behavior if it determines that adjustment is needed
        self.effects["problem_with_airflow"] = True


class AuthorizeAirflowAdjustment(AIaction):
    effects = {"airflow_adjustment_authorized": True}
    preconditions = {"problem_with_airflow": True}

    def behavior(self):
        # custom behavior must be specified by anyone implementing an AI action
        raise NotImplementedError

    def authorization_failed(self):
        # this should be by custom behavior if it fails to confirm that the proper maintenance was given
        self.effects["airflow_adjustment_authorized"] = False
        self.effects["problem_with_airflow"] = True


class AdjustAirflow(AIaction):
    effects = {"problem_with_airflow": False}
    preconditions = {"airflow_adjustment_authorized": True}

    def behavior(self):
        # custom behavior must be specified by anyone implementing an AI action
        raise NotImplementedError

    def __adjustment_failed(self):
        # this should be called by custom behavior if it fails to complete the adjustment
        self.effects["problems_with_airflow"] = True
