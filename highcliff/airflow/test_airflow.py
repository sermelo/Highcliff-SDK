import unittest
from pprint import pprint

there_is_a_problem_with_airflow = True
user_denied_request_to_adjust_the_vent = True

capabilities = []


class TestAirflow(unittest.TestCase):

    def setUp(self):
        # use the SDK to monitor and manage air flow in the room
        from highcliff.airflow import MonitorAirflow, AuthorizeAirflowAdjustment, AdjustAirflow
        from highcliff.ai import AI

        # create an air vent sensor
        class AirVentSensor(MonitorAirflow):
            def behavior(self):
                # take a sensor reading

                if there_is_a_problem_with_airflow:
                    # make it known that the sensor found a problem with the air flow
                    super().adjustment_needed()

                    # log the problem
                else:
                    # do nothing if the sensor finds that the air flow is fine
                    # log the sensor readings
                    pass

        # create a UI that authorizes an adjustment to the air vent
        class AirVentUI(AuthorizeAirflowAdjustment):
            def behavior(self):
                if user_denied_request_to_adjust_the_vent:
                    super().authorization_failed()
                else:
                    pass

        # set up the initial state of the world for Highcliff
        # this is only necessary if you are running a local version of Highcliff
        the_world = {
            "monitor_airflow": False,
            "problem_with_airflow": False
        }

        # give Highcliff its goals
        goals = {
            "monitor_airflow": True,
            "problem_with_airflow": False
        }

        # instantiate the air vent sensor
        AirVentSensor(the_world_global_variable=the_world, capabilities_global_variable=capabilities)

        # instantiate the authorization UI
        AirVentUI(the_world_global_variable=the_world, capabilities_global_variable=capabilities)

        # run a local version of Highcliff
        ai_life_span_in_iterations = 1
        self.highcliff = AI(the_world_global_variable=the_world, capabilities_global_variable=capabilities,
                            goals=goals, life_span_in_iterations=ai_life_span_in_iterations)

        # output Highcliff's diary
        pprint(self.highcliff.diary())

    def test_maintain_comfortable_airflow(self):
        self.assertEqual(str(self.highcliff.diary()[0]['action_status']), "ActionStatus.SUCCESS")


if __name__ == '__main__':
    unittest.main()
