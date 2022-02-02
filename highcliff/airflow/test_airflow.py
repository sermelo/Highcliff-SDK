import unittest
from pprint import pprint

there_is_a_problem_with_airflow = True

the_world = {}
capabilities = []


class TestAirflow(unittest.TestCase):

    def setUp(self):
        from highcliff.airflow import MonitorAirflow, AuthorizeAirflowAdjustment, AdjustAirflow
        from highcliff.ai import AI, goals

        class AcmeAirflowMonitor(MonitorAirflow):
            def behavior(self):
                if there_is_a_problem_with_airflow:
                    super().adjustment_needed()
                else:
                    pass

        AcmeAirflowMonitor(the_world_global_variable=the_world, capabilities_global_variable=capabilities)

        # run a local version of Highcliff
        ai_life_span_in_iterations = 1
        self.highcliff = AI(the_world_global_variable=the_world, capabilities_global_variable=capabilities,
                            goals=goals, life_span_in_iterations=ai_life_span_in_iterations)

        # output the diary
        pprint(self.highcliff.diary())

    def test_maintain_comfortable_airflow(self):
        self.assertEqual(str(self.highcliff.diary()[0]['action_status']), "ActionStatus.SUCCESS")


if __name__ == '__main__':
    unittest.main()
