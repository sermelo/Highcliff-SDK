import copy
import unittest

# needed to connect to the central infrastructure
from highcliff.infrastructure import LocalNetwork, InvalidTopic

# needed to run a local version of the AI
from highcliff.ai import AI

from highcliff.actions import ActionStatus

# the Highcliff actions to be tested
from highcliff.exampleactions import MonitorBodyTemperature, AuthorizeRoomTemperatureChange, ChangeRoomTemperature, A, B, C

# global variables needed to test publish and subscribe
global published_topic
global published_message


class TestHighcliffExamples(unittest.TestCase):
    def setUp(self):
        # define the infrastructure used to coordinate and communicate
        self.network = LocalNetwork.instance()

    def tearDown(self):
        # reset the infrastructure
        self.network.reset()

    def test_custom_behavior_is_required(self):
        # an error should be thrown if an action's custom behavior is not defined

        # define an action without implementing custom behavior
        class InvalidActionClass(MonitorBodyTemperature):
            pass

        try:
            self.assertRaises(NotImplementedError,
                              InvalidActionClass,
                              self.network)
        except:
            pass

    def test_action_properties_set_properly_at_action_instantiation(self):

        # define a test action with a blank custom behavior
        class TestAction(MonitorBodyTemperature):
            def behavior(self):
                pass

        # instantiate the test action
        test_action = TestAction(self.network)

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
        self.assertEqual(empty_world, self.network.the_world())

        # add a dummy condition to the known world
        dummy_condition = {'dummy_condition': False}
        self.network.update_the_world(dummy_condition)

        # instantiate the test action
        test_action = TestAction(self.network)
        expected_known_world = {**self.network.the_world(), **test_action.effects}

        # take an action and test to see if that action properly affected the world
        test_action.act()
        self.assertEqual(expected_known_world, self.network.the_world())

    def test_action_registers_its_capabilities(self):
        # when an action is instantiated, it should register itself as a capability

        # define a test action with a blank custom behavior
        class TestAction(MonitorBodyTemperature):
            def behavior(self):
                pass

        # test that the capabilities registry is currently empty
        no_capabilities = []
        self.assertEqual(no_capabilities, self.network.capabilities())

        # instantiate the test action
        test_action = TestAction(self.network)

        # test to see if the test action properly registered itself as a new capability
        self.assertTrue(len(self.network.capabilities()) == 1)
        self.assertEqual(test_action, self.network.capabilities()[0])

    def test_action_notifies_success(self):
        # an action that has the intended effect should record a success

        # define a test action with a successful behavior
        class TestSucceededAction(MonitorBodyTemperature):
            def behavior(self):
                pass

        TestSucceededAction(self.network)

        # define the test world state and goals
        world_update = {"is_body_temperature_monitored": False}
        self.network.update_the_world(world_update)
        goals = {"is_body_temperature_monitored": True}

        # run a local version of Highcliff
        ai_life_span_in_iterations = 1
        highcliff = AI(self.network, goals, ai_life_span_in_iterations)

        # the action should complete unsuccessfully
        self.assertEqual(ActionStatus.SUCCESS, highcliff.diary()[0]['action_status'])

    def test_action_notifies_failure(self):
        # an action that does not have the intended effect should record a failure

        # define a test action with a behavior failure
        class TestFailedAction(MonitorBodyTemperature):

            def action_failure(self):
                self.effects['is_body_temperature_monitored'] = False

            def behavior(self):
                self.action_failure()

        TestFailedAction(self.network)

        # define the test world state and goals
        world_update = {"is_body_temperature_monitored": False}
        self.network.update_the_world(world_update)
        goals = {"is_body_temperature_monitored": True}

        # run a local version of Highcliff
        ai_life_span_in_iterations = 1
        highcliff = AI(self.network, goals, ai_life_span_in_iterations)

        # the action should complete unsuccessfully
        self.assertEqual(ActionStatus.FAIL, highcliff.diary()[0]['action_status'])

    @staticmethod
    def __is_subset_dictionary(subset_dictionary, superset_dictionary):
        is_subset = True
        for key in subset_dictionary:
            try:
                if subset_dictionary[key] != superset_dictionary[key]:
                    # there is a value in the subset not in the superset
                    is_subset = False
            except KeyError:
                # there is a key in the subset not in the superset
                is_subset = False

        return is_subset

    def test_running_a_one_step_plan(self):
        # test that the ai can create a one-step plan to execute a single action with a single goal

        # define a test body temperature monitor with a blank custom behavior
        class TestBodyTemperatureMonitor(MonitorBodyTemperature):
            def behavior(self):
                pass

        # instantiate the test body temperature monitor
        test_body_temperature_monitor = TestBodyTemperatureMonitor(self.network)

        # define the test world state and goals
        world_update = {"is_body_temperature_monitored": False}
        self.network.update_the_world(world_update)
        world_state_before_running_the_ai = copy.copy(self.network.the_world())
        goals = {"is_body_temperature_monitored": True}

        # run a local version of Highcliff
        ai_life_span_in_iterations = 1
        highcliff = AI(self.network, goals, ai_life_span_in_iterations)

        # the action should complete successfully
        self.assertEqual(ActionStatus.SUCCESS, highcliff.diary()[0]['action_status'])

        # the goal should have been recorded in the diary
        self.assertEqual(goals, highcliff.diary()[0]['my_goal'])

        # the ai should have devised a one-step plan
        expected_plan_steps = 1
        self.assertEqual(expected_plan_steps, len(highcliff.diary()[0]['my_plan']))

        # the plan should have been to monitor body temperature
        self.assertEqual(test_body_temperature_monitor, highcliff.diary()[0]['my_plan'][0].action)

        # the diary should have recorded that the world state before matched the original known world
        self.assertEqual(world_state_before_running_the_ai, highcliff.diary()[0]['the_world_state_before'])

        # the diary should have recorded that the world changed to reflect the goal state
        world_state_after_matches_goals = self.__is_subset_dictionary(goals,
                                                                      highcliff.diary()[0]['the_world_state_after'])
        self.assertTrue(world_state_after_matches_goals)

    def test_running_a_two_step_plan(self):
        # test that the ai can create a two-step plan to execute multiple actions to reach a goal

        # define a test body temperature monitor with a blank custom behavior
        class TestBodyTemperatureMonitor(MonitorBodyTemperature):
            def behavior(self):
                pass

        # instantiate the test body temperature monitor
        TestBodyTemperatureMonitor(self.network)

        # define a test body authorization application with a blank custom behavior
        class TestAuthorizationApp(AuthorizeRoomTemperatureChange):
            def behavior(self):
                pass

        # instantiate the test authorization app
        TestAuthorizationApp(self.network)

        # define the test world state and goals
        world_update = {"is_body_temperature_monitored": False, "is_room_temperature_change_authorized": False}
        self.network.update_the_world(world_update)
        goals = {"is_room_temperature_change_authorized": True}

        # run a local version of Highcliff
        ai_life_span_in_iterations = 2
        highcliff = AI(self.network, goals, ai_life_span_in_iterations)

        # the plan should have started with two steps, then progress to a single step
        self.assertEqual(2, len(highcliff.diary()[0]['my_plan']))
        self.assertEqual(1, len(highcliff.diary()[1]['my_plan']))

        # in the second iteration, the ai should have reached it's goal
        highcliff_reached_its_goal = self.__is_subset_dictionary(goals, highcliff.diary()[1]['the_world_state_after'])
        self.assertTrue(highcliff_reached_its_goal)

    def test_a_three_step_plan(self):
        # test that the ai can create a two-step plan to execute multiple actions to reach a goal

        class testA(A):
            def behavior(self):
                pass

        testA(self.network)

        class testB(B):
            def behavior(self):
                pass

        testB(self.network)

        class testC(C):
            def behavior(self):
                pass

        testC(self.network)

        # define the test world state and goals
        world_update = {}
        self.network.update_the_world(world_update)
        goals = {"is_room_temperature_comfortable": True}

        # run a local version of Highcliff
        ai_life_span_in_iterations = 3
        highcliff = AI(self.network, goals, ai_life_span_in_iterations)

        import pprint
        pprint.pprint(highcliff.diary())

        # the plan should have started with two steps, then progress to a single step
        self.assertEqual(3, len(highcliff.diary()[0]['my_plan']))
        self.assertEqual(2, len(highcliff.diary()[1]['my_plan']))
        self.assertEqual(1, len(highcliff.diary()[2]['my_plan']))

        # in the third iteration, the ai should have reached it's goal
        highcliff_reached_its_goal = self.__is_subset_dictionary(goals, highcliff.diary()[2]['the_world_state_after'])
        self.assertTrue(highcliff_reached_its_goal)

    def test_publish_subscribe(self):
        # create a topic
        test_topic = "test_topic"
        self.network.create_topic(test_topic)

        # create a callback function to test publishing
        def test_callback(topic, message):
            global published_message
            global published_topic

            published_topic = topic
            published_message = message

        # subscribe to the test topic
        self.network.subscribe(test_topic, test_callback)

        # publish a message to the subscribed topic
        test_message = {"payload": "test_payload", "effects": {"first_effect": True, "second_effect": True}}
        self.network.publish(test_topic, test_message)

        # subscribers should be notified when there is a new message posted to a topic of interest
        global published_message
        global published_topic
        self.assertEqual(test_topic, published_topic)
        self.assertEqual(test_message, published_message)

        # an invalid message should raise an error

        # an invalid topic should raise an error
        invalid_topic = "invalid_topic"
        try:
            self.assertRaises(InvalidTopic, self.network.publish, invalid_topic, test_message)
        except InvalidTopic:
            pass


if __name__ == '__main__':
    unittest.main()
