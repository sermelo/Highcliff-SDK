import pprint
import unittest

from highcliff.infrastructure import LocalNetwork
from highcliff.exampleactions import MonitorBodyTemperature
from highcliff.ai import AI


class TestAI(unittest.TestCase):
    def setUp(self):
        # define the infrastructure used to coordinate and communicate
        self.network = LocalNetwork.instance()

    def tearDown(self):
        # reset the infrastructure
        self.network.reset()

    def test_goal_not_in_any_actions(self):
        # if the ai has no registered actions to achieve a goal, it should end with no plan

        # define a test body temperature monitor with a blank custom behavior
        class TestAction(MonitorBodyTemperature):
            def behavior(self):
                pass

        # instantiate the test body temperature monitor
        TestAction(self.network)

        # define the test world state and goals
        world_update = {}
        self.network.update_the_world(world_update)
        goals = {"goal_not_in_the_test_action": True}

        # run a local version of Highcliff
        ai_life_span_in_iterations = 1
        highcliff = AI(self.network, goals, ai_life_span_in_iterations)

        # there should be no plan
        self.assertEqual(None, highcliff.diary()[0]['my_plan'])

    def test_goal_not_already_in_the_world(self):
        # if the ai encounters a goal not already in the world (in some state).
        # it should record that goal as unmet in the world

        # define a test body temperature monitor with a blank custom behavior
        class TestBodyTemperatureMonitor(MonitorBodyTemperature):
            def behavior(self):
                pass

        # instantiate the test body temperature monitor
        TestBodyTemperatureMonitor(self.network)

        # define the test world state and goals
        world_update = {}
        self.network.update_the_world(world_update)
        goals = {"is_room_temperature_change_needed": True}

        # run a local version of Highcliff
        ai_life_span_in_iterations = 1
        highcliff = AI(self.network, goals, ai_life_span_in_iterations)

        # before starting the first action, the ai should have notified the world that the goal was unmet
        unmet_goal = {"is_room_temperature_change_needed": False}
        self.assertEqual(unmet_goal, highcliff.diary()[0]['the_world_state_before'])

    def test_aimless_iterations(self):
        # the ai should be able to handle iterations with no goals
        # define a test body temperature monitor with a blank custom behavior
        class TestAction(MonitorBodyTemperature):
            def behavior(self):
                pass

        # instantiate the test body temperature monitor
        TestAction(self.network)

        # define the test world state and goals
        world_update = {}
        self.network.update_the_world(world_update)
        goals = {"is_room_temperature_change_needed": True}

        # run a local version of Highcliff
        ai_life_span_in_iterations = 3
        highcliff = AI(self.network, goals, ai_life_span_in_iterations)

        # it only takes 1 iteration for the ai to solve the problem
        # the remaining iterations should have no goal or plan
        no_goal = {}
        self.assertEqual(no_goal, highcliff.diary()[1]['my_goal'])
        self.assertEqual(no_goal, highcliff.diary()[2]['my_goal'])
        no_plan = []
        self.assertEqual(no_plan, highcliff.diary()[1]['my_plan'])
        self.assertEqual(no_plan, highcliff.diary()[2]['my_plan'])


if __name__ == '__main__':
    unittest.main()
