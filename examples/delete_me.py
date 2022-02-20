import unittest

# needed to run a local version of the AI
from highcliff.ai import AI

from highcliff.actions import ActionStatus

# the Highcliff actions to be tested
from highcliff.exampleactions import MonitorBodyTemperature

# needed to pretty-print the AI's execution logs
from pprint import pprint


# TODO: retrofit with the new infrastructure

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

        # define an action without implementing custom behavior
        class InvalidActionClass(MonitorBodyTemperature):
            pass

        try:
            self.assertRaises(NotImplementedError,
                              InvalidActionClass,
                              self.the_world_GLOBAL_VARIABLE,
                              self.capabilities_GLOBAL_VARIABLE)
        except:
            pass

    def test_action_properties_set_properly_at_action_instantiation(self):
        self.the_world_GLOBAL_VARIABLE = {}
        self.capabilities_GLOBAL_VARIABLE = []

        # define a test action with a blank custom behavior
        class TestAction(MonitorBodyTemperature):
            def behavior(self):
                pass

        # instantiate the test action
        test_action = TestAction(self.the_world_GLOBAL_VARIABLE, self.capabilities_GLOBAL_VARIABLE)

        # check the effects of the test action
        expected_effects = {"is_body_temperature_monitored": True, "is_room_temperature_comfortable": False}
        self.assertEqual(expected_effects, test_action.effects)

        # check the preconditions of the test action
        expected_preconditions = {"is_body_temperature_monitored": False}
        self.assertEqual(expected_preconditions, test_action.preconditions)

    def test_action_updates_the_world(self):
        # the world should be updated after an action occurs

        # define a test action with a blank custom behavior
        class TestAction(MonitorBodyTemperature):
            def behavior(self):
                pass

        # test that the known world is currently empty
        empty_world = {}
        self.assertEqual(empty_world, self.the_world_GLOBAL_VARIABLE)

        # add a dummy condition to the known world
        self.the_world_GLOBAL_VARIABLE = {'dummy_condition': False}

        # instantiate the test action
        test_action = TestAction(self.the_world_GLOBAL_VARIABLE, self.capabilities_GLOBAL_VARIABLE)
        expected_known_world = {**self.the_world_GLOBAL_VARIABLE, **test_action.effects}

        # take an action and test to see if that action properly affected the world
        test_action.act()
        self.assertEqual(expected_known_world, self.the_world_GLOBAL_VARIABLE)

    def test_action_registers_its_capabilities(self):
        # when an action is instantiated, it should register itself as a capability

        # define a test action with a blank custom behavior
        class TestAction(MonitorBodyTemperature):
            def behavior(self):
                pass

        # test that the capabilities registry is currently empty
        no_capabilities = []
        self.assertEqual(no_capabilities, self.capabilities_GLOBAL_VARIABLE)

        # instantiate the test action
        test_action = TestAction(self.the_world_GLOBAL_VARIABLE, self.capabilities_GLOBAL_VARIABLE)

        # test to see if the test action properly registered itself as a new capability
        self.assertTrue(len(self.capabilities_GLOBAL_VARIABLE) == 1)
        self.assertEqual(test_action, self.capabilities_GLOBAL_VARIABLE[0])

    def test_action_notifies_success(self):
        # an action that has the intended effect should record a success

        # define a test action with a successful behavior
        class TestSucceededAction(MonitorBodyTemperature):
            def behavior(self):
                pass

        TestSucceededAction(self.the_world_GLOBAL_VARIABLE, self.capabilities_GLOBAL_VARIABLE)

        # define the test world state and goals
        self.the_world_GLOBAL_VARIABLE = {"is_body_temperature_monitored": False}
        goals = {"is_body_temperature_monitored": True}

        # run a local version of Highcliff
        ai_life_span_in_iterations = 1
        highcliff = AI(self.the_world_GLOBAL_VARIABLE,
                       self.capabilities_GLOBAL_VARIABLE,
                       goals, ai_life_span_in_iterations)

        # the action should complete unsuccessfully
        pprint(highcliff.diary())
        self.assertEqual(ActionStatus.SUCCESS, highcliff.diary()[0]['action_status'])


if __name__ == '__main__':
    unittest.main()
