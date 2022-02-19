import unittest

# needed to run a local version of the AI
from highcliff.ai import AI

from highcliff.actions import ActionStatus

# the Highcliff actions to be tested
from highcliff.exampleactions import MonitorBodyTemperature

# needed to pretty-print the AI's execution logs
from pprint import pprint


class TestHighcliffExamples(unittest.TestCase):
    def setUp(self):
        # define global variables representing state of the world and the ai capabilities.
        # these global variables simulate underlying infrastructure when running a local version of Highcliff
        self.the_world_GLOBAL_VARIABLE = {}
        self.capabilities_GLOBAL_VARIABLE = []

    def tearDown(self):
        # remove the global variables created during set up
        del self.the_world_GLOBAL_VARIABLE
        del self.capabilities_GLOBAL_VARIABLE

    def test_custom_behavior_is_required(self):
        # an error should be thrown if an action's custom behavior is not defined
        self.assertTrue(False)

    def test_action_status_is_properly_set(self):
        # the status recorded should reflect the success or failure of an action
        self.assertTrue(False)

    def test_running_a_one_step_plan(self):
        # test that the ai can create a one-step plan to execute a single action with a single goal

        # define a test body temperature monitor with a blank custom behavior
        class TestBodyTemperatureMonitor(MonitorBodyTemperature):
            def behavior(self):
                pass

        # instantiate the test body temperature monitor
        test_body_temperature_monitor = TestBodyTemperatureMonitor(self.the_world_GLOBAL_VARIABLE,
                                                                   self.capabilities_GLOBAL_VARIABLE)

        # define the test world state and goals
        self.the_world_GLOBAL_VARIABLE = {"is_body_temperature_monitored": False}
        goals = {"is_body_temperature_monitored": True}

        # run a local version of Highcliff
        ai_life_span_in_iterations = 1
        highcliff = AI(self.the_world_GLOBAL_VARIABLE,
                       self.capabilities_GLOBAL_VARIABLE,
                       goals, ai_life_span_in_iterations)

        # the action should complete successfully
        self.assertEqual(ActionStatus.SUCCESS, highcliff.diary()[0]['action_status'])

        # the goal should have been to monitor body temperature
        self.assertEqual(goals, highcliff.diary()[0]['my_goal'])

        # the ai should have devised a one-step plan
        expected_plan_steps = 1
        self.assertEqual(expected_plan_steps, len(highcliff.diary()[0]['my_plan']))

        # the plan should have been to monitor body temperature
        self.assertEqual(test_body_temperature_monitor, highcliff.diary()[0]['my_plan'][0].action)

        # the initial world state should match the world state given
        self.assertEqual(self.the_world_GLOBAL_VARIABLE, highcliff.diary()[0]['the_world_state_before'])

        # the world should have been changed to match the goal state
        self.assertEqual(goals, highcliff.diary()[0]['the_world_state_after'])


if __name__ == '__main__':
    unittest.main()
