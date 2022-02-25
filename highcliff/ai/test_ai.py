import pprint
import unittest

from highcliff.infrastructure import LocalNetwork
from highcliff.exampleactions import MonitorBodyTemperature
from highcliff.ai import AI


class TestAI(unittest.TestCase):
    def setUp(self):
        # define the infrastructure used to coordinate and communicate
        self.network = LocalNetwork.instance()

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

    def test_goal_not_in_the_world(self):
        pass

    def test_aimless_iterations(self):
        # the ai should be able to handle iterations with no goals
        pass

if __name__ == '__main__':
    unittest.main()
